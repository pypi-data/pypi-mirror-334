import asyncio
from .llm import LLMAPIClient
from .utils.prompt_editor.prompt_editor import PromptEditor
from .agent_utils.agent_message import MessageList
import inspect
from typing import Dict, Callable, Optional, Any, TypedDict, Union

class ResponseDict(TypedDict):
    role: str
    content: str

class Agent:
    def __init__(self,
                 model="gpt-4o",
                 template_source=None,
                 max_messages=None,
                 trim_strategy=[1],
                 output_format=None,
                 output_fields=None,
                 output_free=None,
                 postprocessor=None,
                 system_data=None):
        """
        Initialize an Agent object.
        
        Args:
            model (str): The LLM model to use.
            template_source (str or Path, optional): Template source for the system prompt.
            max_messages (int, optional): Maximum number of messages to keep.
            trim_strategy (list or str, optional): Strategy for trimming when max length is reached.
            output_format (dict, optional): Format specification for the output JSON structure.
            output_fields (dict, optional): Simplified format specification.
            postprocessor (dict, optional): Dictionary mapping field names to callback functions.
                Each callback is a function that takes the value of its corresponding field from the LLM response
                and processes it in some way. Callbacks can be either synchronous or asynchronous functions.
                
                Format: {field_name: callback_function}
                
                Callback functions must:  
                - Take a single argument (the value of the field from the LLM response)
                - Return one of the following:
                  1. A dictionary with "role" and "content" keys: This will be added as a new message to the
                     conversation history. Example: {"role": "assistant", "content": "The result is 10"}
                  2. Any other value: Will be included in the result dictionary with the original field name
                  3. None: The field will be omitted from the result dictionary
                
                Behavior:
                - Callbacks are executed in parallel (using asyncio.gather)
                - Fields without callbacks are directly added to the result dictionary
                - Asynchronous callbacks (coroutines) are awaited automatically
                - If a callback returns a valid message dictionary, it's added to the conversation history
                  and not included in the returned result dictionary
                
                Typical use cases for postprocessors:
                - Performing calculations or validations on LLM output
                - Transforming LLM output into a different format
                - Adding additional context or information to the conversation
                - Handling LLM output that requires further processing before presenting to the user
            system_data (dict, optional): Additional data to include in the system message.
        
        Raises:
            TypeError: If callbacks are not properly formatted or don't return the expected type.
        """
        self.messages = AgentMessages(template_source, max_messages, trim_strategy, output_format, output_fields, output_free)
        self.llm = LLMAPIClient(model, json_mode=True)
        self.postprocessor = postprocessor
        self.system_data = system_data
        
        # Validate callbacks if provided
        if self.postprocessor is not None:
            if not isinstance(self.postprocessor, dict):
                raise TypeError("callbacks must be a dictionary mapping field names to callback functions")
            
            for field, callback in self.postprocessor.items():
                if callback is not None and not callable(callback):
                    raise TypeError(f"Callback for field '{field}' must be callable or None")
    
    async def run(self, stream=False, stream_keys=None, **kwargs):
        """
        Run the agent with the given user input.
        
        Args:
            user_input (str): The user input message.
            postprocessor (dict, optional): Callback functions for each output field.
                Format: {field_name: callback_function}
            system_data (dict, optional): Data to update the system message directly.
                This is ignored if preprocessor is provided.
        
        Returns:
            dict: The response from the LLM.
        """
        key_set = self.messages.prompt_editor.extract_variables()
        if set(kwargs.keys()) != key_set:
            raise ValueError("Unexpected keys in kwargs. Expected: {}, Actual: {}".format(key_set, set(kwargs.keys())))
        self.messages.update_system(kwargs)
        
        # Get messages and request to LLM
        messages = self.messages.get_messages()
        if stream:
            response = self.llm.request_messages(messages=messages, json_mode=True, stream=True, stream_keys=stream_keys)
            async def stream_response(response):
                for chunk in response:
                    yield chunk
                response = self.llm.get_latest_response()
                yield None, response
                yield None, await self._process_response(response)
            return stream_response(response)
                
        else:
            response = self.llm.request_messages(messages=messages, json_mode=True)
            return await self._process_response(response)
    

    async def _process_response(self, response: dict) -> dict:
        run_result: dict = {} 
        # Process the response
        if isinstance(response, dict):
            # Create tasks for all callbacks to run in parallel
            tasks = []
            no_callback_fields = []
            field_order = []
            
            for field, result in response.items():
                field_order.append(field)
                if self.postprocessor is not None:
                    this_callback = self.postprocessor.get(field, None)
                    if callable(this_callback):
                        # Create a task for each callback
                        async def process_callback(f, r, c=this_callback):
                            return f, await c(r) if inspect.iscoroutinefunction(c) else c(r)
                        
                        tasks.append(process_callback(field, response[field]))
                    else:
                        # Track fields that have no callback
                        no_callback_fields.append(field)
                else:
                    # If there's no postprocessor at all, track all fields
                    no_callback_fields.append(field)
            
            # Execute all callback tasks in parallel
            if tasks:
                results = await asyncio.gather(*tasks)
                
            # Process the results in the original order
            for field in field_order:
                if field in no_callback_fields:
                    field_content = response.get(field)
                    if isinstance(field_content, str):
                        self.messages.add("assistant", field_content)
                        run_result[field] = field_content
                    else:
                        run_result[field] = field_content
                else:
                    result = next((r for f, r in results if f == field), None)
                    if isinstance(result, dict) and result.get("role", None) and result.get("content", None):
                        self.messages.add(result["role"], result["content"])
                        run_result[field] = result["content"]
                    else:
                        run_result[field] = result
        return run_result

