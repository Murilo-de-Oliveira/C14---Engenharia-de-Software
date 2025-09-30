import pytest
from app.models import Task
from app.database import (
    create_task_db,
    get_all_tasks_db,
    get_task_db,
    update_task_db,
    delete_task_db,
    clear_db,
)

@pytest.fixture(autouse=True)
def db_cleanup():
    """
    Fixture para limpar o banco de dados antes e depois de cada teste unitário.
    """
    clear_db()
    yield
    clear_db()

def test_get_task_db_not_found():
    """Testa se buscar uma tarefa com ID inexistente retorna None."""
    assert get_task_db(999) is None

def test_get_all_tasks_db_empty():
    """Deve retornar lista vazia se não houver tarefas."""
    assert get_all_tasks_db() == []

def test_create_task_db_multiple():
    """IDs devem ser auto-incrementais."""
    t1 = create_task_db(Task(id=0, title="Title1"))
    t2 = create_task_db(Task(id=0, title="Title2"))
    assert t1.id == 1
    assert t2.id == 2

def test_update_task_db_success():
    t = create_task_db(Task(id=0, title="Old"))
    updated = update_task_db(t.id, Task(id=t.id, title="New"))
    assert updated is not None
    assert updated.title == "New"

def test_update_task_db_not_found():
    """Atualizar ID inexistente deve retornar None."""
    result = update_task_db(999, Task(id=999, title="Title"))
    assert result is None

def test_delete_task_db_success():
    t = create_task_db(Task(id=0, title="Temp"))
    assert delete_task_db(t.id) is True
    assert get_task_db(t.id) is None

def test_delete_task_db_not_found():
    """Deletar ID inexistente deve retornar False."""
    assert delete_task_db(999) is False

def test_clear_db_resets():
    """clear_db deve limpar e resetar contador de IDs."""
    create_task_db(Task(id=0, title="Temp"))
    clear_db()
    assert get_all_tasks_db() == []
    t = create_task_db(Task(id=0, title="Novo"))
    assert t.id == 1