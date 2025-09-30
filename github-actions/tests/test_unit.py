import pytest
from fastapi import HTTPException
from app.models import Task
from app.database import (
    create_task_db,
    get_all_tasks_db,
    get_task_db,
    update_task_db,
    delete_task_db,
    clear_db,
)
from app import main

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

def test_create_task_calls_create_task_db(mocker):
    """Verifica se create_task chama create_task_db corretamente."""
    fake_task = {"id": 1, "title": "Teste", "description": "Mocked"}
    mock_create = mocker.patch("app.main.create_task_db", return_value=fake_task)

    payload = main.TaskCreate(title="Teste", description="Mocked")
    result = main.create_task(payload)

    mock_create.assert_called_once()
    assert result == fake_task


def test_read_task_not_found_raises(mocker):
    """Se get_task_db retornar None, deve levantar 404."""
    mocker.patch("app.main.get_task_db", return_value=None)

    with pytest.raises(HTTPException) as exc:
        main.read_task(999)
    assert exc.value.status_code == 404


def test_update_task_calls_update_task_db(mocker):
    """Verifica se update_task chama update_task_db corretamente."""
    mocker.patch("app.main.get_task_db", return_value={"id": 1})
    mock_update = mocker.patch("app.main.update_task_db", return_value={"id": 1, "title": "Novo"})

    payload = main.TaskCreate(title="Novo")
    result = main.update_task(1, payload)

    mock_update.assert_called_once()
    assert result["title"] == "Novo"


def test_update_task_not_found_raises(mocker):
    """update_task deve levantar 404 se ID não existir."""
    mocker.patch("app.main.get_task_db", return_value=None)
    payload = main.TaskCreate(title="Title")

    with pytest.raises(HTTPException) as exc:
        main.update_task(123, payload)
    assert exc.value.status_code == 404


def test_delete_task_calls_delete_task_db(mocker):
    """delete_task deve chamar delete_task_db e não levantar erro se True."""
    mocker.patch("app.main.delete_task_db", return_value=True)
    assert main.delete_task(1) is None


def test_delete_task_not_found_raises(mocker):
    """delete_task deve levantar 404 se delete_task_db retornar False."""
    mocker.patch("app.main.delete_task_db", return_value=False)

    with pytest.raises(HTTPException) as exc:
        main.delete_task(999)
    assert exc.value.status_code == 404