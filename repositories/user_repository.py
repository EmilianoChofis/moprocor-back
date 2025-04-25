from models.user import User

class UserRepository:
    """ User repository class to manage user data. """

    @staticmethod
    async def get_user_by_username(username: str):
        """
        Get a user by username.
        :param username: The username of the user to retrieve.
        :type username: str
        :return: The User document with the given username, or None if not found.
        :rtype: User
        """
        return await User.find_one({"username": username})