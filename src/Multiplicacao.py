from AFD import AFD

def acha(aux, n1, n2):
        for i in range(len(aux)):
            if(n1 == aux[i][0]) and (n2 == aux[i][1]):
                return i

class Multiplicacao:
    @staticmethod
    def multi(afd1, afd2):
        len1 = len(afd1.estados)
        len2 = len(afd2.estados)
        len3 = len1 * len2
        alf = afd1.alfabeto
        afd3 = AFD(alf)
        for i in range(1, len3+1):
            afd3.criaEstado(i)
        afd3.mudaEstadoInicial(1)
        #print(afd3.estados)
        aux = []
        for i in range(1, len1+1):
            for j in range(1, len2+1):
                aux2 = [i, j]
                aux.append(aux2)

        for i in afd1.transicoes.items():
            for j in afd2.transicoes.items():
                if j[0][1] == i[0][1]:
                    trans1 = acha(aux, i[0][0], j[0][0])
                    trans2 = acha(aux, i[1], j[1])
                    afd3.criaTransicao(trans1+1, trans2+1, j[0][1])

        return afd3
