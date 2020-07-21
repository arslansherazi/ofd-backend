from rest_framework_simplejwt import views as jwt_views

from apis.v10.change_password.api import ChangePassword
from apis.v10.delete_user.api import DeleteUser
from apis.v10.get_profile.api import GetProfile
from apis.v10.login.api import Login
from apis.v10.send_email.api import SendEmail
from apis.v10.signup.api import Signup
from apis.v10.update_profile.api import UpdateProfile
from apis.v10.validate_email.api import ValidateEmail
from apis.v10.verify_email.api import VerifyEmail
from routing.base_routing import BaseRouting


class RoutingV10(BaseRouting):
    api_version = '10'

    def set_routing_collection(self):
        self.routing_collection = {
            'login': Login,
            'signup': Signup,
            'validate_email': ValidateEmail,
            'send_email': SendEmail,
            'change_password': ChangePassword,
            'verify_email': VerifyEmail,
            'update_profile': UpdateProfile,
            'delete_user': DeleteUser,
            'get_profile': GetProfile,
            'api_token': jwt_views.TokenObtainPairView
        }
