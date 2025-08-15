def calcular_risco(tamanho_terra, historico_pagamentos, dividas_ativas, producao_anual, tipo_cultura):
    """
    Calcula um score de risco baseado em parâmetros agrícolas e financeiros.
    """

    # Peso dos fatores (exemplo simples, pode ser refinado com ML)
    peso_tamanho_terra = 0.2
    peso_historico = 0.3
    peso_dividas = 0.3
    peso_producao = 0.2

    # Normalização de dados (escala 0-1)
    score_terra = min(tamanho_terra / 100, 1)
    score_historico = historico_pagamentos / 100  # percentual
    score_dividas = 1 - min(dividas_ativas / 10000, 1)  # menos dívida = mais score
    score_producao = min(producao_anual / 10000, 1)

    # Ajuste por tipo de cultura (exemplo fictício)
    fator_cultura = {
        "milho": 1.0,
        "arroz": 0.9,
        "feijao": 0.8,
        "cana_de_acucar": 0.85
    }.get(tipo_cultura.lower(), 0.75)

    # Cálculo do score final
    score_final = (
        (score_terra * peso_tamanho_terra) +
        (score_historico * peso_historico) +
        (score_dividas * peso_dividas) +
        (score_producao * peso_producao)
    ) * fator_cultura

    # Classificação de risco
    if score_final >= 0.75:
        classificacao = "Baixo"
    elif score_final >= 0.5:
        classificacao = "Médio"
    else:
        classificacao = "Alto"

    return {
        "score": round(score_final, 2),
        "classificacao": classificacao
    }
