import pytest
from app.models import Task, TaskCreate
from app.database import create_task_db, get_all_tasks_db, get_task_db, update_task_db, delete_task_db, clear_db
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def db_cleanup():
    """
    Fixture para limpar o banco de dados antes e depois de cada teste.
    O `autouse=True` faz com que seja executada para TODOS os testes automaticamente.
    """
    clear_db()
    yield  # Aqui é onde o teste é executado
    clear_db()

@pytest.fixture
def sample_task_in_db() -> Task:
    """
    Fixture que cria uma tarefa diretamente no banco de dados e a retorna.
    Útil para testes unitários da camada de DB.
    """
    # Usamos o TestClient para criar a tarefa via API, garantindo consistência
    # Isso também nos dá um objeto Task completo com o ID atribuído.
    task_data = {"title": "Task de Teste", "description": "Descrição de teste"}
    response = client.post("/tasks/", json=task_data)
    return Task(**response.json())

def test_create_task_db_success():
    task_to_create = TaskCreate(title="Nova Tarefa", description="Uma descrição qualquer")
    created_task = client.post("/tasks/", json=task_to_create.model_dump()).json()
    
    assert created_task['id'] == 1
    assert created_task['title'] == "Nova Tarefa"
    assert get_task_db(1) is not None

# (Os outros testes unitários de sucesso que já fizemos podem ser mantidos ou removidos
# em favor dos testes de integração, que são mais completos. Vamos mantê-los por enquanto
# para demonstrar a diferença entre os tipos de teste.)

def test_delete_task_db_success(sample_task_in_db: Task):
    result = client.delete(f"/tasks/{sample_task_in_db.id}")
    assert result.status_code == 204
    assert get_task_db(sample_task_in_db.id) is None

# === Testes de Falha (Unhappy Path) ===

def test_get_task_db_not_found():
    """Testa se buscar uma tarefa com ID inexistente retorna None."""
    found_task = get_task_db(999)
    assert found_task is None

# =================================================================
# TESTES DE INTEGRAÇÃO (API ENDPOINTS)
# =================================================================

