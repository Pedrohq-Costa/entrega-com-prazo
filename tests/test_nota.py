"""Criterios de aceitacao:

RF-001
Dado uma atividade com prazo ate 25/11/2026 as 23:59 e uma entrega feita
exatamente nesse horario
Quando calcular_nota_final e executada
Entao a entrega e aceita e recebe a nota integral, sem desconto por atraso.

RF-002
Dado uma entrega com seis dias iniciados de atraso e justificativa aprovada
Quando calcular_nota_final e executada
Entao o desconto e limitado a 50% da nota, mesmo quando o calculo bruto o excede.

RF-003
Dado uma entrega feita depois de cinco dias de atraso, sem justificativa aprovada
Quando calcular_nota_final e executada
Entao a entrega e rejeitada com ValueError.

RF-004
Dado uma entrega fora do prazo normal, mas dentro de um novo prazo autorizado
Quando calcular_nota_final e executada
Entao a entrega e aceita conforme a reabertura e recebe a nota integral.

RF-005
Dado uma entrega processada com identificador, momento da entrega e nota original
Quando calcular_nota_final e executada
Entao o retorno disponibiliza a nota final e os dados da entrega; o desconto
aplicado pode ser obtido pela diferenca entre a nota original e a nota final.

Contrato dos testes: calcular_nota_final recebe nota, prazo, entrega
(dicionario com identificador e entregue_em), justificativa_aprovada,
novo_prazo, nome, ra, curso e descricao. Retorna uma tupla com esses campos
nessa ordem, substituindo nota pela nota final.
"""

from datetime import datetime

import pytest

from src.nota import calcular_nota_final


def test_entrega_no_horario_limite_recebe_nota_integral():
    nota = 10
    prazo = datetime(2026, 11, 25, 23, 59)
    entrega = {"id": "entrega-001", "entregue_em": prazo}

    resultado = calcular_nota_final(
        nota, prazo, entrega, False, None, "Ana", "RA001", "Engenharia", "Atividade 1"
    )

    assert resultado == (
        nota,
        prazo,
        entrega,
        False,
        None,
        "Ana",
        "RA001",
        "Engenharia",
        "Atividade 1",
    )


def test_desconto_por_atraso_e_limitado_a_cinquenta_porcento():
    nota = 10
    prazo = datetime(2026, 11, 25, 23, 59)
    entrega = {"id": "entrega-002", "entregue_em": datetime(2026, 12, 1, 23, 59)}

    resultado = calcular_nota_final(
        nota, prazo, entrega, True, None, "Bruno", "RA002", "Engenharia", "Atividade 2"
    )

    assert resultado[0] == 5


def test_entrega_apos_cinco_dias_sem_justificativa_e_rejeitada():
    prazo = datetime(2026, 11, 25, 23, 59)
    entrega = {"id": "entrega-003", "entregue_em": datetime(2026, 12, 1, 23, 59)}

    with pytest.raises(ValueError):
        calcular_nota_final(
            10, prazo, entrega, False, None, "Caio", "RA003", "Engenharia", "Atividade 3"
        )


def test_entrega_dentro_do_novo_prazo_autorizado_recebe_nota_integral():
    nota = 10
    prazo = datetime(2026, 11, 25, 23, 59)
    novo_prazo = datetime(2026, 11, 27, 23, 59)
    entrega = {"id": "entrega-004", "entregue_em": novo_prazo}

    resultado = calcular_nota_final(
        nota,
        prazo,
        entrega,
        True,
        novo_prazo,
        "Diana",
        "RA004",
        "Engenharia",
        "Atividade 4",
    )

    assert resultado[0] == nota


def test_resultado_disponibiliza_dados_da_entrega_e_nota_final():
    nota_original = 10
    prazo = datetime(2026, 11, 25, 23, 59)
    momento_entrega = datetime(2026, 11, 26, 23, 59)
    entrega = {"id": "entrega-005", "entregue_em": momento_entrega}

    resultado = calcular_nota_final(
        nota_original,
        prazo,
        entrega,
        False,
        None,
        "Eva",
        "RA005",
        "Engenharia",
        "Atividade 5",
    )

    assert resultado == (
        9,
        prazo,
        entrega,
        False,
        None,
        "Eva",
        "RA005",
        "Engenharia",
        "Atividade 5",
    )
    assert nota_original - resultado[0] == 1
