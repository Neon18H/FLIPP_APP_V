from extensions import db
from tasks.models import Task, TaskComment

def create_task(data, creator_id):
    t = Task(created_by=creator_id, **data)
    db.session.add(t)
    db.session.commit()
    return t

def update_task(tid, data):
    t = Task.query.filter_by(id=tid, is_deleted=False).first_or_404()
    for k,v in data.items(): setattr(t,k,v)
    db.session.commit(); return t

def delete_task(tid):
    t = Task.query.filter_by(id=tid, is_deleted=False).first_or_404()
    t.is_deleted = True
    db.session.commit()

def list_tasks(client_id=None, assignee_id=None, status=None, q=None):
    query = Task.query.filter_by(is_deleted=False)
    if client_id: query = query.filter_by(client_id=client_id)
    if assignee_id: query = query.filter_by(assignee_id=assignee_id) if assignee_id != "me" else query
    if status: query = query.filter_by(status=status)
    if q: query = query.filter(Task.title.ilike(f"%{q}%"))
    return query.order_by(Task.created_at.desc()).all()

def get_task(tid):
    return Task.query.filter_by(id=tid, is_deleted=False).first_or_404()

def change_status(tid, status):
    t = get_task(tid); t.status = status; db.session.commit(); return t

def add_comment(task_id, author_id, content):
    c = TaskComment(task_id=task_id, author_id=author_id, content=content)
    db.session.add(c); db.session.commit(); return c

def list_comments(task_id):
    return TaskComment.query.filter_by(task_id=task_id, is_deleted=False).order_by(TaskComment.created_at.asc()).all()
