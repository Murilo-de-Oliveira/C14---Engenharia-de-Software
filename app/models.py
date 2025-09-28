from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    """
    Modelo de dados para uma tarefa.
    """
    id: int
    title: str = Field(..., min_length=3, max_length=50, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=300, description="Descrição da tarefa")
    completed: bool = False

class TaskCreate(BaseModel):
    """
    Modelo para criação de uma nova tarefa (sem o ID, que será gerado automaticamente).
    """
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    completed: bool = False

"""
Task: Representa uma tarefa com id, title, description e completed. Usamos Field para adicionar validações, 
como o tamanho mínimo e máximo do título.
s
TaskCreate: Um modelo específico para quando o usuário envia dados para criar uma tarefa. Note que ele não 
tem o campo id, pois ele será gerado pela nossa API.
"""