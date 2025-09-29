// Função para alternar entre temas
function toggleTheme() {
    const body = document.body;
    const themeText = document.getElementById('theme-text');
    const themeIcon = document.getElementById('theme-icon');

    const isLightMode = body.getAttribute('data-theme') === 'light';

    if (isLightMode) {
        // Mudar para tema escuro
        body.removeAttribute('data-theme');
        if (themeText) themeText.textContent = 'Tema Claro';
        if (themeIcon) themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        // Mudar para tema claro
        body.setAttribute('data-theme', 'light');
        if (themeText) themeText.textContent = 'Tema Escuro';
        if (themeIcon) themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// Carregar tema salvo ao inicializar
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const themeText = document.getElementById('theme-text');
    const themeIcon = document.getElementById('theme-icon');

    if (savedTheme === 'light') {
        body.setAttribute('data-theme', 'light');
        themeText.textContent = 'Tema Escuro';
        themeIcon.textContent = '🌙';
    } else {
        body.removeAttribute('data-theme');
        themeText.textContent = 'Tema Claro';
        themeIcon.textContent = '☀️';
    }
}

function executarRota() {
    const inicio = document.getElementById('inicio').value;
    const objetivo = document.getElementById('objetivo').value;
    const metodo = document.getElementById('metodo').value;

    if (!inicio || !objetivo || !metodo) {
        alert('Por favor, preencha os campos de início, objetivo e método.');
        return;
    }

    document.getElementById('loading').style.display = 'block';
    document.getElementById('pathResult').style.display = 'none';

    fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ inicio, objetivo, metodo })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('pathResult').style.display = 'block';

        if (data.error) {
            document.getElementById('pathResult').innerHTML = `<p style="color:red;">${data.error}</p>`;
            // Mantém o grafo, apenas mostra erro
            return;
        }

        // Exibe o caminho e o custo
        const caminhoTexto = data.caminho.length > 0 ? data.caminho.join(" → ") : "Nenhum caminho encontrado";
        const custoTexto = data.custo > 0 ? `<br><strong>Custo: ${data.custo} passos</strong>` : "";
        
        document.getElementById('pathResult').innerHTML = 
            `<strong>Caminho:</strong> ${caminhoTexto}${custoTexto}`;

        // Atualiza o grafo com o novo caminho
        desenharGrafo(data.nos, data.grafo, data.caminho, data.posicoes);
    })
    .catch(err => console.error("Erro:", err));
}

////////////////////////////////////////////////////
let network;

// Função para criar SVG de turbina eólica
function criarTurbinaSVG(cor = "#97C2FC", corBorda = "#2B7CE9") {
    const svg = '<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">' +
        '<!-- Base da turbina -->' +
        '<line x1="20" y1="35" x2="20" y2="15" stroke="' + corBorda + '" stroke-width="2"/>' +
        '<!-- Centro da turbina -->' +
        '<circle cx="20" cy="15" r="2" fill="' + corBorda + '"/>' +
        '<!-- Pás da turbina -->' +
        '<path d="M20,15 L18,5 Q20,8 22,5 Z" fill="' + cor + '" stroke="' + corBorda + '" stroke-width="1"/>' +
        '<path d="M20,15 L10,18 Q13,20 10,22 Z" fill="' + cor + '" stroke="' + corBorda + '" stroke-width="1"/>' +
        '<path d="M20,15 L30,18 Q27,20 30,22 Z" fill="' + cor + '" stroke="' + corBorda + '" stroke-width="1"/>' +
        '</svg>';
    
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}

function desenharGrafo(nos, grafo, caminho, posicoes) {
    const container = document.querySelector(".map-container");

    // cria os nós com posições fixas usando imagem de turbina
    const nodes = new vis.DataSet(nos.map(n => ({ 
        id: n, 
        label: n,
        x: posicoes[n].x,
        y: posicoes[n].y,
        fixed: true,  // impede que o nó se mova
        shape: "image",
        image: criarTurbinaSVG(),
        size: 30,
        font: {
            size: 12,
            color: "white",
            background: "rgba(0,0,0,0.7)",
            strokeWidth: 1,
            strokeColor: "black"
        }
    })));

    // cria as arestas (evitando duplicatas)
    const edgesArr = [];
    const addedEdges = new Set();
    
    grafo.forEach((viz, i) => {
        viz.forEach(v => {
            const from = nos[i];
            const to = v;
            // Cria uma chave única para a aresta (ordenada para evitar duplicatas)
            const edgeKey = [from, to].sort((a, b) => a.localeCompare(b)).join('-');
            
            if (!addedEdges.has(edgeKey)) {
                edgesArr.push({ from, to });
                addedEdges.add(edgeKey);
            }
        });
    });
    const edges = new vis.DataSet(edgesArr);

    const data = { nodes, edges };
    const options = {
        nodes: { 
            shape: "image", 
            size: 30,
            font: {
                size: 12,
                color: "white",
                background: "rgba(0,0,0,0.7)",
                strokeWidth: 1,
                strokeColor: "black"
            },
            borderWidth: 0
        },
        edges: { 
            color: "gray", 
            arrows: {
                to: {
                    enabled: false  // Remove as setas
                }
            },
            length: 150,
            smooth: {
                enabled: true,
                type: "continuous",
                roundness: 0.1
            }
        },
        physics: false,
        layout: {
            randomSeed: 42  // garante layout consistente
        }
    };

    network = new vis.Network(container, data, options);

    // destaca caminho (se existir)
    if (caminho && caminho.length > 1) {
        for (let i = 0; i < caminho.length - 1; i++) {
            const a = caminho[i], b = caminho[i + 1];
            edges.forEach(edge => {
                if ((edge.from === a && edge.to === b) || (edge.from === b && edge.to === a)) {
                    edges.update({ 
                        id: edge.id, 
                        color: { color: "#00ff00" }, 
                        width: 4
                    });
                }
            });
        }
        
        // Destaca os nós do caminho com turbinas verdes
        caminho.forEach(nodeId => {
            nodes.update({
                id: nodeId,
                image: criarTurbinaSVG("#66ff66", "#00aa00")
            });
        });
    }
}
//

document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
        executarRota();
    }
});

document.querySelectorAll('.input-field, .select-field').forEach(field => {
    field.addEventListener('focus', function () {
        this.parentElement.style.transform = 'scale(1.02)';
    });

    field.addEventListener('blur', function () {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Carregar tema ao inicializar a página
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    carregarGrafoInicial();
});

// Função para carregar o grafo inicial sem caminho
function carregarGrafoInicial() {
    fetch('/graph-data')
    .then(res => res.json())
    .then(data => {
        // Remove o placeholder e desenha o grafo
        const container = document.querySelector(".map-container");
        const placeholder = container.querySelector(".map-placeholder");
        if (placeholder) {
            placeholder.remove();
        }
        
        desenharGrafo(data.nos, data.grafo, [], data.posicoes);
    })
    .catch(err => console.error("Erro ao carregar grafo inicial:", err));
}