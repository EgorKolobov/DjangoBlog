from storages.backends.s3boto3 import S3Boto3Storage


class ClientDocsStorage(S3Boto3Storage):
    bucket_name = 'egor-django-blog-files'
    file_overwrite = False