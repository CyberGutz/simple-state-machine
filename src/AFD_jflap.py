# from AFD import *
import xml.etree.ElementTree as ET
from AFD import AFD


class AFD_JFLAP:
    @staticmethod
    def lerAFD(path):
        # local = input("Digite o local do arquivo a ser lido: ")
        # Ler o conteúdo do arquivo
        arq = str(path)
        if not arq.endswith(".jff"):
            arq += ".jff"
        with open(arq) as p:
            xml_content = p.read()

        # Analisa o conteúdo XML
        root = ET.fromstring(xml_content)
        # Inicializa as variáveis
        id_inicial = None
        ids_finais = []
        lista_es = []
        origem = []
        car = []
        destino = []
        afd = []
        aux2 = [0, '*', 0]

        # Pegando os estados
        for estado in root.findall('.//state'):
            state_id = estado.get('id')
            for child in estado:
                if child.tag == 'initial':  # Verifica se o estado tem a tag initial, se tiver pega o id do estado
                    id_inicial = int(state_id) + 1
                elif child.tag == 'final':
                    ids_finais.append(int(state_id) + 1)

        for transicao in root.findall('.//transition'):
            for aux1 in transicao.findall('./from'):
                k = aux1.text
                origem.append(int(k) + 1)
            for aux1 in transicao.findall('./read'):
                r = aux1.text
                car.append(r)
            for aux1 in transicao.findall('./to'):
                s = aux1.text
                destino.append(int(s) + 1)
        alf = ""
        estado = []
        for i in range(len(car)):
            aux2[0] = origem[i]
            if aux2[0] not in estado:
                estado.append(aux2[0])
            aux2[1] = car[i]
            if car[i] not in alf:
                alf = alf + car[i]
            aux2[2] = destino[i]
            aux3 = []
            aux3 = aux3 + aux2
            lista_es.append(aux3)

        # Imprime os resultados
        afd.append(id_inicial)
        afd.append(ids_finais)
        afd.append(lista_es)

        afd_res = AFD(alf)

        for i in range(len(estado)):
            afd_res.criaEstado(i + 1)

        afd_res.mudaEstadoInicial(afd[0])  # Pegando o Estado Inicial

        for i in range(len(afd[1])):  # Pegando os Estados Finais
            afd_res.mudaEstadoFinal(afd[1][i], True)

        for i in range(len(afd[2])):  # Pegando as Transições
            afd_res.criaTransicao(afd[2][i][0], afd[2][i][2], afd[2][i][1])

        print(afd_res)

        return afd_res

    @staticmethod
    def escreveAFD(afd, nome):
        arq = str(nome)
        if not arq.endswith(".jff"):
            arq += ".jff"

        a = open(arq, "w")
        a.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.--><structure>&#13;')
        a.write("\n<type>fa</type>&#13;")
        a.write("\n<automaton>&#13;")
        for i in afd.estados:
            aux = i
            aux = i - 1
            q = 'q'
            q = q + str(aux)
            a.write('\n<state id="{}" name="{}">&#13;'.format(aux, aux))
            if i == afd.inicial:
                a.write('\n<initial/>&#13;')
            if i in afd.finais:
                a.write('\n<final/>&#13;')
            a.write("\n</state>&#13;")

        for i in afd.transicoes.items():
            a.write('\n<transition>&#13;')
            a.write('\n<from>{}</from>&#13;'.format(i[0][0] - 1))
            a.write('\n<to>{}</to>&#13;'.format(i[1] - 1))
            a.write('\n<read>{}</read>&#13;'.format(i[0][1]))
            a.write('\n</transition>&#13;')
        a.write('\n</automaton>&#13;')
        a.write('\n</structure>')
        a.close()
