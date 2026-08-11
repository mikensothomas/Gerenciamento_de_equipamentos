from fastapi import APIRouter, Response, status, Query, HTTPException
from DB import db
from typing import Annotated
from entidades.ItemCardapio import ItemCardapio, precoFormatado
from controllers.itemCardapioControllers import verificarItem, salvarItem, getAllItem

itemCardapio_routes = APIRouter(tags=['Cardapio'])
database = db.Database()

@itemCardapio_routes.get("/itens")
def itemCardapio(disponivel: bool = None):    #Precisar ser revisado
    disponiveis = getAllItem()
    resultado = {}
    for index in disponiveis:
        resultado = dict(item=disponiveis[index], precoFormatado=disponiveis[index].precoFormatado())
        return resultado

@itemCardapio_routes.post("/itens", status_code=status.HTTP_201_CREATED)
def cadastroItemCardapio(payload: ItemCardapio):
    try:
        verificarItem(payload)
        salvarItem(payload)
        return Response(status_code=status.HTTP_201_CREATED)
    except ValueError as error:
        raise HTTPException(
            status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= f"{error}"
        )

@itemCardapio_routes.get("/itens/dispo")
def getItensDisponiveis(disponivel : Annotated[bool, Query(description="VAlor de query inválido")]):
    disponiveis = database.getData()

    if disponiveis is None:
        return disponiveis

    retorno = {}

    for item in disponiveis:
        if disponiveis[item]["disponivel"] == disponivel:
            retorno[item]=disponiveis[item]
    return retorno