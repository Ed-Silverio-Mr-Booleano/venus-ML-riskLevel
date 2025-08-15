from flask import Flask, request, jsonify
from services.risk_service import calcular_risco

app = Flask(__name__)

@app.route("/api/risco", methods=["POST"])
def estimar_risco():
    try:
        dados = request.get_json()

        # Validação simples
        campos_obrigatorios = ["tamanho_terra", "historico_pagamentos", "dividas_ativas", "producao_anual", "tipo_cultura"]
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

        resultado = calcular_risco(
            tamanho_terra=dados["tamanho_terra"],
            historico_pagamentos=dados["historico_pagamentos"],
            dividas_ativas=dados["dividas_ativas"],
            producao_anual=dados["producao_anual"],
            tipo_cultura=dados["tipo_cultura"]
        )

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
