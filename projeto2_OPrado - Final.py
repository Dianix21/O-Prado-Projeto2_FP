"""
Projeto realizado por: Diana Goulao ist1102531
este projeto tem como objetivo simular um ecossistema de um prado em que convivem animais que se movimentam, alimentam, reproduzem e morrem, para isso define-se 3 TAD's e algumas funcoes adicionais:
    TAD posicao - O TAD posicao e usado para representar uma posicao (x, y) de um prado arbitrariamente grande, sendo x e y dois valores inteiros nao negativos
    TAD animal - O TAD animal e usado para representar os animais que habitam o prado, existindo de dois tipos: predadores e presas. Os predadores sao caracterizados pela especie, idade, frequencia de reproducao,
        fome e frequencia de alimentacao. As presas sao apenas caracterizadas pela especie, idade e frequencia de reproducao
    TAD prado - O TAD prado e usado para representar o mapa do ecossistema e as animais que se encontram dentro
    funcoes adicionais - geracao e simula_ecossistema
"""

# TAD posicao - Construtores
def cria_posicao(x, y):
    """
    cria_posicao: int x int ---> posicao
    representacao interna: R(x, y) = (x, y)
    esta funcao recebe dois valores correspondentes as coordenadas de uma posicao e devolve a posicao, validando os argumentos
    """
    
    if not (type(x) == int and type(y) == int and x >= 0 and y >= 0):
        raise ValueError("cria_posicao: argumentos invalidos")
    return (x, y)


def cria_copia_posicao(p):
    """
    cria_copia_posicao: posicao ---> posicao
    esta funcao devolve uma copia de uma posicao
    """

    return cria_posicao(p[0], p[1])


# TAD posicao - Seletores
def obter_pos_x(p):
    """
    obter_pos_x: posicao ---> int
    esta funcao devolve a abcissa da posicao
    """
    
    return p[0]


def obter_pos_y(p):
    """
    obter_pos_y: posicao ---> int
    esta funcao devolve a ordenada da posicao
    """
    
    return p[1]


# TAD posicao - Reconhecedores
def eh_posicao(arg):
    """
    eh_posicao: universal ---> booleano
    esta funcao recebe um argumento e devolve True se esse argumento e um TAD posicao e False caso contrario
    """
    
    return (type(arg) == tuple and len(arg) == 2 and type(arg[0]) == int and type(arg[1]) == int and arg[0] >= 0 and arg[1] >= 0)


# TAD posicao - teste
def posicoes_iguais(p1, p2):
    """
    posicoes_igauis: posicao x posicao ---> booleano
    esta funcao recebe duas posicoes e devolve True se elas forem iguais e False caso contrario
    """
    
    return (eh_posicao(p1) and eh_posicao(p2) and obter_pos_x(p1) == obter_pos_x(p2) and obter_pos_y(p1) == obter_pos_y(p2))

# TAD posicao - Transformador
def posicao_para_str(p):
    """
    posicao_para_str: posicao ---> str
    esta funcao recebe uma posicao e devolve a string '(x, y)'
    """
    
    return "(" + str(obter_pos_x(p)) + ", " + str(obter_pos_y(p)) + ")"


# TAD posicoes - funcoes de alto nivel
def obter_posicoes_adjacentes(p):
    """
    obter_posicoes_adjacentes: posicao ---> tuplo
    esta funcao devolve um tuplo com as posicoes adjacentes a posicao dada como argumento, comecando na posicao acima e seguindo no sentido horario
    """
    
    pos_cima, pos_direita, pos_baixo, pos_esquerda = None, None, None, None

    if obter_pos_y(p) != 0:
        pos_cima = cria_posicao(obter_pos_x(p), obter_pos_y(p) - 1)
        
    pos_direita = cria_posicao(obter_pos_x(p) + 1, obter_pos_y(p))
    
    pos_baixo = cria_posicao(obter_pos_x(p), obter_pos_y(p) + 1)
    
    if obter_pos_x(p) != 0:
        pos_esquerda = cria_posicao(obter_pos_x(p) - 1, obter_pos_y(p))

    if pos_cima == None and pos_esquerda == None:
        return (pos_direita, pos_baixo)
    elif pos_esquerda == None:
        return (pos_cima, pos_direita, pos_baixo)
    elif pos_cima == None:
        return (pos_direita, pos_baixo, pos_esquerda)
    else:
        return (pos_cima, pos_direita, pos_baixo, pos_esquerda)


