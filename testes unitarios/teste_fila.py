import pytest
from fila import Fila

@pytest.fixture
def fila():
    return Fila()

def test_fila_inicialmente_vazia(fila):
    assert fila.size() == 0
    assert fila.filaVazia() is True

def test_enfileirar_incrementa_tamanho(fila):
    fila.enfileirar(10)
    assert fila.size() == 1
    assert fila.filaVazia() is False

def test_enfileirar_multiplos_elementos(fila):
    elementos = [1, 2, 3]
    for e in elementos:
        fila.enfileirar(e)
    assert fila.size() == len(elementos)

def test_remove_elemento(fila):
    fila.enfileirar(42)
    elem = fila.removerFila()
    assert elem == 42
    assert fila.size() == 0
    assert fila.filaVazia() is True

def test_removerFila_ordem_fifo(fila):
    fila.enfileirar("a")
    fila.enfileirar("b")
    fila.enfileirar("c")
    assert fila.removerFila() == "a"
    assert fila.removerFila() == "b"
    assert fila.removerFila() == "c"

def test_removerFila_em_fila_vazia_dispara_excecao(fila):
    with pytest.raises(IndexError):
        fila.removerFila()

def test_consistencia_size_e_filaVazia(fila):
    assert fila.filaVazia()
    fila.enfileirar(99)
    assert fila.size() == 1
    assert not fila.filaVazia()
    fila.removerFila()
    assert fila.size() == 0
    assert fila.filaVazia()