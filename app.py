from flask import Flask, render_template, request, jsonify
from src.BuscaNP import buscaNP

app = Flask(__name__)

buscador = buscaNP()

nos = [f"T{i}" for i in range(1, 21)]
grafo = [
    ["T2", "T5"],          # T1 conecta com T2 e T5
    ["T1", "T3", "T6"],    # T2 conecta com T1, T3, T6
    ["T2", "T4", "T7"],    # T3 conecta com T2, T4, T7
    ["T3", "T8"],          # T4 conecta com T3, T8
    ["T1", "T6", "T9"],    # T5 conecta com T1, T6, T9
    ["T2", "T5", "T7", "T10"],  # T6 conecta com T2, T5, T7, T10
    ["T3", "T6", "T8", "T11"],  # T7 conecta com T3, T6, T8, T11
    ["T4", "T7", "T12"],   # T8 conecta com T4, T7, T12
    ["T5", "T10", "T13"],  # T9 conecta com T5, T10, T13
    ["T6", "T9", "T11", "T14"], # T10 conecta com T6, T9, T11, T14
    ["T7", "T10", "T12", "T15"],# T11 conecta com T7, T10, T12, T15
    ["T8", "T11", "T16"],  # T12 conecta com T8, T11, T16
    ["T9", "T14", "T17"],  # T13 conecta com T9, T14, T17
    ["T10", "T13", "T15", "T18"], # T14 conecta com T10, T13, T15, T18
    ["T11", "T14", "T16", "T19"], # T15 conecta com T11, T14, T16, T19
    ["T12", "T15", "T20"], # T16 conecta com T12, T15, T20
    ["T13", "T18"],        # T17 conecta com T13, T18
    ["T14", "T17", "T19"], # T18 conecta com T14, T17, T19
    ["T15", "T18", "T20"], # T19 conecta com T15, T18, T20
    ["T16", "T19"]         # T20 conecta com T16, T19
]

@app.route("/health")
def health_check():
    return "<p>Health Check OK!</p>"

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/methods/bnp")
def algoritmos_bnp():
    return render_template("algoritmos_bnp.html")

@app.route("/graph")
def graph():
    return render_template("graph.html")

@app.route("/search", methods=["POST"])
def search():
    data: dict = request.get_json() 
    if not data: 
        return jsonify({"error": "No data provided"}), 400
    
    inicio = data.get("inicio")
    objetivo = data.get("objetivo")
    metodo = data.get("metodo")

    if not inicio or not objetivo:
        return jsonify({"error": "Campos início e objetivo são obrigatórios"}), 400

    if inicio not in nos or objetivo not in nos:
        return jsonify({"error": "Nó inválido"}), 400

    # método
    if metodo == "rapido":
        caminho = buscador.amplitude(inicio, objetivo, nos, grafo)
    elif metodo == "economico":
        caminho = buscador.profundidade(inicio, objetivo, nos, grafo)
    elif metodo == "panoramico":
        caminho = buscador.prof_limitada(inicio, objetivo, nos, grafo, lim=3)
    elif metodo == "evitar-pedagios":
        caminho = buscador.aprof_iterativo(inicio, objetivo, nos, grafo, lim_max=5)
    else:
        caminho = buscador.bidirecional(inicio, objetivo, nos, grafo)

    return jsonify({
        "caminho": caminho if caminho else [],
        "nos": nos,
        "grafo": grafo
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)