def ordenar_posicoes(t):
    """
    ordenar_posicoes: tuplo ---> tuplo
    esta funcao devolve o tuplo do argumento ordenado de acordo com a ordem de leitura do prado
    """
    
    t = list(t)
    
    def bubblesort(t):
        changed = True
        size = len(t) - 1
        while changed:
            changed = False
            for i in range(size):
                if obter_pos_y(t[i]) > obter_pos_y(t[i + 1]) or (obter_pos_y(t[i]) == obter_pos_y(t[i + 1]) and obter_pos_x(t[i + 1]) < obter_pos_x(t[i])):
                    t[i], t[i + 1] = t[i + 1], t[i]
                    changed = True
            size = size - 1
        return t
        
    return tuple(bubblesort(t))


# TAD animal - Construtores
def cria_animal(especie, reproducao, alimentacao):
    """
    cria_animal: str x int x int ---> animal
    representacao interna: R(especie,reproducao,alimentacao) = se for predador - {"especie": especie, "idade": 0, "frequencia de reproducao": reproducao, "fome": 0, "frequencia de alimentacao": alimentacao}
                                                               se for presa - {"especie": especie, "idade": 0, "frequencia de reproducao": reproducao}
    esta funcao recebe a especie(str) e dois inteiros correspondentes a frequencia de reproducao e de alimentacao e devolve o animal, tendo em conta se e predador ou presa, validando os argumentos
    """
    
    if not (type(especie) == str and type(reproducao) == int and type(alimentacao) == int and len(especie) >= 1 and reproducao > 0 and alimentacao >= 0):
        raise ValueError("cria_animal: argumentos invalidos")
    if alimentacao > 0:  # predadores
        return {"especie": especie, "idade": 0, "frequencia de reproducao": reproducao, "fome": 0, "frequencia de alimentacao": alimentacao}
    else:  # presas
        return {"especie": especie, "idade": 0, "frequencia de reproducao": reproducao}


def cria_copia_animal(animal):
    """
    cria_copia_animal: animal ---> animal
    esta funcao devolve uma copia do animal dado como argumento
    """
    
    return animal.copy()


# TAD animal - Seletores
def obter_especie(animal):
    """
    obter_especie: animal ---> str
    esta funcao recebe um animal e devolve a especie desse animal
    """
    
    return animal["especie"]


def obter_freq_reproducao(animal):
    """
    obter_freq_reproducao: animal ---> int
    esta funcao recebe um animal e devolve o inteiro correspondente a frequencia de reproducao
    """
    
    return animal["frequencia de reproducao"]


def obter_freq_alimentacao(animal):
    """
    obter_freq_alimentacao: animal ---> int
    esta funcao recebe um animal e devolve o inteiro correspondente a frequencia de alimentacao (presas devolvem 0)
    """
    
    if "frequencia de alimentacao" in animal:
        return animal["frequencia de alimentacao"]
    else:
        return 0


def obter_idade(animal):
    """
    obter_idade: animal ---> int
    esta funcao recebe um animal e devolve o inteiro correspondente a idade do animal
    """
    
    return animal["idade"]


def obter_fome(animal):
    """
    obter_fome: animal ---> int
    esta funcao recebe um animal e devolve o inteiro correspondente a fome do animal (presas devolvem 0)
    """
    
    if "fome" in animal:
        return animal["fome"]
    else:
        return 0


# TAD animal - Modificadores
def aumenta_idade(animal):
    """
    aumenta_idade: animal ---> animal
    esta funcao modifica destrutivamente o animal aumentando a sua idade devolvendo o proprio animal
    """
    
    animal["idade"] += 1
    return animal


def reset_idade(animal):
    """
    reset_idade: animal ---> animal
    esta funcao modifica destrutivamente o animal colocando a sua idade a zero devolvendo o proprio animal
    """
    
    animal["idade"] = 0
    return animal


def aumenta_fome(animal):
    """
    aumenta_fome: animal ---> animal
    esta funcao modifica destrutivamente o animal aumentando a sua fome devolvendo o proprio animal
    """
    
    if "fome" in animal:
        animal["fome"] += 1
        return animal
    else:
        return animal


