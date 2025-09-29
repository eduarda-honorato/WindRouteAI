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

    if (!inicio || !objetivo) {
        alert('Por favor, preencha os campos de início e objetivo.');
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
            pathResult.innerHTML = `<p style="color:red;">${data.error}</p>`;
            mapPlaceholder.textContent = 'Erro ao calcular rota.';
            return;
        }

        document.getElementById('pathResult').textContent =
            "Caminho: " + data.caminho.join(" → ");

        desenharGrafo(data.nos, data.grafo, data.caminho);
    })
    .catch(err => console.error("Erro:", err));
}

////////////////////////////////////////////////////
let network;
function desenharGrafo(nos, grafo, caminho) {
    const container = document.querySelector(".map-container");

    // cria os nós
    const nodes = new vis.DataSet(nos.map(n => ({ id: n, label: n })));

    // cria as arestas
    const edgesArr = [];
    grafo.forEach((viz, i) => {
        viz.forEach(v => {
            edgesArr.push({ from: nos[i], to: v });
        });
    });
    const edges = new vis.DataSet(edgesArr);

    const data = { nodes, edges };
    const options = {
        nodes: { shape: "dot", size: 20 },
        edges: { color: "gray", arrows: "to" },
        //physics: false
        physics: { stabilization: true }, // Física para organizar melhor
    };

    network = new vis.Network(container, data, options);

    // destaca caminho (se existir)
    if (caminho && caminho.length > 1) {
        for (let i = 0; i < caminho.length - 1; i++) {
            const a = caminho[i], b = caminho[i + 1];
            edges.forEach(edge => {
                if ((edge.from === a && edge.to === b) || (edge.from === b && edge.to === a)) {
                    edges.update({ id: edge.id, color: { color: "green" }, width: 4 });
                }
            });
        }
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
document.addEventListener('DOMContentLoaded', loadTheme);