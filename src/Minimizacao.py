from AFD import AFD


class Minimizacao:
    # Função que faz a equivalência de estados. Essa é a base para todas as operações desta classe.
    @staticmethod
    def stateEq(afd, id1, id2, visited=None):
        # Casos-base - Estados trivialmente equivalentes ou trivialmente não equivalentes
        # Se os estados são iguais, são equivalentes.
        if id1 == id2:
            return True
        # Se um dos estados não for um estado válido do autômato
        if (id1 not in afd.estados) or (id2 not in afd.estados):
            return False
        # Se ambos são estados finais, eles são equivalentes
        if (id1 in afd.finais) and (id2 in afd.finais):
            return True
        # Se um dos estados estiver nos finais e o outro não
        if (id1 in afd.finais) and (id2 not in afd.finais):
            return False
        if (id1 not in afd.finais) and (id2 in afd.finais):
            return False

        # Inicialização de estados visitados.
        if visited is None:
            visited = set()

        # Se os estados já foram visitados, são equivalentes. Isso também evita loops infinitos.
        if (id1, id2) in visited or (id2, id1) in visited:
            return True

        # Marca os estados como visitados.
        visited.add((id1, id2))

        # Verifica a equivalência para cada símbolo do alfabeto.
        for symbol in afd.alfabeto:
            next_state1 = afd.transicoes.get((id1, symbol))
            next_state2 = afd.transicoes.get((id2, symbol))

            # Se a transição for a mesma para ambos, pula essa iteração de modo a evitar chamadas recursivas desnecessárias
            if next_state1 == next_state2:
                continue

            # Se uma transição é nula e a outra não, os estados não são equivalentes.
            if (next_state1 is None) != (next_state2 is None):
                return False

            # Se ambas as transições não são nulas, verifica a equivalência recursivamente.
            if next_state1 is not None and next_state2 is not None:
                if not Minimizacao.stateEq(afd, next_state1, next_state2, visited):
                    return False

        # Se não foi encontrado motivo para serem diferentes, os estados são equivalentes.
        return True

    # Função cria uma lista de listas de estados equivalentes entre si. Usado na minimização.
    @staticmethod
    def estadosEquivalentes(afd):
        equivalentes = []
        for i in afd.estados:
            aux = []
            for j in afd.estados:
                if i == j:
                    continue
                if [i, j] in equivalentes or [j, i] in equivalentes:
                    continue
                if Minimizacao.stateEq(afd, i, j):
                    aux.append(i)
                    aux.append(j)
                if not aux or aux in equivalentes:
                    continue
                else:
                    equivalentes.append(aux)
        return equivalentes

    @staticmethod
    def concatAF(af1, af2):
        # Concatena os alfabetos
        alfabeto = af1.alfabeto
        if af2.alfabeto != af1.alfabeto:
            for i in af2.alfabeto:
                if i not in af1.alfabeto:
                    alfabeto += i
        # Cria um AFD auxiliar
        aux = AFD(alfabeto)
        # Entra com os estados do AF1
        for i in af1.estados:
            aux.criaEstado(i)
            if af1.inicial == i:
                aux.mudaEstadoInicial(i)
            if i in af1.finais:
                aux.mudaEstadoFinal(i, True)
        # Entra com as transições do AF1
        for i in af1.estados:
            for j in alfabeto:
                for j in alfabeto:
                    if (i, j) in af1.transicoes.keys():
                        aux.criaTransicao(i, af1.transicoes.get((i, j)), j)
        # Concatena os estados do AF2 (Adicionado 20 no estado, de modo a tirar ambiguidade de nomes entre os dois AF's
        for i in af2.estados:
            e = i + 20
            aux.criaEstado(e)
            if i in af2.finais:
                aux.mudaEstadoFinal(e, True)
        # Por fim, concatena as transições do AF2
        for i in af2.estados:
            e = i + 20
            for j in alfabeto:
                if (i, j) in af2.transicoes.keys():
                    aux.criaTransicao(e, (af2.transicoes.get((i, j)) + 20), j)
        return aux

    @staticmethod
    def afEq(afd1, afd2):
        # Concatena os dois autômatos
        afConcatenado = Minimizacao.concatAF(afd1, afd2)
        # Verifica se os estados iniciais são equivalentes. Se forem, os autômatos são equivalentes.
        if Minimizacao.stateEq(afConcatenado, afd1.inicial, (afd2.inicial + 20)):
            return True
        else:
            return False

    @staticmethod
    def minimizacao(afd):
        # Removendo estados equivalentes:
        equivalentes = Minimizacao.estadosEquivalentes(afd)
        for i in equivalentes:
            for j in afd.estados:
                for k in afd.alfabeto:
                    if (j, k) in afd.transicoes:
                        # Transpõe as transições
                        if afd.transicoes[(j, k)] == i[1] and j != i[1]:
                            del afd.transicoes[(j, k)]
                            afd.criaTransicao(j, i[0], k)
                        if j == i[1]:
                            del afd.transicoes[(j, k)]
        # O estado que se mantém é sempre o primeiro da tupla
        afd.estados.remove(i[1])

        # Removendo estados não alcançados
        not_reached = []
        for i in afd.estados:
            controle = 0
            if i is afd.inicial:
                continue
            for j in afd.estados:
                for symbol in afd.alfabeto:
                    # Se existe alguma transição que leva até aquele estado, então ele não é alcançado
                    if afd.transicoes.get((j, symbol)) == i:
                        controle = 0
                        break
                    else:
                        # Se nessa iteração ele não achou nenhuma transição, controle = 1
                        controle = 1
                # Se foi achada alguma transição, ambos os laços são quebrados
                if controle == 0:
                    break
            # Se controle se manteve 1, ou seja, não foi achada nenhuma transição para aquele estado,
            # então ele é incluído na lista de estados não alcançados
            if controle == 1:
                not_reached.append(i)
        # Por fim, percorre o vetor de estados não alcançados e elimina-os.
        for i in not_reached:
            for symbol in afd.alfabeto:
                if (i, symbol) in afd.transicoes:
                    del afd.transicoes[(i, symbol)]
            afd.estados.remove(i)
