from sqlalchemy.orm import Session
from model.task_model import Task
from schemas.task_schema import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def get_by_id_and_user(self, task_id: int, user_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    def create(self, task_data: TaskCreate, user_id: int) -> Task:
        db_task = Task(**task_data.model_dump(), user_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, db_task: Task, update_data: TaskUpdate) -> Task:
        update_dict = update_data.model_dump(exclude_unset=True) 
        for key, value in update_dict.items():
            setattr(db_task, key, value)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, db_task: Task) -> None:
        self.db.delete(db_task)
        self.db.commit()