class Fila:
    def __init__(self):
        self.elementos = []
        self.tamanho = 0

    def size(self):
        return self.tamanho
    
    def filaVazia(self):
        return (self.tamanho == 0)
    
    def enfileirar(self, elem):
        self.elementos.append(elem)
        self.tamanho += 1
    
    def removerFila(self):
        if (self.filaVazia()):
            raise IndexError()
        
        elem = self.elementos.pop(0)
        self.tamanho -= 1
        return elem

