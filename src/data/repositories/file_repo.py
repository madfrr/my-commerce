from google.cloud import storage


class FileRepo:
    def __init__(self, bucket_name: str):
        '''
        Obs.: Poderia criar um serviço do storage para centralizar toda interação com bucket, porém, dada simplicidade do problema, essa classe já está fazendo esse papel. Isso é útil caso seja necessário alterar a lib ou alterar provedor de cloud por exemplo.
        '''
        self.storage = storage.Client()
        self.bucket_name = bucket_name

    def save_picture(
            self,
            file, 
            file_name: str, 
            content_type: str
        ):
        bucket = self.storage.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(file, content_type=content_type)

        link = blob.path_helper(self.bucket_name, file_name)
        link = 'gs://' + link
        return link
    
    def file_exists(self, file_uri: str):
        file_name = file_uri.split("/")[-1]
        bucket = self.storage.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        return blob.exists()