import pytest
from pilha import Pilha

@pytest.fixture
def pilha():
    return Pilha()

def test_pilha_inicialmente_vazia(pilha):
    assert pilha.size() == 0
    assert pilha.pilhaVazia() is True

def test_push_incrementa_tamanho(pilha):
    pilha.push(10)
    assert pilha.size() == 1
    assert pilha.pilhaVazia() is False

def test_push_multiplos_elementos(pilha):
    elementos = [1, 2, 3]
    for e in elementos:
        pilha.push(e)
    assert pilha.size() == len(elementos)

def test_pop_remove_elemento(pilha):
    pilha.push(42)
    elem = pilha.pop()
    assert elem == 42
    assert pilha.size() == 0
    assert pilha.pilhaVazia() is True

def test_pop_ordem_lifo(pilha):
    pilha.push("a")
    pilha.push("b")
    pilha.push("c")
    assert pilha.pop() == "c"
    assert pilha.pop() == "b"
    assert pilha.pop() == "a"

def test_pop_em_pilha_vazia_dispara_excecao(pilha):
    with pytest.raises(IndexError):
        pilha.pop()

def test_consistencia_size_e_pilhaVazia(pilha):
    assert pilha.pilhaVazia()
    pilha.push(99)
    assert pilha.size() == 1
    assert not pilha.pilhaVazia()
    pilha.pop()
    assert pilha.size() == 0
    assert pilha.pilhaVazia()