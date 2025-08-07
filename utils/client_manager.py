import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Client:
    def __init__(self, name: str, email: str = "", phone: str = ""):
        self.id = self._generate_id()
        self.name = name
        self.email = email
        self.phone = phone
        self.company = ""
        self.address = ""
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"  # active, inactive
        self.total_spent = 0.0
        self.quote_count = 0
        self.last_contact = None
        self.notes = ""
        self.preferred_filament = ""
        self.discount_rate = 0.0  # Porcentaje de descuento
    
    def _generate_id(self):
        """Genera un ID único para el cliente."""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte el cliente a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "address": self.address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "total_spent": self.total_spent,
            "quote_count": self.quote_count,
            "last_contact": self.last_contact,
            "notes": self.notes,
            "preferred_filament": self.preferred_filament,
            "discount_rate": self.discount_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un cliente desde un diccionario."""
        client = cls(data["name"], data.get("email", ""), data.get("phone", ""))
        client.id = data["id"]
        client.company = data.get("company", "")
        client.address = data.get("address", "")
        client.created_at = data["created_at"]
        client.updated_at = data["updated_at"]
        client.status = data.get("status", "active")
        client.total_spent = data.get("total_spent", 0.0)
        client.quote_count = data.get("quote_count", 0)
        client.last_contact = data.get("last_contact")
        client.notes = data.get("notes", "")
        client.preferred_filament = data.get("preferred_filament", "")
        client.discount_rate = data.get("discount_rate", 0.0)
        return client

class ClientManager:
    def __init__(self, clients_file="clients.json"):
        self.clients_file = clients_file
        self.clients = self.load_clients()
    
    def load_clients(self):
        """Carga los clientes desde el archivo."""
        if os.path.exists(self.clients_file):
            try:
                with open(self.clients_file, 'r') as f:
                    data = json.load(f)
                    return [Client.from_dict(client_data) for client_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar clientes: {e}")
                return []
        return []
    
    def save_clients(self):
        """Guarda los clientes en el archivo."""
        try:
            with open(self.clients_file, 'w') as f:
                json.dump([client.to_dict() for client in self.clients], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar clientes: {e}")
            return False
    
    def create_client(self, name: str, email: str = "", phone: str = ""):
        """Crea un nuevo cliente."""
        # Verificar si el cliente ya existe
        if self.get_client_by_name(name):
            return False, "El cliente ya existe"
        
        client = Client(name, email, phone)
        self.clients.append(client)
        self.save_clients()
        return client, "Cliente creado exitosamente"
    
    def get_client(self, client_id: str):
        """Obtiene un cliente por ID."""
        for client in self.clients:
            if client.id == client_id:
                return client
        return None
    
    def get_client_by_name(self, name: str):
        """Obtiene un cliente por nombre."""
        for client in self.clients:
            if client.name.lower() == name.lower():
                return client
        return None
    
    def get_clients(self, status=None):
        """Obtiene todos los clientes, opcionalmente filtrados por estado."""
        if status:
            return [c for c in self.clients if c.status == status]
        return self.clients
    
    def update_client(self, client_id: str, **kwargs):
        """Actualiza un cliente con los valores proporcionados."""
        client = self.get_client(client_id)
        if not client:
            return False, "Cliente no encontrado"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(client, key):
                setattr(client, key, value)
        
        # Actualizar fecha de modificación
        client.updated_at = datetime.now().isoformat()
        
        self.save_clients()
        return True, "Cliente actualizado"
    
    def delete_client(self, client_id: str):
        """Elimina un cliente."""
        client = self.get_client(client_id)
        if not client:
            return False, "Cliente no encontrado"
        
        self.clients.remove(client)
        self.save_clients()
        return True, "Cliente eliminado"
    
    def search_clients(self, query: str):
        """Busca clientes por nombre, email o compañía."""
        query = query.lower()
        results = []
        
        for client in self.clients:
            if (query in client.name.lower() or 
                query in client.email.lower() or
                query in client.company.lower() or
                query in client.phone.lower()):
                results.append(client)
        
        return results
    
    def get_client_statistics(self, client_id: str):
        """Obtiene estadísticas de un cliente."""
        client = self.get_client(client_id)
        if not client:
            return None
        
        stats = {
            "total_spent": client.total_spent,
            "quote_count": client.quote_count,
            "avg_order_value": client.total_spent / client.quote_count if client.quote_count > 0 else 0,
            "preferred_filament": client.preferred_filament,
            "discount_rate": client.discount_rate,
            "status": client.status,
            "created_at": client.created_at,
            "last_contact": client.last_contact
        }
        
        return stats
    
    def update_client_spending(self, client_id: str, amount: float):
        """Actualiza el gasto total de un cliente."""
        client = self.get_client(client_id)
        if not client:
            return False, "Cliente no encontrado"
        
        client.total_spent += amount
        client.quote_count += 1
        client.updated_at = datetime.now().isoformat()
        
        self.save_clients()
        return True, "Gasto del cliente actualizado"
    
    def get_top_clients(self, limit: int = 10):
        """Obtiene los clientes con mayor gasto."""
        sorted_clients = sorted(self.clients, key=lambda x: x.total_spent, reverse=True)
        return sorted_clients[:limit]
    
    def get_clients_by_spending_range(self, min_amount: float, max_amount: float):
        """Obtiene clientes dentro de un rango de gasto."""
        return [c for c in self.clients 
                if min_amount <= c.total_spent <= max_amount]
    
    def add_client_note(self, client_id: str, note: str):
        """Añade una nota al cliente."""
        client = self.get_client(client_id)
        if not client:
            return False, "Cliente no encontrado"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_entry = f"[{timestamp}] {note}"
        
        if client.notes:
            client.notes += "\n" + note_entry
        else:
            client.notes = note_entry
        
        client.updated_at = datetime.now().isoformat()
        self.save_clients()
        return True, "Nota añadida al cliente"
    
    def update_last_contact(self, client_id: str):
        """Actualiza la fecha del último contacto con el cliente."""
        client = self.get_client(client_id)
        if not client:
            return False, "Cliente no encontrado"
        
        client.last_contact = datetime.now().isoformat()
        client.updated_at = datetime.now().isoformat()
        self.save_clients()
        return True, "Fecha de último contacto actualizada"
    
    def get_inactive_clients(self, days: int = 90):
        """Obtiene clientes inactivos (sin contacto en X días)."""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        inactive_clients = []
        
        for client in self.clients:
            if client.status == "active":
                if client.last_contact:
                    try:
                        last_contact = datetime.fromisoformat(client.last_contact)
                        if last_contact < cutoff_date:
                            inactive_clients.append(client)
                    except Exception:
                        # Si hay error al parsear la fecha, considerar inactivo
                        inactive_clients.append(client)
                else:
                    # Si no hay fecha de último contacto, considerar inactivo
                    inactive_clients.append(client)
        
        return inactive_clients
    
    def apply_discount_to_client(self, client_id: str, discount_rate: float):
        """Aplica un descuento a un cliente."""
        return self.update_client(client_id, discount_rate=discount_rate)
    
    def get_client_count(self):
        """Obtiene el número total de clientes."""
        return len(self.clients)
    
    def get_active_clients_count(self):
        """Obtiene el número de clientes activos."""
        return len([c for c in self.clients if c.status == "active"])
    
    def export_clients_to_csv(self, filename: str):
        """Exporta la lista de clientes a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'email', 'phone', 'company', 'total_spent', 'quote_count', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for client in self.clients:
                    writer.writerow({
                        'name': client.name,
                        'email': client.email,
                        'phone': client.phone,
                        'company': client.company,
                        'total_spent': client.total_spent,
                        'quote_count': client.quote_count,
                        'status': client.status
                    })
            
            return True, f"Clientes exportados a {filename}"
        except Exception as e:
            return False, f"Error al exportar clientes: {str(e)}"
