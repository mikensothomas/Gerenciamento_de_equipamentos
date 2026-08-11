from dataclasses import dataclass
from entidades import ItemCardapio
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@dataclass
class ItemCardapio:
    id: int
    nome: str
    descricao: str
    preco: float
    disponivel: bool

@property
def precoFormatado(item: ItemCardapio):
    return locale.currency(item.preco, symbol=True, grouping=True)