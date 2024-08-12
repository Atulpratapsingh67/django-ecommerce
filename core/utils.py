import io
import mimetypes
import os
import posixpath
import tempfile
import threading
import warnings
from datetime import datetime
from datetime import timedelta
from urllib.parse import urlencode

from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import SuspiciousOperation
from django.core.files.base import File
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from django.utils.timezone import make_naive

from storages.base import BaseStorage
from storages.compress import CompressedFileMixin
from storages.compress import CompressStorageMixin
from storages.utils import ReadBytesWrapper
from storages.utils import check_location
from storages.utils import clean_name
from storages.utils import is_seekable
from storages.utils import lookup_env
from storages.utils import safe_join
from storages.utils import setting
from storages.utils import to_bytes


from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    print('yes')
    location = settings.AWS_MEDIA_LOCATION
    file_overwrite = False


    def _save(self, name, content):
        cleaned_name = clean_name(name)
        name = self._normalize_name(cleaned_name)
        params = self._get_write_parameters(name, content)

        if is_seekable(content):
            content.seek(0, os.SEEK_SET)

        # wrap content so read() always returns bytes. This is required for passing it
        # to obj.upload_fileobj() or self._compress_content()
        content = ReadBytesWrapper(content)

        if (
            self.gzip
            and params["ContentType"] in self.gzip_content_types
            and "ContentEncoding" not in params
        ):
            content = self._compress_content(content)
            params["ContentEncoding"] = "gzip"

        obj = self.bucket.Object(name)

        # Workaround file being closed errantly see: https://github.com/boto/s3transfer/issues/80
        original_close = content.close
        content.close = lambda: None
        # try:
        a = obj.upload_fileobj(content, ExtraArgs=params, Config=self.transfer_config)
        # finally:
        #     content.close = original_close
        print(a)
        return cleaned_name
