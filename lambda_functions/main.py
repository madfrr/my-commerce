from google.cloud import storage
from os import getenv
import threading


def get_file_index(storage_client, bucket_name, file_name):
    blob_list = storage_client.list_blobs(bucket_name, prefix=file_name)
    max_index = 0
    for blob in blob_list:
        blob_index = blob.name.split(".")[0]
        if "_" in blob_index:
            blob_index = int(blob_index.split("_")[-1])  # se o arquivo for 580_2.jpeg -> 2 é o indice
            max_index = max(max_index, blob_index)

    return max_index + 1


def save_pictures(file, bucket_name: str, file_name: str, file_extension: str, content_type: str):
    storage_client = storage.Client()

    file_index = get_file_index(storage_client, bucket_name, file_name)
    nome_do_arquivo = (
        f"{file_name}_{file_index}.{file_extension}" if file_index != 1 else f"{file_name}.{file_extension}"
    )

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(nome_do_arquivo)
    blob.upload_from_string(file, content_type=content_type)
    return nome_do_arquivo


def data_is_validated(bucket_name, file_name, file_extension, content_type):
    if (
        isinstance(bucket_name, str)
        and isinstance(file_name, str)
        and isinstance(file_extension, str)
        and isinstance(content_type, str)
    ):
        return True
    return False


def main(request):
    token = request.headers.get("token")

    if not token or token != getenv("TOKEN"):
        return {"error": "Unauthorized"}, 401

    bucket_name = request.form.get("bucket_name")
    file_name = request.form.get("file_name")
    file_extension = request.form.get("file_extension")
    content_type = request.form.get("content_type")

    file = dict(request.files).get("file")

    if not data_is_validated(bucket_name, file_name, file_extension, content_type):
        return {
            "error": 'Data is invalid. You have to send "bucket_name", "file_name", "file_extension", "content_type" fields and they must be strings'
        }, 400

    if not file:
        return {"error": "You must send a file"}, 400

    threading.Thread(
        target=save_pictures,
        args=(
            file.read(),
            bucket_name,
            file_name,
            file_extension,
            content_type,
        ),
        daemon=True,
    ).start()

    return {"message": "OK!"}, 201
