"""
User Repository V100
"""
from apps.user.repositories.v100.user_repo import UserRepository


class UserRepositoryV110(UserRepository):
    """
    User Repository V100
    """
    USER_ALREADY_LOGGEDIN_MESSAGE = 'User is already logged in from another device'
    USERNAME_UPDTED_SUCCESSFULLY = 'username updated successfully'
