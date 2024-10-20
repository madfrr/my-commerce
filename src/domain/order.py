from data.repositories.order_repo import OrderRepo
from models.order import CreateOrder, CreateOrderResponse, OrderDTO, ListOrderDTO, FilterParams, UpdateOrder
from exceptions import OrderDoesNotExist

class OrderDomain:
    def __init__(self, repo:OrderRepo, config):
        self.repo:OrderRepo = repo
        self.config = config

    def create(self, order: CreateOrder) -> CreateOrderResponse:  
        id = self.repo.create_order(order)
        return CreateOrderResponse(id=id)
    
    def update(self, order: UpdateOrder):
        return self.repo.update_order(order)
        
    def read(self, filter_query: FilterParams) -> ListOrderDTO:
        id = filter_query.id
        transaction_id = filter_query.transaction_id
        advertising_id = filter_query.advertising_id
        
        orders = self.repo.read_order(id, transaction_id, advertising_id)
        data = [OrderDTO(**order) for order in orders]
        return ListOrderDTO(data=data)
    
    def delete(self, id: str):
        order = self.repo.read_order(id, format_output=True)
        if len(order) == 0:
            raise OrderDoesNotExist()
        
        id = order[0].get("id")
        return self.repo.delete_order(id)