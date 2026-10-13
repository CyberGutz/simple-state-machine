class AFD:
    def __init__(self, Alfabeto):
        self.__estadoAtual = None
        self.__deuErro = None
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    @staticmethod
    def saveAf(af, nome):
        nome = str(nome)
        if not nome.endswith(".txt"):
            nome += ".txt"
        arq = open(nome, "w")
        arq.write(str(af))
        arq.close()

    @staticmethod
    def loadAF(path):
        afs = open(path, "r").read()
        est = afs[afs.find('E = {') + 1:afs.find('A = {')]
        alfa = afs[afs.find('A = {') + 1:afs.find('T = {')]
        trans = afs[afs.find('T = {') + 1:afs.find('i = ')]
        ini = afs[afs.find('i = ') + 4]
        fin = afs[afs.find('F = {') + 1:len(afs)]
        bypass = " >'=-{},()\n"
        aux = ""
        for i in alfa:
            if i not in bypass:
                aux = aux + i
        af = AFD(aux)
        for i in est:
            if i not in bypass:
                if i in ini and i in fin:
                    af.criaEstado(i, True, True)
                if i in ini and i not in fin:
                    af.criaEstado(i, True)
                if i in fin and i not in ini:
                    af.criaEstado(i, False, True)
                else:
                    af.criaEstado(i)
        aux = []
        for i in trans:
            if i not in bypass:
                aux.append(i)
        i = 0
        while i != len(aux):
            af.criaTransicao(int(aux[i]), int(aux[i + 2]), aux[i + 1])
            i = i + 3
        return af

    @staticmethod
    def copiaAFD(origem):
        copia = AFD(origem.alfabeto)
        copia.estados = origem.estados
        copia.transicoes = origem.transicoes
        for i in origem.estados:
            if i is origem.inicial:
                copia.mudaEstadoInicial(i)
            if i in origem.finais:
                copia.mudaEstadoFinal(i, True)
        return copia

    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    def criaEstado(self, id, inicial=False, final=False):
        id = int(id)
        if id in self.estados:
            return False
        self.estados = self.estados.union({id})
        if inicial:
            self.inicial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    def criaTransicao(self, origem, destino, simbolo):
        origem = int(origem)
        destino = int(destino)
        simbolo = str(simbolo)
        if origem not in self.estados:
            return False
        if destino not in self.estados:
            return False
        self.transicoes[(origem, simbolo)] = destino
        return True

    def mudaEstadoInicial(self, id):
        if id not in self.estados:
            return
        self.inicial = id

    def mudaEstadoFinal(self, id, final):
        if id not in self.estados or (not final and id not in self.finais):
            return
        if final:
            self.finais.add(id)
        else:
            self.finais.remove(id)

    def moveAFD(self, cadeia):
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                self.__deuErro = True
                break
            if (self.__estadoAtual, simbolo) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                break
        return self.__estadoAtual

    def deuErro(self):
        return self.__deuErro

    def estadoAtual(self):
        return self.__estadoAtual

    def estadoFinal(self, id):
        return id in self.finais

    def __str__(self):
        s = 'AFD(E, A, T, i, F): \n'
        s += '  E = { '
        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += '  A = { '
        for a in self.alfabeto:
            s += "'{}', ".format(a)
        s += '} \n'
        s += '  T = { '
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({}, '{}') --> {}, ".format(e, a, d)
        s += '} \n'
        s += '  i = {}\n'.format(self.inicial)
        s += '  F = {'
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '} \n'
        return s
