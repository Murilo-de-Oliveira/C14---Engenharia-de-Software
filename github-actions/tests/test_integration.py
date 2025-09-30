import pytest
from app.models import Task, TaskCreate
from app.database import clear_db
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def db_cleanup():
    """
    Fixture para limpar o banco de dados antes e depois de cada teste de integração.
    """
    clear_db()
    yield
    clear_db()

@pytest.fixture
def sample_task_in_db() -> Task:
    """
    Fixture que cria uma tarefa via API e retorna o objeto Task completo.
    """
    task_data = {"title": "Task de Teste", "description": "Descrição de teste"}
    response = client.post("/tasks/", json=task_data)
    return Task(**response.json())

def test_create_task_api():
    """Testa a criação de uma tarefa via POST /tasks/."""
    payload = {"title": "Comprar pão", "description": "Na padaria da esquina"}
    response = client.post("/tasks/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert "id" in data
    assert data["completed"] is False

def test_read_all_tasks_api():
    """Testa a listagem de todas as tarefas via GET /tasks/."""
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    response = client.get("/tasks/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"

def test_read_one_task_api(sample_task_in_db: Task):
    """Testa a busca de uma tarefa específica via GET /tasks/{task_id}."""
    response = client.get(f"/tasks/{sample_task_in_db.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_task_in_db.id

def test_update_task_api(sample_task_in_db: Task):
    """Testa a atualização de uma tarefa via PUT /tasks/{task_id}."""
    payload = {"title": "Título Atualizado", "description": "Descrição Nova", "completed": True}
    response = client.put(f"/tasks/{sample_task_in_db.id}", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

def test_delete_task_api_flow(sample_task_in_db: Task):
    """Testa a deleção de uma tarefa e verifica se ela realmente sumiu."""
    response_delete = client.delete(f"/tasks/{sample_task_in_db.id}")
    assert response_delete.status_code == 204
    response_get = client.get(f"/tasks/{sample_task_in_db.id}")
    assert response_get.status_code == 404

def test_read_one_task_api_not_found():
    """Testa se buscar uma tarefa com ID inexistente retorna 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_update_task_api_not_found():
    """Testa se atualizar uma tarefa com ID inexistente retorna 404."""
    payload = {"title": "Inexistente"}
    response = client.put("/tasks/999", json=payload)
    assert response.status_code == 404

def test_delete_task_api_not_found():
    """Testa se deletar uma tarefa com ID inexistente retorna 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404

def test_create_task_api_invalid_payload():
    """Testa a criação de tarefa com um título muito curto, esperando um erro 422."""
    payload = {"title": "ab"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 422

def test_create_task_without_description():
    """Deve aceitar criação sem description."""
    r = client.post("/tasks/", json={"title": "Sem desc"})
    assert r.status_code == 201
    assert r.json()["description"] is None

def test_create_task_with_completed_true():
    """Deve aceitar completed=True na criação."""
    payload = {"title": "Feita", "completed": True}
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201
    assert r.json()["completed"] is True

def test_read_all_tasks_empty():
    """GET /tasks/ deve retornar lista vazia se não houver nada."""
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert r.json() == []