def reset_fome(animal):
    """
    reset_fome: animal ---> animal
    esta funcao modifica destrutivamente o animal colocando a sua fome a zero devolvendo o proprio animal
    """
    
    if "fome" in animal:
        animal["fome"] = 0
        return animal
    else:
        return animal


# TAD animal - Reconhecedores
def eh_animal(arg):
    """
    eh_animal: universal ---> booleano
    esta funcao recebe um argumento e devolve True se este e um TAD animal e False caso contrario
    """
    
    if not (type(arg) == dict and (len(arg) == 3 or len(arg) == 5) and "especie" in arg and "idade" in arg and "frequencia de reproducao" in arg):
        return False
    elif not (type(arg["especie"]) == str and type((arg["frequencia de reproducao"])) == int and type(arg["idade"]) == int and len(arg["especie"]) >= 1 and arg["frequencia de reproducao"] > 0 and arg["idade"] >= 0):
        return False
    elif len(arg) == 5:  # restricao predadores
        if not ("fome" in arg and "frequencia de alimentacao" in arg and type(arg["fome"]) == int and type(arg["frequencia de alimentacao"]) == int and arg["fome"] >= 0 and arg["frequencia de alimentacao"] > 0):
            return False
    return True


def eh_predador(arg):
    """
    eh_predador: universal ---> booleano
    esta funcao recebe um argumento e devolve True se este e um TAD animal do tipo predador e False caso contrario
    """
    
    return (eh_animal(arg) and len(arg) == 5)


def eh_presa(arg):
    """
    eh_presa: universal ---> booleano
    esta funcao recebe um argumento e devolve True se este e um TAD animal do tipo presa e False caso contrario
    """
    
    return (eh_animal(arg) and len(arg) == 3)


# TAD animal - Testes
def animais_iguais(a1, a2):
    """
    animais_iguais: animal x animal ---> booleano
    esta funcao recebe dois animais e devolve True se estes forem animais e iguais e False caso contrario
    """
    
    if not (eh_animal(a1) and eh_animal(a2)):
        return False
    elif not ((eh_presa(a1) and eh_presa(a2)) or (eh_predador(a1) and eh_predador(a2))):
        return False
    elif (eh_presa(a1) and eh_presa(a2)):
        if not (a1["especie"] == a2["especie"] and a1["frequencia de reproducao"] == a2["frequencia de reproducao"] and a1["idade"] == a2["idade"]):
            return False
    elif (eh_predador(a1) and eh_predador(a2)):
        if not (a1["especie"] == a2["especie"] and a1["idade"] == a2["idade"] and a1["frequencia de reproducao"] == a2["frequencia de reproducao"] and a1["fome"] == a2["fome"] and a1["frequencia de alimentacao"] == a2["frequencia de alimentacao"]):
            return False
    return True


# TAD animal - Transformadores
def animal_para_char(animal):
    """
    animal_para_char: animal ---> str
    esta funcao recebe um animal e devolve o caracter correspondente a primeira letra da especie do animal, em maiuscula para predadores e minuscula para as presas
    """
    
    if eh_predador(animal):
        return animal["especie"][0].upper()
    else:
        return animal["especie"][0].lower()


def animal_para_str(animal):
    """
    animal_para_str: animal ---> str
    esta funcao recebe um animal e devolve uma string que representa o animal
    """
    
    if eh_presa(animal):
        return animal["especie"] + " [" + str(animal["idade"]) + "/" + str(animal["frequencia de reproducao"]) + "]"
    else:
        return animal["especie"] + " [" + str(animal["idade"]) + "/" + str(animal["frequencia de reproducao"]) + ";" + str(animal["fome"]) + "/" + str(animal["frequencia de alimentacao"]) + "]"


# TAD animal - funcoes de alto nivel
def eh_animal_fertil(animal):
    """
    eh_animal_fertil: animal ---> booleano
    esta funcao recebe um animal e devolve True se o animal atingiu a idade de reproducao e False caso contrario
    """
    
    return obter_idade(animal) >= obter_freq_reproducao(animal)


def eh_animal_faminto(animal):
    """
    eh_animal_faminto: animal ---> booleano
    esta funcao recebe um animal e devolve True se o animal atingiu o um valor de fome igual ou seuperior a freq de reproducao e False caso contrario (presas devolvem sempre False)
    """
    
    return eh_predador(animal) and obter_fome(animal) >= obter_freq_alimentacao(animal)


