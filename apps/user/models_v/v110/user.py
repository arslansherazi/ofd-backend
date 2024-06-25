from apps.user.models import User


class UserV110(User):
    class Meta:
        proxy = True

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
