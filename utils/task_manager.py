import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class Task:
    def __init__(self, title: str, description: str = ""):
        self.id = self._generate_id()
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.due_date = None
        self.priority = "medium"  # low, medium, high, urgent
        self.status = "pending"  # pending, in_progress, completed, cancelled
        self.assigned_to = ""
        self.project_id = ""
        self.client_id = ""
        self.related_quote_id = ""
        self.tags = []
        self.notes = ""
        self.reminder_date = None
        self.completed_at = None
    
    def _generate_id(self):
        """Genera un ID único para la tarea."""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte la tarea a diccionario."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "project_id": self.project_id,
            "client_id": self.client_id,
            "related_quote_id": self.related_quote_id,
            "tags": self.tags,
            "notes": self.notes,
            "reminder_date": self.reminder_date,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea una tarea desde un diccionario."""
        task = cls(data["title"], data.get("description", ""))
        task.id = data["id"]
        task.created_at = data["created_at"]
        task.updated_at = data["updated_at"]
        task.due_date = data.get("due_date")
        task.priority = data.get("priority", "medium")
        task.status = data.get("status", "pending")
        task.assigned_to = data.get("assigned_to", "")
        task.project_id = data.get("project_id", "")
        task.client_id = data.get("client_id", "")
        task.related_quote_id = data.get("related_quote_id", "")
        task.tags = data.get("tags", [])
        task.notes = data.get("notes", "")
        task.reminder_date = data.get("reminder_date")
        task.completed_at = data.get("completed_at")
        return task
    
    def is_overdue(self):
        """Verifica si la tarea está vencida."""
        if not self.due_date or self.status == "completed":
            return False
        
        try:
            due_date = datetime.fromisoformat(self.due_date)
            return datetime.now() > due_date
        except Exception:
            return False
    
    def is_due_soon(self, days: int = 3):
        """Verifica si la tarea vence pronto."""
        if not self.due_date or self.status == "completed":
            return False
        
        try:
            due_date = datetime.fromisoformat(self.due_date)
            days_until_due = (due_date - datetime.now()).days
            return 0 <= days_until_due <= days
        except Exception:
            return False
    
    def has_reminder(self):
        """Verifica si la tarea tiene un recordatorio."""
        if not self.reminder_date:
            return False
        
        try:
            reminder_date = datetime.fromisoformat(self.reminder_date)
            return datetime.now() >= reminder_date
        except Exception:
            return False

class TaskManager:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Carga las tareas desde el archivo."""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    return [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar tareas: {e}")
                return []
        return []
    
    def save_tasks(self):
        """Guarda las tareas en el archivo."""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar tareas: {e}")
            return False
    
    def create_task(self, title: str, description: str = ""):
        """Crea una nueva tarea."""
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str):
        """Obtiene una tarea por ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks(self, status=None, priority=None, assigned_to=None):
        """Obtiene todas las tareas, opcionalmente filtradas."""
        filtered_tasks = self.tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        
        if assigned_to:
            filtered_tasks = [t for t in filtered_tasks if t.assigned_to == assigned_to]
        
        return filtered_tasks
    
    def update_task(self, task_id: str, **kwargs):
        """Actualiza una tarea con los valores proporcionados."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        # Actualizar fecha de modificación
        task.updated_at = datetime.now().isoformat()
        
        self.save_tasks()
        return True, "Tarea actualizada"
    
    def delete_task(self, task_id: str):
        """Elimina una tarea."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        self.tasks.remove(task)
        self.save_tasks()
        return True, "Tarea eliminada"
    
    def search_tasks(self, query: str):
        """Busca tareas por título, descripción o etiquetas."""
        query = query.lower()
        results = []
        
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower() or
                any(query in tag.lower() for tag in task.tags)):
                results.append(task)
        
        return results
    
    def get_overdue_tasks(self):
        """Obtiene tareas vencidas."""
        return [t for t in self.tasks if t.is_overdue()]
    
    def get_due_soon_tasks(self, days: int = 3):
        """Obtiene tareas que vencen pronto."""
        return [t for t in self.tasks if t.is_due_soon(days)]
    
    def get_tasks_with_reminders(self):
        """Obtiene tareas con recordatorios pendientes."""
        return [t for t in self.tasks if t.has_reminder()]
    
    def complete_task(self, task_id: str):
        """Marca una tarea como completada."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        task.updated_at = datetime.now().isoformat()
        
        self.save_tasks()
        return True, "Tarea completada"
    
    def cancel_task(self, task_id: str):
        """Cancela una tarea."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        task.status = "cancelled"
        task.updated_at = datetime.now().isoformat()
        
        self.save_tasks()
        return True, "Tarea cancelada"
    
    def get_task_statistics(self):
        """Obtiene estadísticas de tareas."""
        if not self.tasks:
            return None
        
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == "completed"])
        pending_tasks = len([t for t in self.tasks if t.status == "pending"])
        in_progress_tasks = len([t for t in self.tasks if t.status == "in_progress"])
        cancelled_tasks = len([t for t in self.tasks if t.status == "cancelled"])
        overdue_tasks = len([t for t in self.tasks if t.is_overdue()])
        
        # Agrupar por prioridad
        priorities = {}
        for task in self.tasks:
            priority = task.priority
            if priority not in priorities:
                priorities[priority] = 0
            priorities[priority] += 1
        
        # Calcular porcentaje de completitud
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        stats = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "cancelled_tasks": cancelled_tasks,
            "overdue_tasks": overdue_tasks,
            "priorities": priorities,
            "completion_rate": completion_rate
        }
        
        return stats
    
    def assign_task(self, task_id: str, assignee: str):
        """Asigna una tarea a un usuario."""
        return self.update_task(task_id, assigned_to=assignee)
    
    def set_task_priority(self, task_id: str, priority: str):
        """Establece la prioridad de una tarea."""
        valid_priorities = ["low", "medium", "high", "urgent"]
        if priority not in valid_priorities:
            return False, f"Prioridad no válida. Valores válidos: {valid_priorities}"
        
        return self.update_task(task_id, priority=priority)
    
    def set_task_status(self, task_id: str, status: str):
        """Establece el estado de una tarea."""
        valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
        if status not in valid_statuses:
            return False, f"Estado no válido. Valores válidos: {valid_statuses}"
        
        # Si se marca como completada, registrar la fecha
        if status == "completed":
            return self.complete_task(task_id)
        
        return self.update_task(task_id, status=status)
    
    def add_task_tag(self, task_id: str, tag: str):
        """Añade una etiqueta a una tarea."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        if tag not in task.tags:
            task.tags.append(tag)
            task.updated_at = datetime.now().isoformat()
            self.save_tasks()
            return True, "Etiqueta añadida"
        
        return False, "La etiqueta ya existe"
    
    def remove_task_tag(self, task_id: str, tag: str):
        """Elimina una etiqueta de una tarea."""
        task = self.get_task(task_id)
        if not task:
            return False, "Tarea no encontrada"
        
        if tag in task.tags:
            task.tags.remove(tag)
            task.updated_at = datetime.now().isoformat()
            self.save_tasks()
            return True, "Etiqueta eliminada"
        
        return False, "La etiqueta no existe"
    
    def get_tasks_by_tag(self, tag: str):
        """Obtiene tareas por etiqueta."""
        return [t for t in self.tasks if tag in t.tags]
    
    def get_tasks_by_project(self, project_id: str):
        """Obtiene tareas asociadas a un proyecto."""
        return [t for t in self.tasks if t.project_id == project_id]
    
    def get_tasks_by_client(self, client_id: str):
        """Obtiene tareas asociadas a un cliente."""
        return [t for t in self.tasks if t.client_id == client_id]
    
    def set_due_date(self, task_id: str, due_date: str):
        """Establece la fecha de vencimiento de una tarea."""
        try:
            # Verificar que la fecha sea válida
            datetime.fromisoformat(due_date)
            return self.update_task(task_id, due_date=due_date)
        except ValueError:
            return False, "Formato de fecha no válido. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
    
    def set_reminder(self, task_id: str, reminder_date: str):
        """Establece un recordatorio para una tarea."""
        try:
            # Verificar que la fecha sea válida
            datetime.fromisoformat(reminder_date)
            return self.update_task(task_id, reminder_date=reminder_date)
        except ValueError:
            return False, "Formato de fecha no válido. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
    
    def get_upcoming_tasks(self, days: int = 7):
        """Obtiene tareas programadas para los próximos días."""
        cutoff_date = datetime.now() + timedelta(days=days)
        upcoming_tasks = []
        
        for task in self.tasks:
            if task.due_date and task.status != "completed":
                try:
                    due_date = datetime.fromisoformat(task.due_date)
                    if datetime.now() <= due_date <= cutoff_date:
                        upcoming_tasks.append(task)
                except Exception:
                    continue
        
        # Ordenar por fecha de vencimiento
        upcoming_tasks.sort(key=lambda x: x.due_date)
        return upcoming_tasks
    
    def export_tasks_to_csv(self, filename: str):
        """Exporta la lista de tareas a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'title', 'description', 'status', 'priority', 'due_date',
                    'assigned_to', 'tags'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for task in self.tasks:
                    writer.writerow({
                        'title': task.title,
                        'description': task.description,
                        'status': task.status,
                        'priority': task.priority,
                        'due_date': task.due_date,
                        'assigned_to': task.assigned_to,
                        'tags': ', '.join(task.tags)
                    })
            
            return True, f"Tareas exportadas a {filename}"
        except Exception as e:
            return False, f"Error al exportar tareas: {str(e)}"
    
    def import_tasks_from_csv(self, filename: str):
        """Importa tareas desde un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0
                
                for row in reader:
                    title = row.get('title', '')
                    description = row.get('description', '')
                    
                    task = Task(title, description)
                    task.status = row.get('status', 'pending')
                    task.priority = row.get('priority', 'medium')
                    task.due_date = row.get('due_date')
                    task.assigned_to = row.get('assigned_to', '')
                    
                    # Procesar etiquetas
                    tags_str = row.get('tags', '')
                    if tags_str:
                        task.tags = [tag.strip() for tag in tags_str.split(',')]
                    
                    self.tasks.append(task)
                    imported_count += 1
                
                self.save_tasks()
                return True, f"{imported_count} tareas importadas exitosamente"
        except Exception as e:
            return False, f"Error al importar tareas: {str(e)}"
