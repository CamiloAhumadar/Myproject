from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskUpdate
from model.user_model import User

class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)

    def list_tasks(self, current_user: User):
        return self.task_repo.get_all_by_user(current_user.id)

    def create_task(self, task_data: TaskCreate, current_user: User):
        return self.task_repo.create(task_data, current_user.id)

    def get_task(self, task_id: int, current_user: User):
        task = self.task_repo.get_by_id_and_user(task_id, current_user.id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarea no encontrada"
            )
        return task

    def update_task(self, task_id: int, update_data: TaskUpdate, current_user: User):
        task = self.get_task(task_id, current_user) 
        return self.task_repo.update(task, update_data)

    def delete_task(self, task_id: int, current_user: User):
        task = self.get_task(task_id, current_user) 
        self.task_repo.delete(task)