from flask import Flask, render_template, request, jsonify
from src.BuscaNP import buscaNP

app = Flask(__name__)

buscador = buscaNP()

nos = [f"T{i}" for i in range(1, 21)]

grafo = [
    ["T2", "T6", "T14"],             
    ["T1", "T3", "T5", "T6"],              
    ["T2", "T4", "T8"],              
    ["T3"],                          
    ["T2", "T18"],                   
    ["T1", "T2", "T7", "T10", "T12", "T17"],      
    ["T6", "T14"],                   
    ["T3", "T9"],                    
    ["T8", "T13", "T16", "T19"],     
    ["T6", "T12", "T16"],     
    ["T13", "T16"],           
    ["T6", "T10"],                          
    ["T9", "T11"],                   
    ["T1", "T7", "T15"],                   
    ["T14", "T20"],            
    ["T9", "T10", "T11"],            
    ["T6"],                         
    ["T5"],                          
    ["T9"],                          
    ["T15"]                          
]


posicoes_nos = {
    "T1": {"x": -300, "y": -150},    
    "T2": {"x": -100, "y": -150},    
    "T3": {"x": 100, "y": -150},     
    "T4": {"x": 250, "y": -200},     
    "T5": {"x": -100, "y": -250},      
    "T6": {"x": -150, "y": 0},       
    "T7": {"x": -300, "y": 100},     
    "T8": {"x": 300, "y": -80},       
    "T9": {"x": 300, "y": 50},      
    "T10": {"x": 0, "y": 100},       
    "T11": {"x": 100, "y": 250},     
    "T12": {"x": 80, "y": 0},       
    "T13": {"x": 300, "y": 200},     
    "T14": {"x": -420, "y": 0},      
    "T15": {"x": -550, "y": 100},    
    "T16": {"x": 150, "y": 100},     
    "T17": {"x": -150, "y": 250},       
    "T18": {"x": -350, "y": -300},     
    "T19": {"x": 450, "y": 50},     
    "T20": {"x": -500, "y": 250}     
}

@app.route("/health")
def health_check():
    return "<p>Health Check OK!</p>"

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/methods/bnp")
def methods_bnp():
    return render_template("algoritmos_bnp.html", nos=nos)

@app.route("/graph-data")
def graph_data():
    return jsonify({
        "nos": nos,
        "grafo": grafo,
        "posicoes": posicoes_nos
    })

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

    if metodo == "amplitude":
        caminho = buscador.amplitude(inicio, objetivo, nos, grafo)
    elif metodo == "profundidade":
        caminho = buscador.profundidade(inicio, objetivo, nos, grafo)
    elif metodo == "profundidade-limitada":
        caminho = buscador.prof_limitada(inicio, objetivo, nos, grafo, lim=6)
    elif metodo == "aprofundamento-iterativo":
        caminho = buscador.aprof_iterativo(inicio, objetivo, nos, grafo, lim_max=10)
    else:
        caminho = buscador.bidirecional(inicio, objetivo, nos, grafo)

    # Calcula o custo do caminho (número de passos)
    custo = len(caminho) - 1 if caminho and len(caminho) > 1 else 0

    return jsonify({
        "caminho": caminho if caminho else [],
        "custo": custo,
        "nos": nos,
        "grafo": grafo,
        "posicoes": posicoes_nos
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)