def reproduz_animal(animal):
    """
    reproduz: animal ---> animal
    esta funcao recebe um animal e devolve um novo animal da mesma especie com idade e fome igual a zero, alterando o animal progenitor passando a sua idade a zero
    """
    
    animal_novo = cria_copia_animal(animal)
    reset_idade(animal_novo)
    reset_fome(animal_novo)
    reset_idade(animal)
    return animal_novo


# TAD prado - Construtores
def cria_prado(d, r, a, p):
    """
    cria_prado: posicao x tuplo x tuplo x tuplo ---> prado
    representacao interna: R(d, r, a, p) = [d, r, a, p]
    esta funcao recebe a posicao do conto inferior direito do prado, um tuplo contendo as posicoes dos obstaculos, outro contendo os animais e um outro contendo as posicoes dos animais e devolve um prado, validando os argumentos
    """
    
    if not (eh_posicao(d) and type(r) == tuple and type(a) == tuple and type(p) == tuple):
        raise ValueError("cria_prado: argumentos invalidos")
    if not (len(r) >= 0 and all(eh_posicao(elemento) for elemento in r) and len(a) >= 1 and all(eh_animal(arg) for arg in a) and len(p) == len(a)):
        raise ValueError("cria_prado: argumentos invalidos")
    for pos_obs in r:
        if not (0 < obter_pos_x(pos_obs) < obter_pos_x(d) and 0 < obter_pos_y(pos_obs) < obter_pos_y(d)):  # verifica se as posicoes dos obstaculos estao dentro dos limites do prado
            raise ValueError("cria_prado: argumentos invalidos")
    for pos_ani in p:
        if not (0 < obter_pos_x(pos_ani) < obter_pos_x(d) and 0 < obter_pos_y(pos_ani) < obter_pos_y(d)):  # verifica se as posicoes dos animais estao dentro dos limites do prado
            raise ValueError("cria_prado: argumentos invalidos")
    return [d, r, a, p]


def cria_copia_prado(prado):
    """
    cria_copia_prado: prado ---> prado
    esta funcao devolve uma copia do prado dado como argumento
    """
   
    return prado.copy()


# TAD prado - Seletores
def obter_tamanho_x(prado):
    """
    obter_tamanho_x: prado ---> int
    esta funcao devolve o inteiro que corresponde ao numero de colunas do prado dado como argumento
    """
    
    return obter_pos_x(prado[0]) + 1


def obter_tamanho_y(prado):
    """
    obter_tamanho_y: prado ---> int
    esta funcao devolve o inteiro que corresponde ao numero de linhas do prado dado como argumento
    """
    
    return obter_pos_y(prado[0]) + 1


def obter_numero_predadores(prado):
    """
    obter_numero_predadores: prado ---> int
    esta funcao devolve o numero de animais predadores do prado dado como argumento
    """
    
    n_predadores = 0
    for animal in prado[2]:
        if eh_predador(animal):
            n_predadores += 1
    return n_predadores


def obter_numero_presas(prado):
    """
    obter_numero_presas: prado ---> int
    esta funcao devolve o numero de animais presa do prado dado como argumento
    """
    
    n_presas = 0
    for animal in prado[2]:
        if eh_presa(animal):
            n_presas += 1
    return n_presas
    

def obter_posicao_animais(prado):
    """
    obter_posicao_animais: prado ---> tuplo posicoes
    esta funcao devolve um tuplo que contem as posicoes do prado ocupadas por animais, ordenadas pela ordem de leitura do prado
    """
    
    return ordenar_posicoes(prado[3])


def aux_obter_indice_posicao(prado, posicao): # esta funcao auxiliar permite determinar o indice da posicao dada como argumento
    for pos in range(len(prado[3])):
        if posicoes_iguais(prado[3][pos], posicao):
            return pos
            

def obter_animal(prado, posicao):
    """
    obter_animal: prado x posicao ---> animal
    esta funcao devolve o animal do prado que se encontra na posicao dada como argumento
    """
    
    return prado[2][aux_obter_indice_posicao(prado, posicao)]