# === Testes de Sucesso (Happy Path) ===

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
    # Arrange: cria duas tarefas
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    
    # Act
    response = client.get("/tasks/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_read_one_task_api(sample_task_in_db: Task):
    """Testa a busca de uma tarefa específica via GET /tasks/{task_id}."""
    response = client.get(f"/tasks/{sample_task_in_db.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task_in_db.id
    assert data["title"] == sample_task_in_db.title

def test_update_task_api(sample_task_in_db: Task):
    """Testa a atualização de uma tarefa via PUT /tasks/{task_id}."""
    payload = {"title": "Título Atualizado", "description": "Descrição Nova", "completed": True}
    response = client.put(f"/tasks/{sample_task_in_db.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["completed"] is True

def test_delete_task_api_flow(sample_task_in_db: Task):
    """Testa a deleção de uma tarefa e verifica se ela realmente sumiu."""
    # Deleta a tarefa
    response_delete = client.delete(f"/tasks/{sample_task_in_db.id}")
    assert response_delete.status_code == 204

    # Tenta buscar a tarefa deletada
    response_get = client.get(f"/tasks/{sample_task_in_db.id}")
    assert response_get.status_code == 404

# === Testes de Falha (Unhappy Path) ===

def test_read_one_task_api_not_found():
    """Testa se buscar uma tarefa com ID inexistente retorna 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_update_task_api_not_found():
    """Testa se atualizar uma tarefa com ID inexistente retorna 404."""
    payload = {"title": "Inexistente"}
    response = client.put("/tasks/999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_delete_task_api_not_found():
    """Testa se deletar uma tarefa com ID inexistente retorna 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_create_task_api_invalid_payload():
    """Testa a criação de tarefa com um título muito curto, esperando um erro 422."""
    # O Pydantic/FastAPI deve barrar títulos com menos de 3 caracteres
    payload = {"title": "ab", "description": "Inválido"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 422 # Unprocessable Entity

def test_get_all_tasks_db_empty():
    """Deve retornar lista vazia se não houver tarefas."""
    assert get_all_tasks_db() == []


def test_create_task_db_multiple():
    """IDs devem ser auto-incrementais."""
    t1 = create_task_db(Task(id=0, title="Title1"))
    t2 = create_task_db(Task(id=0, title="Title2"))
    assert t1.id == 1
    assert t2.id == 2


def test_update_task_db_not_found():
    """Atualizar ID inexistente deve retornar None."""
    result = update_task_db(999, Task(id=999, title="Title"))
    assert result is None


def test_delete_task_db_not_found():
    """Deletar ID inexistente deve retornar False."""
    result = delete_task_db(999)
    assert result is False


def test_clear_db_resets():
    """clear_db deve limpar e resetar contador de IDs."""
    create_task_db(Task(id=0, title="Temp"))
    clear_db()
    assert get_all_tasks_db() == []
    t = create_task_db(Task(id=0, title="Novo"))
    assert t.id == 1


# ================================================================
# TESTES EXTRAS - API
# ================================================================

def test_create_task_without_description():
    """Deve aceitar criação sem description."""
    payload = {"title": "Sem desc"}
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["description"] is None


def test_create_task_with_completed_true():
    """Mesmo sendo opcional, deve aceitar completed=True."""
    payload = {"title": "Feita", "description": "ok", "completed": True}
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["completed"] is True


def test_read_all_tasks_empty():
    """GET /tasks/ deve retornar lista vazia se não houver nada."""
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert r.json() == []


def test_update_task_only_title(sample_task_in_db: Task):
    """Atualizar apenas o título deve zerar description."""
    payload = {"title": "Novo Título"}
    r = client.put(f"/tasks/{sample_task_in_db.id}", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Novo Título"
    assert data["description"] is None


def test_update_task_empty_payload(sample_task_in_db: Task):
    """PUT sem dados deve falhar com 422."""
    r = client.put(f"/tasks/{sample_task_in_db.id}", json={})
    assert r.status_code == 422


def test_delete_twice(sample_task_in_db: Task):
    """Deletar duas vezes deve retornar 204 e depois 404."""
    r1 = client.delete(f"/tasks/{sample_task_in_db.id}")
    assert r1.status_code == 204
    r2 = client.delete(f"/tasks/{sample_task_in_db.id}")
    assert r2.status_code == 404


# ================================================================
# TESTES DE CONSISTÊNCIA
# ================================================================

def test_create_two_delete_one_flow():
    """Criar 2, deletar 1, listar deve retornar apenas 1."""
    t1 = client.post("/tasks/", json={"title": "Title1"}).json()
    t2 = client.post("/tasks/", json={"title": "Title2"}).json()
    client.delete(f"/tasks/{t1['id']}")
    r = client.get("/tasks/")
    ids = [t["id"] for t in r.json()]
    assert ids == [t2["id"]]


def test_update_then_get(sample_task_in_db: Task):
    """Atualizar e buscar deve refletir mudança."""
    payload = {"title": "Atualizado"}
    client.put(f"/tasks/{sample_task_in_db.id}", json=payload)
    r = client.get(f"/tasks/{sample_task_in_db.id}")
    assert r.json()["title"] == "Atualizado"


def test_delete_all_and_check():
    """Criar várias, deletar todas, lista deve ficar vazia."""
    ids = []
    for i in range(3):
        ids.append(client.post("/tasks/", json={"title": f"Title{i}"}).json()["id"])
    for tid in ids:
        client.delete(f"/tasks/{tid}")
    r = client.get("/tasks/")
    assert r.json() == []


# ================================================================
# EDGE CASES
# ================================================================

def test_get_task_invalid_id():
    """Buscar ID inválido deve retornar 404."""
    r = client.get("/tasks/0")
    assert r.status_code == 404
    r = client.get("/tasks/-1")
    assert r.status_code == 404


def test_create_task_with_empty_description():
    """Deve aceitar description como string vazia."""
    payload = {"title": "Titulo", "description": ""}
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201
    assert r.json()["description"] == ""


def test_update_task_completed_false(sample_task_in_db: Task):
    """Atualizar completed para False explicitamente deve persistir."""
    payload = {"title": "Teste", "completed": False}
    r = client.put(f"/tasks/{sample_task_in_db.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["completed"] is False


def test_bulk_create_many_ids():
    """Criar várias tarefas em sequência deve gerar IDs únicos e sequenciais."""
    ids = []
    for i in range(5):
        ids.append(client.post("/tasks/", json={"title": f"Title{i}"}).json()["id"])
    assert ids == list(range(1, 6))