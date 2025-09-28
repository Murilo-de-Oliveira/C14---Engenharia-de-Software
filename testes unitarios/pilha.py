class Pilha:
    def __init__(self):
        self.elementos = []
        self.tamanho = 0

    def size(self):
        return self.tamanho
    
    def pilhaVazia(self):
        return (self.tamanho == 0)
    
    def push(self, elem):
        self.elementos.append(elem)
        self.tamanho += 1
    
    def pop(self):
        if (self.pilhaVazia()):
            raise IndexError()
        
        elem = self.elementos.pop(self.tamanho - 1)
        self.tamanho -= 1
        return elem

