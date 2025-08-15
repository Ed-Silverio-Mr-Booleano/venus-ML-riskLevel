from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder
import numpy as np

class RiscoCreditoAgricolaService:
    def __init__(self, historico):
        self.historico = historico
        self.model = CategoricalNB()
        
        # LabelEncoders para transformar texto em número
        self.le_cultivo = LabelEncoder()
        self.le_epoca = LabelEncoder()
        self.le_garantia = LabelEncoder()
        self.le_pagou = LabelEncoder()

        self.treinar_modelo()

    def treinar_modelo(self):
        # Separar colunas
        cultivos = [d["cultivo"] for d in self.historico]
        epocas = [d["epoca"] for d in self.historico]
        garantias = [d["garantia"] for d in self.historico]
        pagou = [d["pagou"] for d in self.historico]

        # Codificar em números
        X = np.array(list(zip(
            self.le_cultivo.fit_transform(cultivos),
            self.le_epoca.fit_transform(epocas),
            self.le_garantia.fit_transform(garantias)
        )))
        y = self.le_pagou.fit_transform(pagou)

        # Treinar Naive Bayes
        self.model.fit(X, y)

    def estimar_risco(self, cultivo, epoca, garantia):
        # Transformar entrada em números
        entrada = np.array([[ 
            self.le_cultivo.transform([cultivo])[0],
            self.le_epoca.transform([epoca])[0],
            self.le_garantia.transform([garantia])[0]
        ]])

        # Previsão
        probas = self.model.predict_proba(entrada)[0]  # [prob_nao_pagar, prob_pagar]
        risco_nao_pagar = probas[self.le_pagou.transform(["Não"])[0]] * 100

        # Classificação simples
        if risco_nao_pagar < 30:
            classificacao = "Baixo Risco"
        elif risco_nao_pagar < 60:
            classificacao = "Risco Médio"
        else:
            classificacao = "Alto Risco"

        return {
            "cultivo": cultivo,
            "epoca": epoca,
            "garantia": garantia,
            "probabilidade_nao_pagar": round(risco_nao_pagar, 2),
            "classificacao": classificacao
        }

# =============================
# Exemplo de uso do serviço
# =============================
if __name__ == "__main__":
    historico = [
        {"cultivo": "Milho", "epoca": "Chuva", "garantia": "Terreno", "pagou": "Sim"},
        {"cultivo": "Café", "epoca": "Seca", "garantia": "Gado", "pagou": "Não"},
        {"cultivo": "Feijão", "epoca": "Colheita", "garantia": "Sem garantia", "pagou": "Não"},
        {"cultivo": "Milho", "epoca": "Seca", "garantia": "Máquinas", "pagou": "Sim"},
        {"cultivo": "Milho", "epoca": "Chuva", "garantia": "Sem garantia", "pagou": "Não"},
        {"cultivo": "Café", "epoca": "Chuva", "garantia": "Terreno", "pagou": "Sim"},
        {"cultivo": "Feijão", "epoca": "Seca", "garantia": "Terreno", "pagou": "Sim"},
        {"cultivo": "Milho", "epoca": "Colheita", "garantia": "Gado", "pagou": "Não"},
    ]

    service = RiscoCreditoAgricolaService(historico)

    exemplo = service.estimar_risco("Café", "Seca", "Gado")
    print(exemplo)
