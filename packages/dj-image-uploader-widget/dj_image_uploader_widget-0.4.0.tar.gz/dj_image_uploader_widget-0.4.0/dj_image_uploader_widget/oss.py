from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.exceptions import ImproperlyConfigured
import oss2
from .defaults import get_oss_config


def get_oss_config():
    return getattr(
        settings,
        "DJ_IMAGE_UPLOADER_OSS_CONFIG",
        {
            "ACCESS_KEY_ID": "your_key_id",
            "ACCESS_KEY_SECRET": "your_secret",
            "ENDPOINT": "oss-cn-beijing.aliyuncs.com",
            "BUCKET_NAME": "your_bucket",
            "BASE_PATH": "uploads/",
        },
    )


def upload_to_oss(file_obj, user_id=None):
    config = get_oss_config()

    try:
        auth = oss2.Auth(config["ACCESS_KEY_ID"], config["ACCESS_KEY_SECRET"])
        bucket = oss2.Bucket(auth, config["ENDPOINT"], config["BUCKET_NAME"])

        filename = f"{config['BASE_PATH']}{user_id}_{file_obj.name}"
        bucket.put_object(filename, file_obj)
        return f"https://{config['BUCKET_NAME']}.{config['ENDPOINT']}/{filename}"
    except KeyError as e:
        raise ImproperlyConfigured(f"Missing OSS config: {e}")
