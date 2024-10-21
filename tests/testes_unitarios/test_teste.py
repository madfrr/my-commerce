from models.product import CreateProductResponse, CreateProduct
from domain.product import ProductDomain
from data.repositories.product_repo import ProductRepo
from data.repositories.file_repo import FileRepo
from unittest.mock import MagicMock


def test_create_product(mocker):
    product_repo = ProductRepo(db=None)
    file_repo = FileRepo(bucket_name=None)

    novo_id = 42

    file_exists_mock: MagicMock = mocker.patch.object(file_repo, "file_exists", return_value=True)
    create_product_mock: MagicMock = mocker.patch.object(product_repo, "create_product", return_value=novo_id)

    payload = CreateProduct(
        **{"name": "produto_1", "description": "meu primeiro produto", "pictures": ["www.google.com"]}
    )

    product = ProductDomain(product_repo=product_repo, file_repo=file_repo, config=None).create(payload)

    assert file_exists_mock.call_count == 1
    assert file_exists_mock.call_args[0][0] == "www.google.com"
    assert create_product_mock.call_count == 1
    assert create_product_mock.call_args[0][0] == payload
    assert product.id == novo_id
    assert isinstance(product, CreateProductResponse)
