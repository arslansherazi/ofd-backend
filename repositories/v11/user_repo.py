from repositories.v10.user_repo import UserRepository


class UserRepositoryV11(UserRepository):
    USER_ALREADY_LOGGEDIN_MESSAGE = 'User is already logged in from another device'
    USERNAME_UPDTED_SUCCESSFULLY = 'username updated successfully'
