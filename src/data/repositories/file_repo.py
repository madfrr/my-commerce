from google.cloud import storage


class FileRepo:
    def __init__(self):
        self.storage = storage.Client()

    def save_picture(
            self,
            file, 
            file_name: str, 
            bucket_name: str, 
            content_type: str
        ):
        bucket = self.storage.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(file, content_type=content_type)

        link = blob.path_helper(bucket_name, file_name)
        link = 'gs://' + link
        return link