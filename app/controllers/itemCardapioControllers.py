from entidades.ItemCardapio import ItemCardapio
from DB.db import Database

database = Database()

def verificarItem(item: ItemCardapio):
    if item.preco < 0:
        raise ValueError("O preço não pode ser menor que zero")

    if len(item.nome) <= 5:
        raise ValueError("O nome deve ter no minimo 5 caracteres")

    if len(item.descricao) <= 10:
        raise ValueError("A descrição deve ter no minimo 10 caracteres")

def salvarItem(item: ItemCardapio):
    id = next(database.next_index())
    database.insert(id, item)

def getAllItem():
    return database.getData()