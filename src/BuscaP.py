from collections import deque
from src.NodeP import NodeP

class busca(object):
#--------------------------------------------------------------------------
# SUCESSORES PARA GRAFO
#--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    
#--------------------------------------------------------------------------    
# INSERE NA LISTA MANTENDO-A ORDENADA
#--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
#--------------------------------------------------------------------------    
# GERA H DE FORMA ALEATÓRIAv - GRAFO
#--------------------------------------------------------------------------    
    def heuristica_grafo(self,nos,destino,n):
        i_destino = nos.index(destino)
        i_n = nos.index(n)
        h = [
             [0,180,160,200,140,150,120,130,180,160,170,140,150,120,100,170,110,120,160,140],     # T1
             [180,0,150,280,120,200,220,180,280,210,240,180,200,220,180,240,200,160,280,220],     # T2
             [160,150,0,70,280,180,200,220,280,200,220,190,210,200,180,220,180,160,260,200],      # T3
             [200,280,70,0,350,250,270,290,350,270,290,260,280,270,250,290,250,230,330,270],      # T4
             [140,120,280,350,0,250,270,230,320,260,290,230,250,270,230,290,250,130,300,250],     # T5
             [150,200,180,250,250,0,160,200,260,160,200,140,180,160,140,200,110,220,240,180],     # T6
             [120,220,200,270,270,160,0,220,280,180,220,160,200,80,120,220,180,200,260,200],      # T7
             [130,180,220,290,230,200,220,0,190,240,260,230,250,240,220,260,220,200,280,240],     # T8
             [180,280,280,350,320,260,280,190,0,240,200,120,100,300,260,140,240,280,180,260],     # T9
             [160,210,200,270,260,160,180,240,240,0,180,140,160,180,160,100,140,200,220,180],     # T10
             [170,240,220,290,290,200,220,260,200,180,0,160,140,240,220,120,180,240,260,220],     # T11
             [150,180,190,260,230,140,160,230,260,140,160,0,180,180,160,180,160,200,240,180],     # T12
             [150,200,210,280,250,180,200,250,100,160,140,180,0,220,200,160,200,240,200,220],     # T13
             [120,220,200,270,270,160,80,240,300,180,240,180,220,0,120,240,200,220,280,220],      # T14
             [100,180,180,250,230,140,120,220,260,160,220,160,200,120,0,220,180,200,260,80],      # T15
             [170,240,220,290,290,200,220,260,140,100,120,180,160,240,220,0,180,240,260,220],     # T16
             [110,200,180,250,250,110,180,220,240,140,180,160,200,200,180,180,0,240,220,200],     # T17
             [120,160,160,230,130,220,200,200,280,200,240,200,240,220,200,240,240,0,280,240],     # T18
             [160,280,260,330,300,240,260,280,180,220,260,240,200,280,260,260,220,280,0,280],     # T19
             [140,220,200,270,250,180,200,240,260,180,220,180,220,220,80,220,200,240,280,0]       # T20
             ]
        return h[i_destino][i_n]

# -----------------------------------------------------------------------------
# CUSTO UNIFORME
# -----------------------------------------------------------------------------
    def custo_uniforme(self,inicio,fim,nos,grafo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz} # grafo
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores - grafo
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos: # grafo
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 
    
                # Não visitado ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    self.inserir_ordenado(lista, filho)
        return None
# -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self,inicio,fim,nos,grafo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz} # grafo
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores - grafo
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos: # grafo
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grafo(nos,novo[0],fim)  
    
                # Não visitado ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    self.inserir_ordenado(lista, filho)
        return None
# -----------------------------------------------------------------------------
# A ESTRELA
# -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,nos,grafo,):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz} # grafo
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores - grafo
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos: # grafo
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grafo(nos,novo[0],fim)  
    
                # Não visitado ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    self.inserir_ordenado(lista, filho)
        return None
# -----------------------------------------------------------------------------
# AI ESTRELA
# -----------------------------------------------------------------------------       
    def aia_estrela(self,inicio,fim,nos,grafo): # grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        limite = self.heuristica_grafo(nos,inicio,fim) # grafo
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        
        # Busca iterativa
        while True:
            lim_acima = []
            
            raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {inicio: raiz} # grafo
            
            # loop de busca
            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
        
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2
        
                # Gera sucessores - grafo
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
        
                for novo in filhos: # grafo
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grafo(nos,novo[0],fim)   
                
                    # Verifica se está dentro do limite
                    if v1<=limite:
                        # Não visitado ou custo melhor
                        if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                            filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                            visitado[novo[0]] = filho #grafo
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(v1)
            
            limite = sum(lim_acima)/len(lim_acima)
            lista.clear()
            visitado.clear()
            filhos.clear()
                        
        return None
