from data.repositories.transaction_repo import TransactionRepo
from models.transaction import CreateTransaction, CreateTransactionResponse, TransactionDTO, ListTransactionDTO, FilterParams


class TransactionDomain:
    def __init__(self, repo:TransactionRepo, config):
        self.repo:TransactionRepo = repo
        self.config = config

    def create(self, transaction: CreateTransaction) -> CreateTransactionResponse:  
        id = self.repo.create_transaction(transaction)
        return CreateTransactionResponse(id=id)
    
    def read(self, filter_query: FilterParams) -> ListTransactionDTO:
        id = filter_query.id
        user_id = filter_query.user_id
        product_id = filter_query.product_id
        
        transactions = self.repo.read_transaction(id, user_id, product_id)
        data = [TransactionDTO(**transaction) for transaction in transactions]
        return ListTransactionDTO(data=data)
