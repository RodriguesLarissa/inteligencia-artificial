from anytree import Node, RenderTree, PreOrderIter
import copy

estado_inicial = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
estado_final = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
estados_e_valores: dict = {} #tupla_estados: valor_heuristica
nos: list[Node] = []

def movimento(matriz_pai: list[list[int]], x: int, x_destino: int, y: int, y_destino):
    matriz = copy.deepcopy(matriz_pai)

    numero_movido = matriz[x_destino][y_destino]
    matriz[x_destino][y_destino] = 0
    matriz[x][y] = numero_movido
    return matriz

def mover_para_cima(matriz_pai: list[list[int]], x: int, y: int):
    return movimento(matriz_pai, x, x-1, y, y)

def mover_para_baixo(matriz_pai: list[list[int]], x: int, y: int):
    return movimento(matriz_pai, x, x+1, y, y)

def mover_para_direita(matriz_pai: list[list[int]], x: int, y: int):
    return movimento(matriz_pai, x, x, y, y+1)

def mover_para_esquerda(matriz_pai: list[list[int]], x: int, y: int):
    return movimento(matriz_pai, x, x, y, y-1)

def expandir_estados(x: int, y: int, matriz_pai: list[list[int]], no_pai: Node):
    global estados_e_valores
    global nos

    matriz_do_estado: list(list(int))

    #Analisa a opcao de cima
    if x-1 >= 0:
        matriz_do_estado = mover_para_cima(matriz_pai, x, y)
        estado_salvo = tuple(tuple(item) for item in matriz_do_estado)

        if not estado_salvo in estados_e_valores:
            estados_e_valores[estado_salvo] = calcular_heuristica(matriz_do_estado, no_pai)
            nos.append(Node(list(estados_e_valores.items())[-1], parent=no_pai))

    #Analisa a opcao da direita
    if y+1 <= 2:
        matriz_do_estado = mover_para_direita(matriz_pai, x, y)
        estado_salvo = tuple(tuple(item) for item in matriz_do_estado)

        if not estado_salvo in estados_e_valores:
            estados_e_valores[estado_salvo] = calcular_heuristica(matriz_do_estado, no_pai)
            nos.append(Node(list(estados_e_valores.items())[-1], parent=no_pai))

    #Analisa a opcao de baixo
    if x+1 <= 2:
        matriz_do_estado = mover_para_baixo(matriz_pai, x, y)
        estado_salvo = tuple(tuple(item) for item in matriz_do_estado)

        if not estado_salvo in estados_e_valores:
            estados_e_valores[estado_salvo] = calcular_heuristica(matriz_do_estado, no_pai)
            nos.append(Node(list(estados_e_valores.items())[-1], parent=no_pai))

    #Analisa a opcao da esquerda
    if y-1 >= 0:
        matriz_do_estado = mover_para_esquerda(matriz_pai, x, y)
        estado_salvo = tuple(tuple(item) for item in matriz_do_estado)

        if not estado_salvo in estados_e_valores:
            estados_e_valores[estado_salvo] = calcular_heuristica(matriz_do_estado, no_pai)
            nos.append(Node(list(estados_e_valores.items())[-1], parent=no_pai))


def calcular_heuristica(matriz: list[list[int]], no_pai: Node):
    heuristica = 0

    for i, linha in enumerate(matriz):
        for k, numero in enumerate(linha):
            if numero != 0:
                x_destino, y_destino = procurar_localizacao_estado(matriz[i][k] , estado_final)
                heuristica += abs(x_destino - i) + abs(y_destino - k)
    
    return heuristica

def procurar_localizacao_estado(estado: int, estados_analisado: list[int]):
    for i, linha in enumerate(estados_analisado):
        if estado in linha:
            y = linha.index(estado)
            x = i
            return x, y

def busca_gulosa(no_pai: Node):
    menor_valor = 0
    primeiro_acesso = False
    nos_heuristica_menores: list[Node] = []
    
    for no in PreOrderIter(no_pai):
        if no.is_leaf:
            if not primeiro_acesso:
                menor_valor = no.name[1]
                primeiro_acesso = True
            elif no.name[1] < menor_valor:
                menor_valor = no.name[1]
                menor_no = no

    for no in PreOrderIter(no_pai):
        if no.is_leaf and no.name[1] == menor_valor:
            return no

def funcao_principal():
    global estados_e_valores
    global nos
    i = 0

    estado_salvo = tuple(tuple(item) for item in estado_inicial)
    estados_e_valores[estado_salvo] = 0
    
    nos.append(Node(list(estados_e_valores.items())[-1]))
    matriz_analisada = list(list(item) for item in nos[0].name[0])
    no_analisado = nos[0]

    while(matriz_analisada != estado_final):
        x, y = procurar_localizacao_estado(0, matriz_analisada)
        expandir_estados(x, y, matriz_analisada, no_analisado)
        no_analisado = busca_gulosa(no_analisado)
        matriz_analisada = list(list(item) for item in no_analisado.name[0])
        i+=1

    print('Resultado atingido em: ', i, ' passos')
    print('----------------')
    for pre, fill, node in RenderTree(nos[0]):
        print("%s%s" % (pre, node.name))

funcao_principal()