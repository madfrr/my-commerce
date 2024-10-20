from data.repositories.advertising_repo import AdvertisingRepo
from models.advertising import (
    CreateAdvertising,
    CreateAdvertisingResponse,
    AdvertisingDTO,
    ListAdvertisingDTO,
    FilterParams,
    UpdateAdvertising,
)
from exceptions import AdvertisingDoesNotExist


class AdvertisingDomain:
    def __init__(self, repo: AdvertisingRepo, config):
        self.repo: AdvertisingRepo = repo
        self.config = config

    def create(self, advertising: CreateAdvertising) -> CreateAdvertisingResponse:
        id = self.repo.create_advertising(advertising)
        return CreateAdvertisingResponse(id=id)

    def update(self, advertising: UpdateAdvertising):
        return self.repo.update_advertising(advertising)

    def read(self, filter_query: FilterParams) -> ListAdvertisingDTO:
        id = filter_query.id
        user_id = filter_query.user_id
        product_id = filter_query.product_id

        advertisings = self.repo.read_advertising(id, user_id, product_id)
        data = [AdvertisingDTO(**advertising) for advertising in advertisings]
        return ListAdvertisingDTO(data=data)

    def delete(self, id: str):
        advertising = self.repo.read_advertising(id, format_output=True)
        if len(advertising) == 0:
            raise AdvertisingDoesNotExist()

        id = advertising[0].get("id")
        return self.repo.delete_advertising(id)
