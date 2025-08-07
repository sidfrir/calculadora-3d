import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Project:
    def __init__(self, name: str, description: str = ""):
        self.id = self._generate_id()
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"  # active, completed, archived
        self.quotes = []  # Lista de IDs de cotizaciones
        self.budget = 0.0
        self.actual_cost = 0.0
        self.deadline = None
        self.client = ""
        self.notes = ""
    
    def _generate_id(self):
        """Genera un ID único para el proyecto."""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte el proyecto a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "quotes": self.quotes,
            "budget": self.budget,
            "actual_cost": self.actual_cost,
            "deadline": self.deadline,
            "client": self.client,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un proyecto desde un diccionario."""
        project = cls(data["name"], data.get("description", ""))
        project.id = data["id"]
        project.created_at = data["created_at"]
        project.updated_at = data["updated_at"]
        project.status = data.get("status", "active")
        project.quotes = data.get("quotes", [])
        project.budget = data.get("budget", 0.0)
        project.actual_cost = data.get("actual_cost", 0.0)
        project.deadline = data.get("deadline")
        project.client = data.get("client", "")
        project.notes = data.get("notes", "")
        return project

class ProjectManager:
    def __init__(self, projects_file="projects.json"):
        self.projects_file = projects_file
        self.projects = self.load_projects()
    
    def load_projects(self):
        """Carga los proyectos desde el archivo."""
        if os.path.exists(self.projects_file):
            try:
                with open(self.projects_file, 'r') as f:
                    data = json.load(f)
                    return [Project.from_dict(project_data) for project_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar proyectos: {e}")
                return []
        return []
    
    def save_projects(self):
        """Guarda los proyectos en el archivo."""
        try:
            with open(self.projects_file, 'w') as f:
                json.dump([project.to_dict() for project in self.projects], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar proyectos: {e}")
            return False
    
    def create_project(self, name: str, description: str = ""):
        """Crea un nuevo proyecto."""
        project = Project(name, description)
        self.projects.append(project)
        self.save_projects()
        return project
    
    def get_project(self, project_id: str):
        """Obtiene un proyecto por ID."""
        for project in self.projects:
            if project.id == project_id:
                return project
        return None
    
    def get_projects(self, status=None):
        """Obtiene todos los proyectos, opcionalmente filtrados por estado."""
        if status:
            return [p for p in self.projects if p.status == status]
        return self.projects
    
    def update_project(self, project_id: str, **kwargs):
        """Actualiza un proyecto con los valores proporcionados."""
        project = self.get_project(project_id)
        if not project:
            return False, "Proyecto no encontrado"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        # Actualizar fecha de modificación
        project.updated_at = datetime.now().isoformat()
        
        self.save_projects()
        return True, "Proyecto actualizado"
    
    def delete_project(self, project_id: str):
        """Elimina un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return False, "Proyecto no encontrado"
        
        self.projects.remove(project)
        self.save_projects()
        return True, "Proyecto eliminado"
    
    def add_quote_to_project(self, project_id: str, quote_id: str):
        """Agrega una cotización a un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return False, "Proyecto no encontrado"
        
        if quote_id not in project.quotes:
            project.quotes.append(quote_id)
            project.updated_at = datetime.now().isoformat()
            self.save_projects()
            return True, "Cotización agregada al proyecto"
        
        return False, "La cotización ya está en el proyecto"
    
    def remove_quote_from_project(self, project_id: str, quote_id: str):
        """Elimina una cotización de un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return False, "Proyecto no encontrado"
        
        if quote_id in project.quotes:
            project.quotes.remove(quote_id)
            project.updated_at = datetime.now().isoformat()
            self.save_projects()
            return True, "Cotización eliminada del proyecto"
        
        return False, "La cotización no está en el proyecto"
    
    def get_project_quotes(self, project_id: str):
        """Obtiene las cotizaciones asociadas a un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return None
        
        return project.quotes
    
    def get_project_statistics(self, project_id: str):
        """Obtiene estadísticas de un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return None
        
        stats = {
            "total_quotes": len(project.quotes),
            "budget": project.budget,
            "actual_cost": project.actual_cost,
            "budget_remaining": project.budget - project.actual_cost if project.budget > 0 else 0,
            "budget_utilization": (project.actual_cost / project.budget * 100) if project.budget > 0 else 0,
            "status": project.status,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        
        return stats
    
    def search_projects(self, query: str):
        """Busca proyectos por nombre o descripción."""
        query = query.lower()
        results = []
        
        for project in self.projects:
            if (query in project.name.lower() or 
                query in project.description.lower() or
                query in project.client.lower()):
                results.append(project)
        
        return results
    
    def get_overdue_projects(self):
        """Obtiene proyectos con fechas vencidas."""
        today = datetime.now().date()
        overdue = []
        
        for project in self.projects:
            if project.deadline and project.status == "active":
                try:
                    deadline_date = datetime.fromisoformat(project.deadline).date()
                    if deadline_date < today:
                        overdue.append(project)
                except Exception:
                    continue
        
        return overdue
    
    def get_projects_by_client(self, client_name: str):
        """Obtiene proyectos de un cliente específico."""
        return [p for p in self.projects if p.client.lower() == client_name.lower()]
    
    def archive_project(self, project_id: str):
        """Archiva un proyecto."""
        return self.update_project(project_id, status="archived")
    
    def complete_project(self, project_id: str):
        """Marca un proyecto como completado."""
        return self.update_project(project_id, status="completed")
    
    def get_active_projects_count(self):
        """Obtiene el número de proyectos activos."""
        return len([p for p in self.projects if p.status == "active"])
    
    def get_project_timeline(self, project_id: str):
        """Obtiene la línea de tiempo de un proyecto."""
        project = self.get_project(project_id)
        if not project:
            return None
        
        timeline = [
            {
                "event": "Proyecto creado",
                "date": project.created_at,
                "type": "creation"
            }
        ]
        
        # Añadir eventos de actualización
        if project.updated_at != project.created_at:
            timeline.append({
                "event": "Proyecto actualizado",
                "date": project.updated_at,
                "type": "update"
            })
        
        # Añadir eventos de cambio de estado
        if project.status != "active":
            timeline.append({
                "event": f"Proyecto {project.status}",
                "date": project.updated_at,
                "type": "status_change"
            })
        
        return timeline