# TAD prado - Modificadores
def eliminar_animal(prado, posicao):
    """
    eliminar_animal: prado x posicao ---> prado
    esta funcao modifica destrutivamente o prado eliminando o animal na posicao dada como argumento, deixando-a livre, devolvendo o prado alterado
    """
    
    i = aux_obter_indice_posicao(prado, posicao)
    prado[3] = prado[3][:i] + prado[3][i + 1:]
    prado[2] = prado[2][:i] + prado[2][i + 1:]
    return prado
    
    
def mover_animal(prado, p1, p2):
    """
    mover_animal: prado x posicao x posicao ---> prado
    esta funcao modifica destrutivamente o prado movendo o animal na posicao dada como argumento para a nova posicao também dada como argumento, devolvendo o prado alterado
    """
    
    i = aux_obter_indice_posicao(prado, p1)
    prado[3] = prado[3][:i] + (p2,) + prado[3][i + 1:]
    return prado


def inserir_animal(prado, animal, posicao):
    """
    inserir_animal: prado x animal x posicao ---> prado
    esta funcao modifica destrutivamente o prado inserirndo um novo animal dado como argumento na posicao dada também como argumento, devolvendo o prado alterado
    """
    
    prado[3] = prado[3][:] + (posicao,)
    prado[2] = prado[2][:] + (animal,)
    return prado


# TAD prado - Reconhecedores
def eh_prado(arg):
    """
    eh_prado: universal ---> booleano
    esta funcao verifica se o argumento e um TAD prado
    """
    
    if not (type(arg) == list and len(arg) == 4):
        return False
    if not (eh_posicao(arg[0]) and type(arg[1]) == tuple and type(arg[2]) == tuple and type(arg[3]) == tuple):
        return False
    if not (len(arg[1]) >= 0 and all(eh_posicao(elemento) for elemento in arg[1]) and len(arg[2]) >= 1 and all(eh_animal(arg) for arg in arg[2]) and len(arg[3]) == len(arg[2])):
        return False
    return True


def eh_posicao_animal(prado, posicao):
    """
    eh_posicao_animal: prado x posicao ---> booleano
    esta funcao verifica se a posicao dada como argumento esta ocupada por um animal
    """
    
    return posicao in prado[3]


def eh_posicao_obstaculo(prado, posicao):
    """
    eh_posicao_obstaculo: prado x posicao ---> booleano
    esta funcao verifica se a posicao dada como argumento esta ocupada por um obstaculo (montanha ou rochedo)
    """
    
    return posicao in prado[1] or obter_pos_x(posicao) == 0 or obter_pos_x(posicao) == obter_tamanho_x(prado) - 1 or obter_pos_y(posicao) == 0 or obter_pos_y(posicao) == obter_tamanho_y(prado) - 1


def eh_posicao_livre(prado, posicao):
    """
    eh_posicao_livre: prado x posicao ---> booleano
    esta funcao verifica se a posicao dada como argumento esta livre
    """
    
    return not (eh_posicao_obstaculo(prado, posicao) or eh_posicao_animal(prado, posicao))


# TAD prado - Teste
def prados_iguais(prado1, prado2):
    """
    prados_iguais: prado x prado ---> booleano
    esta funcao verifica se os prados dados como argumentos sao iguais
    """
    
    return posicoes_iguais(prado1[0],prado2[0]) \
           and len(prado1[1]) == len(prado2[1]) and all(posicoes_iguais(prado1[1][i], prado2[1][i]) for i in range(len(prado1[1]))) \
           and len(prado1[2]) == len(prado2[2]) and all(animais_iguais(prado1[2][i], prado2[2][i]) for i in range(len(prado1[2]))) \
           and len(prado1[3]) == len(prado2[3]) and all(posicoes_iguais(ordenar_posicoes(prado1[3])[i], ordenar_posicoes(prado2[3])[i]) for i in range(len(prado1[3]))) \
           and all(animais_iguais(obter_animal(prado1, p), obter_animal(prado2, p)) for p in prado1[3]) # verifica se cada posicao corresponde ao mesmo animal

