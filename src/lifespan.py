from fastapi import FastAPI
from contextlib import asynccontextmanager
from data import setup_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    https://fastapi.tiangolo.com/advanced/events/
    Adicionar aqui tudo que a aplicação precisa executar antes de inicializar.
    Isso significa que tudo que for chamado antes do "yield" vai ser executado apenas uma (1) única antes da aplicação começar a receber requisições!

    Da docs:
    This can be very useful for setting up resources that you need to use for the whole app, and that are shared among requests, and/or that you need to clean up afterwards
    '''
    app.state.db = setup_db()
    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''
    app.state.uow.closeall()
