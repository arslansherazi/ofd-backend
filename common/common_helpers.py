import os
import random
from operator import itemgetter

import bcrypt
import geopy.distance
from cryptography.fernet import Fernet
from exponent_server_sdk import PushClient, PushMessage, PushServerError
from PIL import Image
from shapely import wkt
from shapely.geometry import Point

from common.constants import (AVERAGE_PREPARATION_TIME, BUFFER_TIME,
                              MENU_IMAGE_DIMENSIONS,
                              MENU_ITEM_IMAGE_DIMENSIONS,
                              PROFILE_IMAGE_DIMENSIONS)
from models.location import Location
from security.security_credentials import ENCRYPTION_KEY


class CommonHelpers(object):
    @staticmethod
    def generate_six_digit_random_code():
        """
        Generates 6 digit random code
        """
        code = random.randrange(100000, 999999, 1)
        return code

    @staticmethod
    def generate_password_hash(password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        return password_hash.decode()

    # @staticmethod
    # def pad(data):
    #     """
    #     Add padding into data
    #
    #     :param data data: data
    #     :returns: data after adding padding into it
    #     """
    #     dummy = data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)
    #     return dummy
    #
    # # @staticmethod
    # # def unpad(data):
    # #     """
    # #     Remove padding from data
    # #     """
    # #     return data[:-ord(data[len(data)–1:])]
    #
    # @staticmethod
    # def encrypt_data(data):
    #     data = CommonHelpers.pad(data)
    #     aes = AES.new(ENCRYPTION_KEY, mode=AES.MODE_CBC, IV=ENCRYPTION_SALT)
    #     encrypted_data = aes.encrypt(data)
    #     return base64.b64encode(encrypted_data).decode()
    #
    # @staticmethod
    # def decrypt_data(encrypted_data):
    #     encrypted_data = base64.b64decode(encrypted_data)
    #     aes = AES.new(ENCRYPTION_KEY, mode=AES.MODE_CBC, IV=ENCRYPTION_SALT)
    #     decrypted_data = aes.decrypt(encrypted_data)
    #     return decrypted_data.decode()

    @staticmethod
    def encrypt_data(data):
        cipher_suite = Fernet(ENCRYPTION_KEY.encode())
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    @staticmethod
    def decrypt_data(encrypted_data):
        cipher_suite = Fernet(ENCRYPTION_KEY.encode())
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    @staticmethod
    def process_image(image, is_menu_image=False, is_menu_item_image=False, is_profile_image=False):
        """
        Process image. Verifies the size of image and converts image to required size and also makes small image
        if required
        """
        uploaded_image = Image.open(image)
        image_dimensions = uploaded_image.size
        if is_menu_item_image:
            if image_dimensions != MENU_ITEM_IMAGE_DIMENSIONS:
                image = uploaded_image.resize(MENU_ITEM_IMAGE_DIMENSIONS)
            else:
                image = uploaded_image
            return image
        elif is_profile_image:
            if image_dimensions != PROFILE_IMAGE_DIMENSIONS:
                image = uploaded_image.resize(PROFILE_IMAGE_DIMENSIONS)
            else:
                image = uploaded_image
            return image
        elif is_menu_image:
            if image_dimensions != MENU_IMAGE_DIMENSIONS:
                image = uploaded_image.resize(MENU_IMAGE_DIMENSIONS)
            else:
                image = uploaded_image
            return image

    @staticmethod
    def upload_image(image, image_name, image_path):
        """
        Uploads image into specified directory

        :param Image image: image
        :param str image_name: image name
        :param str image_path: image path
        """
        image_location = 'uploads/{image_path}/{image_name}'.format(image_path=image_path, image_name=image_name)
        if not os.path.isdir(image_path):
            os.makedirs(image_path)
        image.save(image_location)

    @classmethod
    def capitalize_string(cls, string):
        string_parts = string.split(' ')
        capitalized_string_parts = [string_part.capitalize() for string_part in string_parts]
        capitalized_string = " ".join(capitalized_string_parts)
        return capitalized_string

    @staticmethod
    def remove_file(file_path, file_name):
        """
        Removes file

        :param str file_path: file path
        :param str file_name: file name
        """
        if os.path.exists(file_path):
            os.remove('{file_path}/{file_name}'.format(file_path=file_path, file_name=file_name))

    @classmethod
    def get_location_id(cls, latitude, longitude):
        """
        Gets location id of working location from user lat & lng

        :param float latitude: latitude
        :param float longitude: longitude
        :rtype int
        :return: location id
        """
        locations_boundries_data = Location.get_locations_boundries()
        for location_boundry_data in locations_boundries_data:
            location_polygon_data = location_boundry_data.get('boundry')
            user_location = Point(longitude, latitude)
            location_polygon = wkt.loads(location_polygon_data)
            if location_polygon.contains(user_location):
                return location_boundry_data.get('id')
        return 0

    @staticmethod
    def sort_list_data(data, key, descending=False):
        """
        Sorts list of dictionaries data according to the key

        :param list data: data
        :param str key: sorting key
        :param bool descending: descending order
        :rtype list
        :return: sorted data
        """
        data.sort(key=itemgetter(key), reverse=descending)
        return data

    @staticmethod
    def send_push_notification(notifications_token, message, data=None):
        """
        Sends push notification

        :param str notifications_token: notifications token
        :param str message: push notification message
        :param list data: push notification data
        """
        try:
            PushClient().publish(PushMessage(to=notifications_token, body=message, data=data))
        except PushServerError:
            pass

    @staticmethod
    def calculate_delivery_time_and_distance(
            latitude, longitude, merchant_latitude, merchant_longitude, is_delivery=False
    ):
        """
        Calculates delivery time along with unit

        :param float latitude: buyer latitude
        :param float longitude: buyer longitude
        :param float merchant_latitude: merchant latitude
        :param float merchant_longitude: merchant longitude
        :param bool is_delivery: delivery flag

        :rtype str
        :returns delivery time with unit
        """
        merchant_location = (merchant_latitude, merchant_longitude)
        buyer_location = (latitude, longitude)
        distance = geopy.distance.vincenty(merchant_location, buyer_location).km
        if is_delivery:
            delivery_time = round(distance + AVERAGE_PREPARATION_TIME + BUFFER_TIME)
            if delivery_time <= 60:
                delivery_time_with_unit = '{} MIN'.format(delivery_time)
            else:
                delivery_time_hours = delivery_time // 60
                delivery_time_minutes = delivery_time % 60
                delivery_time_with_unit = '{hours} HRS {minutes} MIN'.format(
                    hours=delivery_time_hours, minutes=delivery_time_minutes
                )
            return delivery_time_with_unit
        else:
            distance_unit = 'km'
            if not distance >= 1:
                distance = distance * 1000
                distance_unit = 'm'
            distance = round(distance, 2)
            distance_with_unit = '{distance} {unit}'.format(
                distance=distance, unit=distance_unit
            )
            return distance_with_unit
