from flask import Flask, render_template, request, jsonify
from src.BuscaNP import buscaNP
from src.BuscaP import busca

app = Flask(__name__)

buscadorNP = buscaNP()
buscadorP = busca()

nos = [f"T{i}" for i in range(1, 21)]

grafo = [
    ["T2", "T6", "T14"],                #T1     
    ["T1", "T3", "T5"],                 #T2         
    ["T2", "T4", "T8"],                 #T3             
    ["T3"],                             #T4              
    ["T2", "T18"],                      #T5   
    ["T1", "T7", "T10", "T12", "T17"],  #T6    
    ["T6", "T14"],                      #T7  
    ["T3", "T9"],                       #T8
    ["T8", "T13", "T16", "T19"],        #T9 
    ["T6", "T12", "T16"],               #T10 
    ["T13", "T16"],                     #T11          
    ["T6", "T10"],                      #T12          
    ["T9", "T11"],                      #T13            
    ["T1", "T7", "T15"],                #T14                  
    ["T14", "T20"],                     #T15         
    ["T9", "T10", "T11"],               #T16           
    ["T6"],                             #T17                
    ["T5"],                             #T18                     
    ["T9"],                             #T19                    
    ["T15"]                             #T20                     
]

grafo_com_pesos = [
    [["T2", 221], ["T6", 187], ["T14", 101]],                # T1
    [["T1", 143], ["T3", 194], ["T5", 178]],                 # T2
    [["T2", 202], ["T4", 97], ["T8", 249]],                  # T3
    [["T3", 81]],                                            # T4
    [["T2", 134], ["T18", 240]],                             # T5
    [["T1", 109], ["T7", 173], ["T10", 145], ["T12", 211], ["T17", 118]],  # T6
    [["T6", 206], ["T14", 132]],                             # T7
    [["T3", 245], ["T9", 230]],                              # T8
    [["T8", 126], ["T13", 140], ["T16", 213], ["T19", 163]], # T9
    [["T6", 200], ["T12", 180], ["T16", 82]],                # T10
    [["T13", 189], ["T16", 156]],                            # T11
    [["T6", 208], ["T10", 247]],                             # T12
    [["T9", 92], ["T11", 177]],                              # T13
    [["T1", 150], ["T7", 94], ["T15", 224]],                 # T14
    [["T14", 242], ["T20", 191]],                            # T15
    [["T9", 171], ["T10", 120], ["T11", 86]],                # T16
    [["T6", 138]],                                           # T17
    [["T5", 160]],                                           # T18
    [["T9", 232]],                                           # T19
    [["T15", 217]]                                           # T20
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

@app.route("/methods/bp")
def methods_bp():
    return render_template("algoritmos_bp.html", nos=nos) ########

@app.route("/graph-data-bnp")
def graph_data_bnp():
    return jsonify({
        "nos": nos,
        "grafo": grafo,
        "posicoes": posicoes_nos
    })

@app.route("/graph-data-bp")
def graph_data_bp():
    return jsonify({
        "nos": nos,
        "grafo_com_pesos": grafo_com_pesos,
        "posicoes": posicoes_nos
    })

@app.route("/search/bnp", methods=["POST"])
def search_bnp():
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
        caminho = buscadorNP.amplitude(inicio, objetivo, nos, grafo)
    elif metodo == "profundidade":
        caminho = buscadorNP.profundidade(inicio, objetivo, nos, grafo)
    elif metodo == "profundidade-limitada":
        caminho = buscadorNP.prof_limitada(inicio, objetivo, nos, grafo, lim=6)
    elif metodo == "aprofundamento-iterativo":
        caminho = buscadorNP.aprof_iterativo(inicio, objetivo, nos, grafo, lim_max=9)
    else:
        caminho = buscadorNP.bidirecional(inicio, objetivo, nos, grafo)

    custo = len(caminho) - 1 if caminho and len(caminho) > 1 else 0

    return jsonify({
        "caminho": caminho if caminho else [],
        "custo": custo,
        "nos": nos,
        "grafo": grafo,
        "posicoes": posicoes_nos
    })

@app.route("/search/bp", methods=["POST"])
def search_bp():
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

    if metodo == "custo-uniforme":
        caminho = buscadorP.custo_uniforme(inicio, objetivo, nos, grafo_com_pesos)
    elif metodo == "greedy":
        caminho = buscadorP.greedy(inicio, objetivo, nos, grafo_com_pesos)
    elif metodo == "a-estrela":
        caminho = buscadorP.a_estrela(inicio, objetivo, nos, grafo_com_pesos)
    else:
        caminho = buscadorP.aia_estrela(inicio, objetivo, nos, grafo_com_pesos)

    custo = len(caminho) - 1 if caminho and len(caminho) > 1 else 0

    return jsonify({
        "caminho": caminho if caminho else [],
        "custo": custo,
        "nos": nos,
        "grafo": grafo_com_pesos,
        "posicoes": posicoes_nos
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)