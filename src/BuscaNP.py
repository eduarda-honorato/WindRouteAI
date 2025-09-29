from collections import deque
from src.Node import Node

class buscaNP(object):
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRAFO
    #--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
  
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
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibirCaminho1(self,encontro,visitado1, visitado2):
        # nó do lado do início
        encontro1 = visitado1[encontro]  
        # nó do lado do objetivo
        encontro2 = visitado2[encontro]
    
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
    
        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))
    
        return caminho1 + caminho2

    #--------------------------------------------------------------------------
    # BUSCA EM AMPLITUDE
    #--------------------------------------------------------------------------
    def amplitude(self,inicio,fim,nos,grafo):   # grafo
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {inicio: raiz}           # grafo
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.popleft()
    
            # Gera sucessores a partir do grafo
            ind = nos.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind, grafo, 1) # grafo
          
            for novo in filhos:
                if novo not in visitado:   # grafo
                    
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    
                    # Verifica se encontrou o objetivo
                    if novo == fim:        # grafo
                    
                        return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE
    #--------------------------------------------------------------------------
    def profundidade(self, inicio, fim, nos, grafo):
    #def profundidade(self,inicio,fim,nx,ny,mapa):
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {inicio: raiz}           # grafo
        
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.pop()
    
            # Gera sucessores a partir do grafo
            ind = nos.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind,grafo,-1) # grafo
            
            for novo in filhos:
                if novo not in visitado:   # grafo
                    
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    
                    # Verifica se encontrou o objetivo
                    if novo == fim:        # grafo
                    
                        return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE LIMITADA
    #--------------------------------------------------------------------------
    def prof_limitada(self,inicio,fim,nos,grafo,lim):
    #def prof_limitada(self,inicio,fim,nx,ny,mapa,lim):
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {inicio: raiz}           # grafo
        
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.pop()
            
            if atual.v1<lim:
                # Gera sucessores a partir do grafo
                ind = nos.index(atual.estado)    # grafo
                filhos = self.sucessores_grafo(ind,grafo,-1) # grafo
                
                for novo in filhos:
                    if novo not in visitado:   # grafo
                        
                        filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                        fila.append(filho)
                        visitado[novo] = filho   # grafo
                        
                        
                        # Verifica se encontrou o objetivo
                        if novo == fim:        # grafo
                        
                            return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------
    # BUSCA EM APROFUNDAMENTO ITERATIVO
    #--------------------------------------------------------------------------
    def aprof_iterativo(self,inicio,fim,nos,grafo,lim_max):
    #def aprof_iterativo(self,inicio,fim,nx,ny,mapa,lim_max):
        for lim in range(1,lim_max):
            # Finaliza se início for igual a objetivo
            if inicio == fim:
                return [inicio]
            
            #transforma em tupla
            
            # Lista para árvore de busca - FILA
            fila = deque()
            # Inclui início como nó raíz da árvore de busca
            raiz = Node(None,inicio,0,None,None)    # grafo
            fila.append(raiz)
        
            # Marca início como visitado
            visitado = {inicio: raiz}           # grafo
            
            while fila:
                # Remove o primeiro da FILA
                atual = fila.pop()
                
                if atual.v1<lim:
                    # Gera sucessores a partir do grafo
                    ind = nos.index(atual.estado)    # grafo
                    filhos = self.sucessores_grafo(ind,grafo,-1) # grafo
                    
                    for novo in filhos:
                        
                        
                        if novo not in visitado:   # grafo
                            
                            filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                            fila.append(filho)
                            visitado[novo] = filho   # grafo
                            
                            
                            # Verifica se encontrou o objetivo
                            if novo == fim:        # grafo
                            
                                return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA BIDIRECIONAL
    #--------------------------------------------------------------------------
    def bidirecional(self, inicio, fim, nos, grafo):
        if inicio == fim:
            return [inicio]


        # Lista para árvore de busca a partir da origem - FILA
        fila1 = deque()
        
        # Lista para árvore de busca a partir do destino - FILA
        fila2 = deque()  
        
        # Inclui início e fim como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        fila1.append(raiz)
        raiz = Node(None,fim,0,None,None)    # grafo
        fila2.append(raiz)
    
        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {inicio: fila1[0]}
        visitado2 = {fim:    fila2[0]}
        
        nivel = 0
    
        while fila1 and fila2:
            
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(fila1)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila1.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado1:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado1[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado2:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila1.append(filho)
            
            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(fila2)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila2.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
        
                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila2.append(filho)
        return None