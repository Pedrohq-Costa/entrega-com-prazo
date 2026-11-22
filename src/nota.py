from datetime import datetime
from math import ceil
from typing import TypedDict


class Entrega(TypedDict):
    id: str
    entregue_em: datetime


ResultadoNota = tuple[
    int | float,
    datetime,
    Entrega,
    bool,
    datetime | None,
    str,
    str,
    str,
    str,
]


def calcular_nota_final(
    nota: int | float,
    prazo: datetime,
    entrega: Entrega,
    justificativa_aprovada: bool,
    novo_prazo: datetime | None,
    nome: str,
    ra: str,
    curso: str,
    descricao: str,
) -> ResultadoNota:
    """Calcula a nota e devolve a nota final junto aos dados da entrega.

    Cada dia iniciado de atraso desconta 10% da nota original, ate o limite
    de 50%. Apos cinco dias, a entrega exige justificativa aprovada. Um novo
    prazo autorizado aceita a entrega ate esse momento, sem desconto.
    """
    entregue_em = entrega["entregue_em"]

    if entregue_em <= prazo or (novo_prazo is not None and entregue_em <= novo_prazo):
        nota_final = nota
    else:
        atraso = entregue_em - prazo
        dias_atraso = ceil(atraso.total_seconds() / 86_400)
        if dias_atraso > 5 and not justificativa_aprovada:
            raise ValueError("Entrega apos cinco dias de atraso sem justificativa aprovada")

        desconto = min(dias_atraso * 0.10, 0.50)
        nota_final = nota * (1 - desconto)

    return (
        nota_final,
        prazo,
        entrega,
        justificativa_aprovada,
        novo_prazo,
        nome,
        ra,
        curso,
        descricao,
    )
