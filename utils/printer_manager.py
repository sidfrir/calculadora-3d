import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Printer:
    def __init__(self, name: str, model: str, manufacturer: str):
        self.id = self._generate_id()
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"  # active, maintenance, retired
        self.purchase_date = None
        self.purchase_price = 0.0
        self.hourly_rate = 0.0
        self.power_consumption = 0.0  # Watts
        self.build_volume = ""  # e.g., "200x200x200mm"
        self.technology = "FDM"  # FDM, SLA, SLS, etc.
        self.nozzle_diameter = 0.4  # mm
        self.layer_height_range = "0.05-0.3mm"
        self.materials_supported = []  # Lista de tipos de material
        self.maintenance_schedule = 0  # Horas entre mantenimientos
        self.last_maintenance = None
        self.total_print_hours = 0.0
        self.notes = ""
        self.location = ""
    
    def _generate_id(self):
        """Genera un ID único para la impresora."""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte la impresora a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "purchase_date": self.purchase_date,
            "purchase_price": self.purchase_price,
            "hourly_rate": self.hourly_rate,
            "power_consumption": self.power_consumption,
            "build_volume": self.build_volume,
            "technology": self.technology,
            "nozzle_diameter": self.nozzle_diameter,
            "layer_height_range": self.layer_height_range,
            "materials_supported": self.materials_supported,
            "maintenance_schedule": self.maintenance_schedule,
            "last_maintenance": self.last_maintenance,
            "total_print_hours": self.total_print_hours,
            "notes": self.notes,
            "location": self.location
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea una impresora desde un diccionario."""
        printer = cls(
            data["name"], 
            data["model"], 
            data["manufacturer"]
        )
        printer.id = data["id"]
        printer.created_at = data["created_at"]
        printer.updated_at = data["updated_at"]
        printer.status = data.get("status", "active")
        printer.purchase_date = data.get("purchase_date")
        printer.purchase_price = data.get("purchase_price", 0.0)
        printer.hourly_rate = data.get("hourly_rate", 0.0)
        printer.power_consumption = data.get("power_consumption", 0.0)
        printer.build_volume = data.get("build_volume", "")
        printer.technology = data.get("technology", "FDM")
        printer.nozzle_diameter = data.get("nozzle_diameter", 0.4)
        printer.layer_height_range = data.get("layer_height_range", "0.05-0.3mm")
        printer.materials_supported = data.get("materials_supported", [])
        printer.maintenance_schedule = data.get("maintenance_schedule", 0)
        printer.last_maintenance = data.get("last_maintenance")
        printer.total_print_hours = data.get("total_print_hours", 0.0)
        printer.notes = data.get("notes", "")
        printer.location = data.get("location", "")
        return printer
    
    def calculate_electricity_cost(self, print_hours: float, electricity_price_per_kwh: float):
        """Calcula el costo de electricidad para un tiempo de impresión dado."""
        kwh = (self.power_consumption / 1000) * print_hours
        return kwh * electricity_price_per_kwh
    
    def is_due_for_maintenance(self):
        """Verifica si la impresora necesita mantenimiento."""
        if not self.last_maintenance or self.maintenance_schedule <= 0:
            return False
        
        try:
            last_maintenance_date = datetime.fromisoformat(self.last_maintenance)
            hours_since_maintenance = self.total_print_hours
            
            # Si tenemos un registro de horas totales, podríamos calcular
            # desde la última fecha de mantenimiento, pero para simplificar
            # asumimos que total_print_hours es acumulativo
            return self.total_print_hours >= self.maintenance_schedule
        except Exception:
            return False
    
    def get_utilization_rate(self, period_days: int = 30):
        """Calcula la tasa de utilización de la impresora en un período."""
        # Esta función requeriría datos históricos de uso
        # Por ahora devolvemos un valor basado en horas totales
        hours_in_period = period_days * 24
        if hours_in_period > 0:
            return min((self.total_print_hours / hours_in_period) * 100, 100)
        return 0

class PrinterManager:
    def __init__(self, printers_file="printers.json"):
        self.printers_file = printers_file
        self.printers = self.load_printers()
    
    def load_printers(self):
        """Carga las impresoras desde el archivo."""
        if os.path.exists(self.printers_file):
            try:
                with open(self.printers_file, 'r') as f:
                    data = json.load(f)
                    return [Printer.from_dict(printer_data) for printer_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar impresoras: {e}")
                return []
        return []
    
    def save_printers(self):
        """Guarda las impresoras en el archivo."""
        try:
            with open(self.printers_file, 'w') as f:
                json.dump([printer.to_dict() for printer in self.printers], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar impresoras: {e}")
            return False
    
    def add_printer(self, name: str, model: str, manufacturer: str):
        """Añade una nueva impresora."""
        # Verificar si la impresora ya existe
        if self.get_printer_by_name(name):
            return False, "La impresora ya existe"
        
        printer = Printer(name, model, manufacturer)
        self.printers.append(printer)
        self.save_printers()
        return printer, "Impresora añadida exitosamente"
    
    def get_printer(self, printer_id: str):
        """Obtiene una impresora por ID."""
        for printer in self.printers:
            if printer.id == printer_id:
                return printer
        return None
    
    def get_printer_by_name(self, name: str):
        """Obtiene una impresora por nombre."""
        for printer in self.printers:
            if printer.name.lower() == name.lower():
                return printer
        return None
    
    def get_printers(self, status=None, technology=None):
        """Obtiene todas las impresoras, opcionalmente filtradas por estado o tecnología."""
        filtered_printers = self.printers
        
        if status:
            filtered_printers = [p for p in filtered_printers if p.status == status]
        
        if technology:
            filtered_printers = [p for p in filtered_printers if p.technology == technology]
        
        return filtered_printers
    
    def update_printer(self, printer_id: str, **kwargs):
        """Actualiza una impresora con los valores proporcionados."""
        printer = self.get_printer(printer_id)
        if not printer:
            return False, "Impresora no encontrada"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(printer, key):
                setattr(printer, key, value)
        
        # Actualizar fecha de modificación
        printer.updated_at = datetime.now().isoformat()
        
        self.save_printers()
        return True, "Impresora actualizada"
    
    def delete_printer(self, printer_id: str):
        """Elimina una impresora."""
        printer = self.get_printer(printer_id)
        if not printer:
            return False, "Impresora no encontrada"
        
        self.printers.remove(printer)
        self.save_printers()
        return True, "Impresora eliminada"
    
    def search_printers(self, query: str):
        """Busca impresoras por nombre, modelo o fabricante."""
        query = query.lower()
        results = []
        
        for printer in self.printers:
            if (query in printer.name.lower() or 
                query in printer.model.lower() or
                query in printer.manufacturer.lower() or
                query in printer.location.lower()):
                results.append(printer)
        
        return results
    
    def get_printer_statistics(self):
        """Obtiene estadísticas de impresoras."""
        if not self.printers:
            return None
        
        total_printers = len(self.printers)
        active_printers = len([p for p in self.printers if p.status == "active"])
        maintenance_printers = len([p for p in self.printers if p.status == "maintenance"])
        retired_printers = len([p for p in self.printers if p.status == "retired"])
        
        # Agrupar por tecnología
        technologies = {}
        for printer in self.printers:
            tech = printer.technology
            if tech not in technologies:
                technologies[tech] = 0
            technologies[tech] += 1
        
        # Calcular horas totales de impresión
        total_print_hours = sum(p.total_print_hours for p in self.printers)
        
        # Impresoras que necesitan mantenimiento
        maintenance_due_printers = [p for p in self.printers if p.is_due_for_maintenance()]
        
        stats = {
            "total_printers": total_printers,
            "active_printers": active_printers,
            "maintenance_printers": maintenance_printers,
            "retired_printers": retired_printers,
            "technologies": technologies,
            "total_print_hours": total_print_hours,
            "maintenance_due_count": len(maintenance_due_printers),
            "maintenance_due_printers": [p.name for p in maintenance_due_printers]
        }
        
        return stats
    
    def update_print_hours(self, printer_id: str, hours: float):
        """Actualiza las horas de impresión de una impresora."""
        printer = self.get_printer(printer_id)
        if not printer:
            return False, "Impresora no encontrada"
        
        printer.total_print_hours += hours
        printer.updated_at = datetime.now().isoformat()
        self.save_printers()
        
        # Verificar si necesita mantenimiento
        if printer.is_due_for_maintenance():
            return True, f"Horas actualizadas. ¡Alerta! La impresora necesita mantenimiento"
        
        return True, f"Horas actualizadas: {printer.total_print_hours} horas totales"
    
    def record_maintenance(self, printer_id: str):
        """Registra el mantenimiento de una impresora."""
        printer = self.get_printer(printer_id)
        if not printer:
            return False, "Impresora no encontrada"
        
        printer.last_maintenance = datetime.now().isoformat()
        printer.status = "active"
        printer.updated_at = datetime.now().isoformat()
        self.save_printers()
        
        return True, "Mantenimiento registrado exitosamente"
    
    def get_maintenance_due_printers(self):
        """Obtiene impresoras que necesitan mantenimiento."""
        return [p for p in self.printers if p.is_due_for_maintenance()]
    
    def get_printers_by_technology(self, technology: str):
        """Obtiene impresoras de una tecnología específica."""
        return [p for p in self.printers if p.technology == technology]
    
    def calculate_printer_cost(self, printer_id: str, print_hours: float, electricity_price_per_kwh: float):
        """Calcula el costo de uso de una impresora para un tiempo dado."""
        printer = self.get_printer(printer_id)
        if not printer:
            return None, "Impresora no encontrada"
        
        # Costo de mano de obra (basado en tarifa horaria)
        labor_cost = printer.hourly_rate * print_hours
        
        # Costo de electricidad
        electricity_cost = printer.calculate_electricity_cost(print_hours, electricity_price_per_kwh)
        
        total_cost = labor_cost + electricity_cost
        
        cost_breakdown = {
            "labor_cost": labor_cost,
            "electricity_cost": electricity_cost,
            "total_cost": total_cost
        }
        
        return cost_breakdown, f"Costo calculado: ${total_cost:.2f}"
    
    def set_printer_status(self, printer_id: str, status: str):
        """Establece el estado de una impresora."""
        valid_statuses = ["active", "maintenance", "retired"]
        if status not in valid_statuses:
            return False, f"Estado no válido. Estados válidos: {valid_statuses}"
        
        return self.update_printer(printer_id, status=status)
    
    def get_active_printers_count(self):
        """Obtiene el número de impresoras activas."""
        return len([p for p in self.printers if p.status == "active"])
    
    def export_printers_to_csv(self, filename: str):
        """Exporta la lista de impresoras a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'name', 'model', 'manufacturer', 'status', 'technology',
                    'total_print_hours', 'location'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for printer in self.printers:
                    writer.writerow({
                        'name': printer.name,
                        'model': printer.model,
                        'manufacturer': printer.manufacturer,
                        'status': printer.status,
                        'technology': printer.technology,
                        'total_print_hours': printer.total_print_hours,
                        'location': printer.location
                    })
            
            return True, f"Impresoras exportadas a {filename}"
        except Exception as e:
            return False, f"Error al exportar impresoras: {str(e)}"
    
    def import_printers_from_csv(self, filename: str):
        """Importa impresoras desde un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0
                
                for row in reader:
                    name = row.get('name', '')
                    model = row.get('model', '')
                    manufacturer = row.get('manufacturer', '')
                    
                    # Verificar si la impresora ya existe
                    if not self.get_printer_by_name(name):
                        printer = Printer(name, model, manufacturer)
                        printer.status = row.get('status', 'active')
                        printer.technology = row.get('technology', 'FDM')
                        printer.total_print_hours = float(row.get('total_print_hours', 0))
                        printer.location = row.get('location', '')
                        
                        self.printers.append(printer)
                        imported_count += 1
                
                self.save_printers()
                return True, f"{imported_count} impresoras importadas exitosamente"
        except Exception as e:
            return False, f"Error al importar impresoras: {str(e)}"