# TAD prado - Transformador
def prado_para_str(prado):
    """
    prado_para_str: prado ---> str
    esta funcao recebe um prado e devolve a string correspondente a representacao "grafica" do prado
    """
    
    linhas = obter_tamanho_y(prado)
    colunas = obter_tamanho_x(prado)
    print_prado = ""
    for i in range(linhas):
        if i == 0:  # primeira linha
            for j in range(colunas):
                if j == 0 or j == colunas - 1:  # cantos superiores
                    print_prado += ("+")
                else:
                    print_prado += ("-")
            print_prado += "\n"
            
        elif i == linhas - 1:  # ultima linha
            for j in range(colunas):
                if j == 0 or j == colunas - 1:  # cantos inferiores
                    print_prado += ("+")
                else:
                    print_prado += ("-")
        else:
            for j in range(colunas):
                if j == 0 or j == colunas - 1:  # limites laterais do prado
                    print_prado += ("|")
                elif eh_posicao_obstaculo(prado, cria_posicao(j, i)):
                    print_prado += ("@")
                elif eh_posicao_animal(prado, cria_posicao(j, i)):
                    print_prado += (animal_para_char(obter_animal(prado, cria_posicao(j, i))))
                else:
                    print_prado += (".")
            print_prado += "\n"
    return print_prado


# TAD animal - funcoes de alto nivel
def obter_valor_numerico(prado, posicao):
    """
    obter_valor_numerico: prado x posicao ---> int
    esta funcao devolve o valor numerico da posicao dada como argumento correspondente a ordem de leitura do prado dado também como argumento
    """
    
    return obter_tamanho_x(prado) * obter_pos_y(posicao) + obter_pos_x(posicao)


def obter_movimento(prado, posicao):
    """
    eh_posicao_obstaculo: prado x posicao ---> posicao
    esta funcao devolve a posicao seguinte do animal que se encontra na posicao dada como argumento de acordo com as regras de moviemnto dos animais no prado
    """

    pos_adjacentes = (obter_posicoes_adjacentes(posicao))
    lst_adjacentes = []
    lst_presa = []
    N = obter_valor_numerico(prado, posicao)
    
    for pos in pos_adjacentes:
        if eh_presa(obter_animal(prado, posicao)):
            if eh_posicao_livre(prado, pos) and 0 < obter_pos_x(pos) < obter_tamanho_x(prado) - 1 and 0 < obter_pos_y(pos) < obter_tamanho_y(prado) - 1:
                lst_adjacentes += [pos]
        else:
            if eh_posicao_animal(prado, pos) and eh_presa(obter_animal(prado, pos)) and 0 < obter_pos_x(pos) < obter_tamanho_x(prado) - 1 and 0 < obter_pos_y(pos) < obter_tamanho_y(prado) - 1:
                # excecao dos predadores: perioridade a posicoes adjacentes com presas
                lst_presa += [pos]
            elif eh_posicao_livre(prado, pos) and 0 < obter_pos_x(pos) < obter_tamanho_x(prado) - 1 and 0 < obter_pos_y(pos) < obter_tamanho_y(prado) - 1:
                lst_adjacentes += [pos]

    if len(lst_presa) == 1:
        return lst_presa[0]
    elif len(lst_presa) > 1:
        p = len(lst_presa)
        pos = N % p
        return lst_presa[pos]
        
    elif len(lst_adjacentes) == 1:
        return lst_adjacentes[0]
    elif len(lst_adjacentes) == 0:
        return posicao
    else:
        p = len(lst_adjacentes)
        pos = N % p
        return lst_adjacentes[pos]
        

# Funcoes adicionais
def geracao(prado):
    """
    geracao: prado ---> prado
    esta funcao modifica o prado dado como argumento de acordo com a evolucao de uma geracao completa (cada animal, no seu turno, realiza uma acao de acordo com as regras) e devolve o proprio prado
    """

    pos_animais_mortos = ()
    pos_animais = obter_posicao_animais(prado)
    for pos in pos_animais:
        if any(posicoes_iguais(pos, posMorto) for posMorto in pos_animais_mortos):
            # predador após matar a presa
            continue
        nova_pos = obter_movimento(prado, pos)
        animal = obter_animal(prado, pos)
        animal = aumenta_idade(animal)
        animal = aumenta_fome(animal)
        if pos != nova_pos:
            # regras de alimentacao
            if eh_predador(animal) and (eh_posicao_animal(prado, nova_pos) and eh_presa(obter_animal(prado, nova_pos))):  # se é predador e a nova posicao e ocupada por uma presa esta e comida
                prado = eliminar_animal(prado, nova_pos)
                animal = reset_fome(animal)
                prado = mover_animal(prado, pos, nova_pos)
                pos_animais_mortos += (nova_pos,)
            elif eh_predador(animal) and not (eh_posicao_animal(prado, nova_pos) and eh_presa(obter_animal(prado, nova_pos))) and not eh_animal_faminto(animal):
                prado = mover_animal(prado, pos, nova_pos)
            else:
                prado = mover_animal(prado, pos, nova_pos)

            # regras de reproducao
            if eh_animal_fertil(animal):
                prado = inserir_animal(prado, reproduz_animal(animal), pos)

        # regras de morte
        if eh_animal_faminto(animal):
            prado = eliminar_animal(prado, nova_pos)

    return prado


