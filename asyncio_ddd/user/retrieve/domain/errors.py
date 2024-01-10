from pydantic import UUID4


class UserNotFoundError(Exception):
    def __init__(self, user_id: UUID4):
        self.message = f"[user id: {str(user_id)}]"
        super().__init__(self.message)
