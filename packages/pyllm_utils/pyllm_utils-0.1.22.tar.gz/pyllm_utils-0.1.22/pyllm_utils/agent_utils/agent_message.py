class MessageList:
    def __init__(self, max_length=None, trim_strategy="first", role_key="role", content_key="content"):
        """
        Initialize a MessageList object.
        
        Args:
            max_length (int, optional): Maximum number of elements in the list. None means no limit.
            trim_strategy (str or list, optional): Strategy for trimming when max length is reached.
                String options: "first", "last", "system_preserve".
                List/set options: Specific indices to remove when trimming (these are post-insertion indices).
            role_key (str, optional): Key name for the role field in messages. Default is "role".
            content_key (str, optional): Key name for the content field in messages. Default is "content".
        """
        self._messages = []
        self.max_length = max_length
        self.trim_strategy = trim_strategy
        self.role_key = role_key
        self.content_key = content_key
    
    def __getitem__(self, index):
        """Allow indexing like a regular list."""
        return self._messages[index]
    
    def __setitem__(self, index, value):
        """Allow setting items by index."""
        self._validate_message(value)
        self._messages[index] = value
        
    def __len__(self):
        """Return the number of messages."""
        return len(self._messages)
    
    def __iter__(self):
        """Allow iteration."""
        return iter(self._messages)
    
    def __str__(self):
        """String representation of the message list."""
        return str(self._messages)
    
    def __repr__(self):
        """Detailed string representation of the message list."""
        return f"MessageList(messages={self._messages}, max_length={self.max_length}, trim_strategy='{self.trim_strategy}')"
    
    def __contains__(self, item):
        """Check if an item is in the list."""
        return item in self._messages
    
    def _validate_message(self, item):
        """
        Validate that the item is a dict and has the required keys (role_key, content_key).
        Raises ValueError if validation fails.
        """
        if not isinstance(item, dict):
            raise ValueError("MessageList only supports dict items.")
        if self.role_key not in item or self.content_key not in item:
            raise ValueError(f"Item must contain '{self.role_key}' and '{self.content_key}' keys.")
    
    def append(self, item):
        """
        Append an item (dict) to the end of the list.
        Must contain at least `role_key` and `content_key`.
        
        Args:
            item (dict): The message to append.
        """
        self._validate_message(item)
        self._messages.append(item)
        self._trim_if_needed()
    
    def insert(self, index, item):
        """
        Insert an item (dict) at the given position.
        Must contain at least `role_key` and `content_key`.
        
        Args:
            index (int): The position to insert.
            item (dict): The message to insert.
        """
        self._validate_message(item)
        self._messages.insert(index, item)
        self._trim_if_needed()
    
    def _trim_if_needed(self):
        """
        Trim the list if it exceeds the maximum length.
        """
        if self.max_length is None or len(self._messages) <= self.max_length:
            return
        
        # If trim_strategy is a list or set of indices to remove
        if isinstance(self.trim_strategy, (list, set, tuple)):
            indices_to_remove = sorted(self.trim_strategy, reverse=True)
            while len(self._messages) > self.max_length and indices_to_remove:
                idx = indices_to_remove[0]
                indices_to_remove = indices_to_remove[1:]
                if 0 <= idx < len(self._messages):
                    self._messages.pop(idx)
            while len(self._messages) > self.max_length:
                self._messages.pop(0)
        else:
            # Handle string-based strategies
            while len(self._messages) > self.max_length:
                if self.trim_strategy == "first":
                    self._messages.pop(0)
                elif self.trim_strategy == "last":
                    self._messages.pop()
                elif self.trim_strategy == "system_preserve":
                    # Keep system messages, remove the oldest non-system message
                    for i, msg in enumerate(self._messages):
                        if msg[self.role_key] != "system":
                            self._messages.pop(i)
                            break
                    else:
                        # If all messages are system messages, remove the oldest one
                        self._messages.pop(0)
    
    def get_list(self):
        """
        Get the complete list of messages.
        
        Returns:
            list: The message list.
        """
        return self._messages

    def clear(self):
        """
        Clear all messages from the list.
        
        Returns:
            MessageList: Self for method chaining.
        """
        self._messages.clear()
        return self

    def pop(self, index=-1):
        """
        Remove and return an item at index (default last).
        
        Args:
            index (int, optional): Index of the item to remove. Default is -1 (last item).
        
        Returns:
            dict: The removed message.
        """
        return self._messages.pop(index)

    def remove(self, message):
        """
        Remove the first occurrence of a message.
        
        Args:
            message (dict): Message to remove.
        
        Returns:
            MessageList: Self for method chaining.
        """
        self._messages.remove(message)
        return self

    def count(self, role=None):
        """
        Count messages, optionally filtered by role.
        
        Args:
            role (str, optional): If provided, count only messages with this role.
        
        Returns:
            int: Number of messages (matching the role if specified).
        """
        if role is None:
            return len(self._messages)
        return sum(1 for msg in self._messages if msg[self.role_key] == role)

    def extend(self, messages):
        """
        Extend the list by appending elements from the iterable.
        
        Args:
            messages (iterable): Iterable of messages (dicts) to add.
        
        Returns:
            MessageList: Self for method chaining.
        """
        for msg in messages:
            self._validate_message(msg)
            self._messages.append(msg)
            self._trim_if_needed()
        return self

    # ----- Optional convenience methods -----
    # もし「roleとcontentを直接指定して追加したい」ようなもともとの機能を残したい場合は、
    # add_xxxのような別名メソッドを用意しておくと便利です。

    def add_message(self, role, content, **kwargs):
        """
        Insert a message at the end (like original append) by specifying role/content.
        
        Args:
            role (str): role of the message
            content (str): content of the message
            **kwargs: additional keys
        """
        msg = {self.role_key: role, self.content_key: content, **kwargs}
        self.append(msg)  # 内部的にはappend(item)でOK
        return self

    def insert_message(self, index, role, content, **kwargs):
        """
        Insert a message at the specified index by specifying role/content.
        """
        msg = {self.role_key: role, self.content_key: content, **kwargs}
        self.insert(index, msg)
        return self

    def update_system_content(self, new_content):
        """
        Update the content of the first system role message.
        
        Args:
            new_content (str): New content for the system message.
        
        Returns:
            MessageList: Self for method chaining.
        
        Raises:
            ValueError: If no system message is found.
        """
        for msg in self._messages:
            if msg[self.role_key] == "system":
                msg[self.content_key] = new_content
                return self
        raise ValueError("No system message found")

    def update_content(self, index, new_content):
        """
        Update the content of a message at the specified index.
        
        Args:
            index (int): Index of the message to update.
            new_content (str): New content for the message.
        
        Returns:
            MessageList: Self for method chaining.
        """
        self._messages[index][self.content_key] = new_content
        return self

    def update_role(self, index, new_role):
        """
        Update the role of a message at the specified index.
        
        Args:
            index (int): Index of the message to update.
            new_role (str): New role for the message.
        
        Returns:
            MessageList: Self for method chaining.
        """
        self._messages[index][self.role_key] = new_role
        return self
