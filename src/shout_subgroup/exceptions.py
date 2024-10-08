class NotGroupChatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GroupChatDoesNotExistError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SubGroupDoesNotExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SubGroupExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidSubGroupNameError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
