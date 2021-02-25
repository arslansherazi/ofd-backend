import secrets
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.utils import timezone

from common.constants import EMAIL_VERIFICATION_LINK_EXPIRATION_TIME


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, profile_image_url, user_type):
        """
        Creates user

        :param str username: username
        :param str email: email
        :param str password: password
        :param str profile_image_url: profile image url
        :param int user_type: user type
        :return:
        """
        user = self.model(username=username, email=email, profile_image_url=profile_image_url, user_type=user_type)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=100)
    profile_image_url = models.TextField()
    user_type = models.IntegerField(db_index=True)
    email_verification_code = models.IntegerField(null=True, default=None)
    forgot_password_code = models.IntegerField(null=True, default=None)
    change_email_code = models.IntegerField(null=True, default=None)
    is_email_verified = models.BooleanField(default=False)
    email_verification_code_expiration = models.DateTimeField(null=True, default=None)
    forgot_password_code_expiration = models.DateTimeField(null=True, default=None)
    change_email_code_expiration = models.DateTimeField(null=True, default=None)
    change_password_token = models.CharField(max_length=255, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()

    # configurations
    USERNAME_FIELD = 'email'
    objects = UserManager()

    # not required fields
    last_login = None

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.updated_date = timezone.now()
        return super(User, self).save(*args, **kwargs)

    @classmethod
    def check_username_availability(cls, username, user_type):
        """
        Checks that username is available or not

        :param str username: username
        :param int user_type: user type
        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(username=username, user_type=user_type)
        user = _q.values('id')
        if user:
            return False
        return True

    @classmethod
    def check_email_availability(cls, email, user_type):
        """
        Checks that email already exists or not

        :param str email: email
        :param int user_type: user type
        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(email=email, user_type=user_type)
        user = _q.values('id')
        if user:
            return True
        return False

    @classmethod
    def insert_user_into_db(cls, username, email, password, profile_image_url, user_type):
        """
        Inserts user into the system

        :param str username: username
        :param str email: email
        :param str password: password
        :param str profile_image_url: profile image url
        :param int user_type: user type
        :rtype int
        :returns user id
        """
        user = cls.objects.create_user(username, email, password, profile_image_url, user_type)
        user_id = user.id
        return user_id

    @classmethod
    def get_user_login_info(cls, user_id=None, username=None, user_type=None):
        """
        Gets user login info

        :param int user_id: user id
        :param str username: username
        :param int user_type: user type
        :return user login info
        :rtype: dict
        """
        _q = cls.objects
        if user_id:
            _q = _q.filter(id=user_id)
        else:
            _q = _q.filter((Q(username=username) | Q(email=username)), user_type=user_type)
        user = _q.values('email', 'password', 'is_email_verified').first()
        return user

    @classmethod
    def get_forgot_password_email_code_and_expiration(cls, user_id, change_password_token):
        """
        Gets forgot password email code and expiration

        :param int user_id: user id
        :param str change_password_token: change password token
        :return: forgot password code and expiration time
        :rtype dict
        """
        _q = cls.objects
        _q = _q.filter(id=user_id, change_password_token=change_password_token)
        forgot_password_data = _q.values(
            'forgot_password_code', 'forgot_password_code_expiration'
        ).first()
        return forgot_password_data

    @classmethod
    def get_email_verification_code_and_expiration(cls, user_id):
        """
        Verifies email verification code and expiration

        :param int user_id: user id
        :param int code: code
        :return: email verification code and expiration time
        :rtype dict
        """
        _q = cls.objects
        _q = _q.filter(id=user_id)
        email_verification_data = _q.values(
            'is_email_verified', 'email_verification_code', 'email_verification_code_expiration'
        ).first()
        return email_verification_data

    @classmethod
    def get_change_email_code_and_expiration(cls, user_id, email):
        """
        Gets change email code and expiration

        :param id user_id: user id
        :param str email: email
        :param int code: code
        :return: change email verification code and expiration time
        :rtype dict
        """
        _q = cls.objects
        _q = _q.filter(id=user_id, email=email)
        change_email_data = _q.values('change_email_code', 'change_email_code_expiration').first()
        return change_email_data

    @classmethod
    def update_email_verification_status(cls, user_id):
        """
        Updates email verification status

        :param int user_id: user id
        """
        user = cls.objects.get(id=user_id)
        user.is_email_verified = True
        user.save()

    @classmethod
    def update_forgot_password_code_and_expiration(cls, user_id, code):
        """
        Updates forgot password code and expiration time

        :param int user_id: user id
        :param int code: forgot password code
        :returns change password token
        :rtype str
        """
        user = cls.objects.get(id=user_id)
        user.forgot_password_code = code
        user.forgot_password_code_expiration = timezone.now() + timedelta(hours=EMAIL_VERIFICATION_LINK_EXPIRATION_TIME)
        user.change_password_token = secrets.token_hex()
        user.save()
        return user.change_password_token

    @classmethod
    def update_change_email_code_and_expiration(cls, user_id, code):
        """
        Updates change email code and expiration time.
        It also expires forgot password code so that forgot password links on old email will also expire

        :param int user_id: user id
        :param int code: change email code
        """
        user = cls.objects.get(id=user_id)
        user.change_email_code = code
        user.change_email_code_expiration = timezone.now() + timedelta(hours=EMAIL_VERIFICATION_LINK_EXPIRATION_TIME)
        if user.forgot_password_code_expiration:
            user.forgot_password_code_expiration -= timedelta(days=10)
        user.save()

    @classmethod
    def update_email_verification_code_and_expiration(cls, user_id, code):
        """
        Updates email verification code and expiration time

        :param int user_id: user id
        :param int code: forgot password code
        """
        user = cls.objects.get(id=user_id)
        user.email_verification_code = code
        user.email_verification_code_expiration = timezone.now() + timedelta(
            hours=EMAIL_VERIFICATION_LINK_EXPIRATION_TIME
        )
        user.save()

    @classmethod
    def update_password(cls, user_id, password, is_forgot_password=False):
        """
        Updates password of user

        :param int user_id: user id
        :param str password: password
        :param bool is_forgot_password: forgot password flag
        """
        user = cls.objects.get(id=user_id)
        user.set_password(password)
        if is_forgot_password:
            user.is_email_verified = True
            user.change_password_token = None
        user.save()

    @classmethod
    def get_user_id(cls, username, user_type):
        """
        Gets user id of user by username/email

        :param str username: username/email
        :param int user_type: user type
        :rtype int
        :return: user id
        """
        _q = cls.objects
        _q = _q.filter((Q(email=username) | Q(username=username)), user_type=user_type)
        user_data = _q.values('id').first()
        user_id = user_data.get('id')
        return user_id

    @classmethod
    def change_user_email(cls, user_id, new_email):
        """
        Changes user email

        :param int user_id: user id
        :param str new_email: new email
        """

        user = cls.objects.get(id=user_id)
        user.email = new_email
        user.save()

    @classmethod
    def update_profile_image_url(cls, user_id, profile_image_url):
        """
        Updates profile image url

        :param int user_id: user id
        :param str profile_image_url: profile image url
        """

        user = cls.objects.get(id=user_id)
        user.profile_image_url = profile_image_url
        user.save()

    @classmethod
    def get_profile_image_url(cls, user_id):
        """
        Gets profile image url

        :param int user_id: user id
        """
        _q = cls.objects
        _q = _q.filter(id=user_id)
        user = _q.values('profile_image_url').first()
        return user.get('profile_image_url')

    @classmethod
    def update_data(cls, user_id=None, username=None, profile_image_url=None):
        """
        Updates username or profile image url

        :param int user_id: user id
        :param str username: username
        :param str profile_image_url: profile image url
        """
        _q = cls.objects
        user = _q.filter(id=user_id)
        if username:
            user.update(username=username)
        if profile_image_url:
            user.update(profile_image_url=profile_image_url)

    @classmethod
    def delete_user(cls, user_id):
        """
        Deletes user

        :param int user_id: user id
        """
        user = cls.objects.get(id=user_id)
        user.delete()

    @classmethod
    def verify_email(cls, email):
        """
        Verifies that either email already exists or not

        :param str email: email
        :rtype boolean
        """
        _q = cls.objects
        _q = _q.filter(email=email)
        user_email = _q.values('email')
        if user_email:
            return True
        return False
