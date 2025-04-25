from beanie import Document

class User(Document):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "example@gmail.com",
                "full_name": "John Doe",
                "disabled": False,
                "hashed_password": "hashed_password_example"
                }
            }


