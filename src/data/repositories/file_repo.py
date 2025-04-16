from google.cloud import storage


class FileRepo:
    def __init__(self, bucket_name: str, storage_client: storage.Client = None):
        """
        Obs.: Poderia criar um serviço do storage para centralizar toda interação com bucket, porém, dada simplicidade do problema, essa classe já está fazendo esse papel. Isso é útil caso seja necessário alterar a lib ou alterar provedor de cloud por exemplo.
        """
        if storage_client is None:
            storage_client = storage.Client()
        self.storage = storage_client
        self.bucket_name = bucket_name

    def save_picture(self, file, file_name: str, content_type: str):
        bucket = self.storage.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(file, content_type=content_type)

        link = blob.path_helper(self.bucket_name, file_name)
        link = "gs://" + link
        return link

    def file_exists(self, file_uri: str):
        file_name = file_uri.split("/")[-1]
        bucket = self.storage.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        return blob.exists()

    def delete_file(self, file_uri):
        """
        De acordo com a documentação da GCS, a condição de generation_match_precondition serve para evitar condições de corrida. Um exemplo: Pode ser que um usuário esteja querendo deletar um produto enquanto outro estiver realizando leitura.
        """
        file_name = file_uri.split("/")[-1]
        bucket = self.storage.bucket(self.bucket_name)
        blob = bucket.blob(file_name)

        blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
        generation_match_precondition = blob.generation

        return blob.delete(if_generation_match=generation_match_precondition)
