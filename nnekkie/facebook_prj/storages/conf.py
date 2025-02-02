from facebook_prj.env import config


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_S3_FILE_OVERWRITE = False


AWS_STORAGE_BUCKET_NAME = 'nnekkie-aws'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_USE_SSL = True



AWS_DEFAULT_ACL = 'public-read'

STORAGES = {
    "default": {
        "BACKEND": "facebook_prj.storages.backends.MediaStorage",
    },
    'staticfiles':{
        "BACKEND": "facebook_prj.storages.backends.StaticStorage",
    }
}