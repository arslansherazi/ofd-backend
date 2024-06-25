import io
import os

import boto3
from PIL import Image

from common.constants import (AWS_ACL_PUBLIC_READ, AWS_S3_BUCKET_NAME,
                              AWS_STANDARD_STORAGE_CLASS)
from security.security_credentials import (AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY)


def convert_image_to_bytes(image):
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format='PNG')
    return in_mem_file.getvalue()


def put_s3_object(file, file_name, file_path=None):
    try:
        file_key = file_name
        bucket = AWS_S3_BUCKET_NAME
        client = boto3.client(
            's3', aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_access_key_id=AWS_ACCESS_KEY_ID
        )
        if file_path:
            file_key = '{directory}/{file_name}'.format(directory=file_path, file_name=file_name)
        client.put_object(
            Bucket=bucket, Key=file_key, Body=file, ACL=AWS_ACL_PUBLIC_READ, StorageClass=AWS_STANDARD_STORAGE_CLASS
        )
    except Exception:
        pass


def upload_file(file_path, aws_file_path):
    try:
        for file_name in os.listdir(file_path):
            file_full_path = '{file_path}/{file_name}'.format(file_path=file_path, file_name=file_name)
            file = Image.open(file_full_path)
            file = convert_image_to_bytes(file)
            put_s3_object(
                file=file, file_name=file_name, file_path=aws_file_path
            )
    except Exception:
        pass


if __name__ == '__main__':
    buyers_count = int(input('Enter buyers count::'))  # enter maximum buyer id
    merchants_count = int(input('Enter merchants count::'))  # enter maximum merchant id

    # handle buyers
    for buyer_id in range(buyers_count):
        file_path = '../uploads/buyers/{buyer_id}/profile'.format(buyer_id=buyer_id+1)
        aws_file_path = 'buyers/{buyer_id}/profile'.format(buyer_id=buyer_id+1)
        upload_file(file_path=file_path, aws_file_path=aws_file_path)

    # handle merchants (profile)
    for merchant_id in range(merchants_count):
        file_path = '../uploads/merchants/{merchant_id}/profile'.format(merchant_id=merchant_id+1)
        aws_file_path = 'merchants/{merchant_id}/profile'.format(merchant_id=merchant_id+1)
        upload_file(file_path=file_path, aws_file_path=aws_file_path)

    # handle merchants (menus)
    for merchant_id in range(merchants_count):
        file_path = '../uploads/merchants/{merchant_id}/menus'.format(merchant_id=merchant_id+1)
        aws_file_path = 'merchants/{merchant_id}/menus'.format(merchant_id=merchant_id+1)
        upload_file(file_path=file_path, aws_file_path=aws_file_path)

    # handle merchants (menu items)
    for merchant_id in range(merchants_count):
        menus_path = '../uploads/merchants/{merchant_id}/menus'.format(merchant_id=merchant_id+1)
        try:
            for menu_id in os.listdir(menus_path):
                file_path = '../uploads/merchants/{merchant_id}/menus/{menu_id}'.format(
                    merchant_id=merchant_id + 1, menu_id=menu_id
                )
                aws_file_path = 'merchants/{merchant_id}/menus/{menu_id}'.format(merchant_id=merchant_id+1, menu_id=menu_id)
                upload_file(file_path=file_path, aws_file_path=aws_file_path)
        except Exception:
            pass
