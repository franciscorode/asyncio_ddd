from uuid import UUID


class UserAlreadyExistError(Exception):
    def __init__(self, user_id: UUID):
        self.message = f"[user id: {str(user_id)}]"
        super().__init__(self.message)
