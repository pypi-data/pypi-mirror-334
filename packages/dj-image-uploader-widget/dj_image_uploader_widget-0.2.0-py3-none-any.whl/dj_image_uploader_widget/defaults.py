from django.conf import settings


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