class AgentMessages:
    def __init__(self, 
                 template_source=None, 
                 max_messages=None, 
                 trim_strategy=[1],  # インデックス1（最初のuser/assistantメッセージ）を削除
                 output_format=None,
                 output_fields=None,
                 output_free=None):
        """
        Initialize an AgentMessages object.
        
        Args:
            template_source (str or Path, optional): Template source for the system prompt.
            max_messages (int, optional): Maximum number of messages to keep. None means no limit.
            trim_strategy (list or str, optional): Strategy for trimming when max length is reached.
                Default is [1], which removes the first user/assistant message (index 1).
            output_format (dict, optional): Format specification for the output JSON structure.
                Format: {key: {"type": type_str, "description": desc_str}}
            output_fields (dict, optional): Simplified format specification.
                Format: {key: description_str}
            output_free (str, optional): Free text message to use instead of JSON format prompt.
                If provided, this will be prioritized over output_format and output_fields.
        """
        # Initialize the message list
        self.messages = MessageList(max_length=max_messages, trim_strategy=trim_strategy)
        
        # Initialize the prompt editor if template is provided
        self.prompt_editor = None
        if template_source is not None:
            self.prompt_editor = PromptEditor(template_source)
        
        # Store output_free for later use
        self.output_free = output_free
        
        # Convert simplified output_fields to full output_format if provided
        if output_fields is not None and output_format is None:
            output_format = {}
            for key, description in output_fields.items():
                output_format[key] = {"type": "string", "description": description}
        
        # Always create a system message
        if self.prompt_editor is None:
            # デフォルトのシステムテンプレートを作成
            self.prompt_editor = PromptEditor("あなたは便利なアシスタントです。")
        
        # 出力フォーマットが指定されていなければデフォルト値を設定
        if output_format is None and output_fields is None and output_free is None:
            output_fields = {
                "chat": "相手への意思表示、必要なければ空文字",
                "thought": "思考プロセス",
                "action": "次の行動"
            }
            # 簡易フォーマットをoutput_formatに変換
            output_format = {}
            for key, description in output_fields.items():
                output_format[key] = {"type": "string", "description": description}
        
        # システムメッセージを作成（必須）
        system_content = self._generate_system_content(output_format)
        self.messages.add_message("system", system_content)
        
        # Add the final user message - either output_free or JSON format prompt
        if self.output_free:
            # If output_free is provided, use it as the final user message
            self.messages.add_message("user", self.output_free)
        else:
            # Otherwise, use the JSON format prompt
            json_format_prompt = self._generate_json_format_prompt(output_format)
            self.messages.add_message("user", json_format_prompt)
    
    def _generate_system_content(self, output_format):
        """
        Generate system content based on the template and output format.
        
        Args:
            output_format (dict): Format specification for the output JSON structure.
        
        Returns:
            str: Generated system content.
        """
        # システムメッセージにはテンプレート内容のみを使用
        # JSONフォーマットはユーザーメッセージに入れる
        return self.prompt_editor.template
    
    def _generate_json_format_prompt(self, output_format):
        """
        Generate JSON format prompt for the user message.
        
        Args:
            output_format (dict): Format specification for the output JSON structure.
        
        Returns:
            str: Generated JSON format prompt.
        """
        prompt = "上記のuser,assistantの履歴があれば上記に対して下記のJSONフォーマットのみで応答してください。：\n"
        prompt += "{\n"
        
        # Add each field with type and description
        for idx, (key, info) in enumerate(output_format.items()):
            field_type = info.get("type", "string")
            description = info.get("description", "")
            
            prompt += f'    "{key}": {field_type}, // {description}'
            if idx < len(output_format) - 1:
                prompt += "\n"
        
        return prompt
    
    def add(self, role, content, **kwargs):
        """
        Add a message to the conversation, inserting it before the last message.
        
        Args:
            role (str): Role of the message (e.g., "user", "assistant").
            content (str): Content of the message.
            **kwargs: Additional message attributes.
        
        Returns:
            AgentMessages: Self for method chaining.
        """
        # Insert before the last message (which is always a user message with JSON format prompt)
        self.messages.insert_message(-1, role, content, **kwargs)
        return self
    
    def update_system(self, data):
        """
        Update the system message by applying the template with the given data.
        
        Args:
            data (dict): Data to be applied to the template.
        
        Returns:
            AgentMessages: Self for method chaining.
        
        Raises:
            ValueError: If there is no prompt editor or system message.
        """
        if self.prompt_editor is None:
            raise ValueError("No prompt editor configured.")
        
        new_content = self.prompt_editor.apply(data)
        self.messages.update_system_content(new_content)
        return self
    
    def update_json_format(self, output_format=None, output_fields=None, output_free=None):
        """
        Update the JSON format prompt in the last user message.
        
        Args:
            output_format (dict, optional): New format specification for the output JSON.
            output_fields (dict, optional): Simplified format specification.
            output_free (str, optional): Free text message to use instead of JSON format prompt.
        
        Returns:
            AgentMessages: Self for method chaining.
        """
        # If output_free is provided, use it instead of JSON format
        if output_free is not None:
            self.output_free = output_free
            self.messages[-1]["content"] = output_free
            return self
            
        # Convert simplified output_fields to full output_format if provided
        if output_fields is not None and output_format is None:
            output_format = {}
            for key, description in output_fields.items():
                output_format[key] = {"type": "string", "description": description}
        
        if output_format is not None and self.output_free is None:
            json_format_prompt = self._generate_json_format_prompt(output_format)
            self.messages[-1]["content"] = json_format_prompt
        
        return self
    
    def get_messages(self):
        """
        Get all messages as a list.
        
        Returns:
            list: List of message dictionaries.
        """
        return self.messages.get_list()
    
    def clear(self):
        """
        Clear all messages except the system message and the last JSON format user message.
        
        Returns:
            AgentMessages: Self for method chaining.
        """
        system_msg = None
        json_format_msg = None
        
        # 最初のシステムメッセージと最後のJSONフォーマットメッセージを保存
        if len(self.messages) > 0:
            if self.messages[0]["role"] == "system":
                system_msg = self.messages[0]
        
        if len(self.messages) > 0:
            json_format_msg = self.messages[-1]
        
        self.messages.clear()
        
        # Re-add the system message
        if system_msg:
            self.messages.append(system_msg)
        else:
            # システムメッセージがなければデフォルトを追加
            self.messages.add_message("system", "あなたは便利なアシスタントです。")
        
        # Always keep the final user message
        if json_format_msg:
            self.messages.append(json_format_msg)
        else:
            # If we have output_free, use it
            if self.output_free:
                self.messages.add_message("user", self.output_free)
            else:
                # Otherwise use default JSON format
                default_format = {
                    "chat": {"type": "string", "description": "相手への意思表示、必要なければ空文字"},
                    "thought": {"type": "string", "description": "思考プロセス"},
                    "action": {"type": "string", "description": "次の行動"}
                }
                json_format_prompt = self._generate_json_format_prompt(default_format)
                self.messages.add_message("user", json_format_prompt)
        return self
    
    def __len__(self):
        """Return the number of messages."""
        return len(self.messages)
    
    def __str__(self):
        """String representation of the AgentMessages."""
        return str(self.messages)
    
    def __repr__(self):
        """Detailed string representation of the AgentMessages."""
        return f"AgentMessages(messages={self.messages}, prompt_editor={self.prompt_editor})"