def simula_ecossistema(f_config, numero_geracoes, modo):
    """
    simula_ecossistema: str x int x booleano ---> tuplo
    esta funcao simula o ecossistema de um prado, recebe um ficheiro com as configuracoes da simulacao, um inteiro correspondente ao numero de geracoes a simular e um booleano que ativa o modo verboso(True) ou o modo quit(False)
        e devolve um tuplo que corresponde ao numero de predadores e presas no final da simulacao
    """

    fh = open(f_config, "r")
    linhas = fh.readlines()
    fh.close()
    nova_linha = []
    for linha in linhas:
        nova_linha += [(eval(linha))]  # obter os dados necessarios do ficheiro no tipo de dados pretendido de forma a obter os dados necessarios para criar o prado com essas configuracoes
    dim = cria_posicao(nova_linha[0][0], nova_linha[0][1])
    obs = tuple(cria_posicao(nova_linha[1][i][0], nova_linha[1][i][1]) for i in range(len(nova_linha[1])))
    ani = tuple(cria_animal(nova_linha[i][0], nova_linha[i][1], nova_linha[i][2]) for i in range(2, len(nova_linha)))
    pos_final = ()
    for i in range(2, len(nova_linha)):
        pos = tuple(cria_posicao(nova_linha[i][3][0], nova_linha[i][3][1]))
        pos_final += (pos,)
    prado = cria_prado(dim, obs, ani, pos_final)

    print("Predadores:", obter_numero_predadores(prado), "vs Presas:", obter_numero_presas(prado), "(Gen. 0)")  # geracao inicial comum aos dois modos
    print(prado_para_str(prado))

    if not modo:  # modo quiet - mostra apenas o prado no inicio e fim da simulacao retornando o tuplo com o n_presas e n_predadores
        gen = 0
        for gen in range(numero_geracoes + 1):
            prado = geracao(prado)
        print("Predadores:", obter_numero_predadores(prado), "vs Presas:", obter_numero_presas(prado), "(Gen.",
              str(gen) + ")")
        print(prado_para_str(prado))
        return (obter_numero_predadores(prado), obter_numero_presas(prado))

    else:  # modo verboso - - mostra o prado no inicio da simulacao e sempre que e alterado o numero de animais no prado e devolve no final da simulacao o tuplo com o n_presas e n_predadores
        n_presas = obter_numero_presas(prado)
        n_predadores = obter_numero_predadores(prado)
        gen = 0
        while gen <= numero_geracoes:
            gen += 1
            prado = geracao(prado)
            if n_presas != obter_numero_presas(prado) or n_predadores != obter_numero_predadores(prado):   # verificacao de alteracoes no numero de animais no prado
                print("Predadores:", obter_numero_predadores(prado), "vs Presas:", obter_numero_presas(prado), "(Gen.",
                      str(gen) + ")")
                print(prado_para_str(prado))
                n_presas = obter_numero_presas(prado)
                n_predadores = obter_numero_predadores(prado)
                # excecoes de paragem - caso o prado encha antes de chegar ao numero de geracoes a simular
            if n_predadores == 0 and n_presas + len(obs) == (obter_tamanho_x(prado) - 2) * (obter_tamanho_y(prado) - 2):
                return (obter_numero_predadores(prado), obter_numero_presas(prado))
            if n_presas == 0 and n_predadores + len(obs) == (obter_tamanho_x(prado)-2)*(obter_tamanho_y(prado)-2):
                return (obter_numero_predadores(prado), obter_numero_presas(prado))

        return (obter_numero_predadores(prado), obter_numero_presas(prado))

print(simula_ecossistema(config.txt,200,True))