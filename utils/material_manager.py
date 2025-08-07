import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Material:
    def __init__(self, name: str, material_type: str, price_per_kg: float):
        self.id = self._generate_id()
        self.name = name
        self.material_type = material_type  # PLA, ABS, PETG, TPU, etc.
        self.price_per_kg = price_per_kg
        self.density = self._get_default_density(material_type)  # g/cm³
        self.color = ""
        self.manufacturer = ""
        self.supplier = ""
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"  # active, discontinued
        self.stock_quantity = 0.0  # kg
        self.min_stock_alert = 1.0  # kg
        self.notes = ""
        self.properties = self._get_default_properties(material_type)
    
    def _generate_id(self):
        """Genera un ID único para el material."""
        import uuid
        return str(uuid.uuid4())
    
    def _get_default_density(self, material_type: str):
        """Obtiene la densidad por defecto según el tipo de material."""
        densities = {
            "PLA": 1.24,
            "ABS": 1.04,
            "PETG": 1.27,
            "TPU": 1.21,
            "Nylon": 1.15,
            "PC": 1.20,
            "Wood Fill": 1.28,
            "Metal Fill": 3.50
        }
        return densities.get(material_type, 1.24)
    
    def _get_default_properties(self, material_type: str):
        """Obtiene propiedades por defecto según el tipo de material."""
        properties = {
            "PLA": {
                "printing_temp": "190-220°C",
                "bed_temp": "50-60°C",
                "diameter": "1.75mm",
                "finish": "Glossy",
                "strength": "Medium"
            },
            "ABS": {
                "printing_temp": "220-250°C",
                "bed_temp": "90-110°C",
                "diameter": "1.75mm",
                "finish": "Matte",
                "strength": "High"
            },
            "PETG": {
                "printing_temp": "220-250°C",
                "bed_temp": "70-80°C",
                "diameter": "1.75mm",
                "finish": "Semi-transparent",
                "strength": "High"
            },
            "TPU": {
                "printing_temp": "220-240°C",
                "bed_temp": "50-60°C",
                "diameter": "1.75mm",
                "finish": "Flexible",
                "strength": "Flexible"
            }
        }
        return properties.get(material_type, {})
    
    def to_dict(self):
        """Convierte el material a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "material_type": self.material_type,
            "price_per_kg": self.price_per_kg,
            "density": self.density,
            "color": self.color,
            "manufacturer": self.manufacturer,
            "supplier": self.supplier,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "stock_quantity": self.stock_quantity,
            "min_stock_alert": self.min_stock_alert,
            "notes": self.notes,
            "properties": self.properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un material desde un diccionario."""
        material = cls(
            data["name"], 
            data["material_type"], 
            data["price_per_kg"]
        )
        material.id = data["id"]
        material.density = data.get("density", material._get_default_density(data["material_type"]))
        material.color = data.get("color", "")
        material.manufacturer = data.get("manufacturer", "")
        material.supplier = data.get("supplier", "")
        material.created_at = data["created_at"]
        material.updated_at = data["updated_at"]
        material.status = data.get("status", "active")
        material.stock_quantity = data.get("stock_quantity", 0.0)
        material.min_stock_alert = data.get("min_stock_alert", 1.0)
        material.notes = data.get("notes", "")
        material.properties = data.get("properties", material._get_default_properties(data["material_type"]))
        return material
    
    def calculate_cost(self, weight_grams: float):
        """Calcula el costo del material para un peso dado en gramos."""
        weight_kg = weight_grams / 1000
        return weight_kg * self.price_per_kg
    
    def is_low_stock(self):
        """Verifica si el material está bajo en stock."""
        return self.stock_quantity <= self.min_stock_alert

class MaterialManager:
    def __init__(self, materials_file="materials.json"):
        self.materials_file = materials_file
        self.materials = self.load_materials()
    
    def load_materials(self):
        """Carga los materiales desde el archivo."""
        if os.path.exists(self.materials_file):
            try:
                with open(self.materials_file, 'r') as f:
                    data = json.load(f)
                    return [Material.from_dict(material_data) for material_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar materiales: {e}")
                return []
        return []
    
    def save_materials(self):
        """Guarda los materiales en el archivo."""
        try:
            with open(self.materials_file, 'w') as f:
                json.dump([material.to_dict() for material in self.materials], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar materiales: {e}")
            return False
    
    def add_material(self, name: str, material_type: str, price_per_kg: float):
        """Añade un nuevo material."""
        # Verificar si el material ya existe
        if self.get_material_by_name(name):
            return False, "El material ya existe"
        
        material = Material(name, material_type, price_per_kg)
        self.materials.append(material)
        self.save_materials()
        return material, "Material añadido exitosamente"
    
    def get_material(self, material_id: str):
        """Obtiene un material por ID."""
        for material in self.materials:
            if material.id == material_id:
                return material
        return None
    
    def get_material_by_name(self, name: str):
        """Obtiene un material por nombre."""
        for material in self.materials:
            if material.name.lower() == name.lower():
                return material
        return None
    
    def get_materials(self, material_type=None, status=None):
        """Obtiene todos los materiales, opcionalmente filtrados por tipo o estado."""
        filtered_materials = self.materials
        
        if material_type:
            filtered_materials = [m for m in filtered_materials if m.material_type == material_type]
        
        if status:
            filtered_materials = [m for m in filtered_materials if m.status == status]
        
        return filtered_materials
    
    def update_material(self, material_id: str, **kwargs):
        """Actualiza un material con los valores proporcionados."""
        material = self.get_material(material_id)
        if not material:
            return False, "Material no encontrado"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(material, key):
                setattr(material, key, value)
        
        # Actualizar fecha de modificación
        material.updated_at = datetime.now().isoformat()
        
        self.save_materials()
        return True, "Material actualizado"
    
    def delete_material(self, material_id: str):
        """Elimina un material."""
        material = self.get_material(material_id)
        if not material:
            return False, "Material no encontrado"
        
        self.materials.remove(material)
        self.save_materials()
        return True, "Material eliminado"
    
    def search_materials(self, query: str):
        """Busca materiales por nombre, tipo o fabricante."""
        query = query.lower()
        results = []
        
        for material in self.materials:
            if (query in material.name.lower() or 
                query in material.material_type.lower() or
                query in material.manufacturer.lower() or
                query in material.color.lower()):
                results.append(material)
        
        return results
    
    def get_material_statistics(self):
        """Obtiene estadísticas de materiales."""
        if not self.materials:
            return None
        
        total_materials = len(self.materials)
        active_materials = len([m for m in self.materials if m.status == "active"])
        discontinued_materials = total_materials - active_materials
        
        # Agrupar por tipo de material
        material_types = {}
        for material in self.materials:
            material_type = material.material_type
            if material_type not in material_types:
                material_types[material_type] = 0
            material_types[material_type] += 1
        
        # Calcular valor total del inventario
        total_inventory_value = sum(m.stock_quantity * m.price_per_kg for m in self.materials)
        
        # Materiales con bajo stock
        low_stock_materials = [m for m in self.materials if m.is_low_stock()]
        
        stats = {
            "total_materials": total_materials,
            "active_materials": active_materials,
            "discontinued_materials": discontinued_materials,
            "material_types": material_types,
            "total_inventory_value": total_inventory_value,
            "low_stock_count": len(low_stock_materials),
            "low_stock_materials": [m.name for m in low_stock_materials]
        }
        
        return stats
    
    def update_stock(self, material_id: str, quantity: float, operation: str = "add"):
        """Actualiza el stock de un material."""
        material = self.get_material(material_id)
        if not material:
            return False, "Material no encontrado"
        
        if operation == "add":
            material.stock_quantity += quantity
        elif operation == "remove":
            if material.stock_quantity >= quantity:
                material.stock_quantity -= quantity
            else:
                return False, "Stock insuficiente"
        elif operation == "set":
            material.stock_quantity = quantity
        else:
            return False, "Operación no válida"
        
        material.updated_at = datetime.now().isoformat()
        self.save_materials()
        
        # Verificar si el stock está bajo después de la actualización
        if material.is_low_stock():
            return True, f"Stock actualizado. ¡Alerta! Stock bajo: {material.stock_quantity} kg"
        
        return True, f"Stock actualizado: {material.stock_quantity} kg"
    
    def get_low_stock_materials(self):
        """Obtiene materiales con bajo stock."""
        return [m for m in self.materials if m.is_low_stock()]
    
    def get_material_types(self):
        """Obtiene los tipos de materiales disponibles."""
        types = list(set(m.material_type for m in self.materials))
        return sorted(types)
    
    def calculate_material_cost(self, material_id: str, weight_grams: float):
        """Calcula el costo de un material para un peso dado."""
        material = self.get_material(material_id)
        if not material:
            return None, "Material no encontrado"
        
        cost = material.calculate_cost(weight_grams)
        return cost, f"Costo calculado: ${cost:.2f}"
    
    def get_materials_by_supplier(self, supplier: str):
        """Obtiene materiales de un proveedor específico."""
        return [m for m in self.materials if m.supplier.lower() == supplier.lower()]
    
    def export_materials_to_csv(self, filename: str):
        """Exporta la lista de materiales a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'name', 'material_type', 'price_per_kg', 'stock_quantity', 
                    'manufacturer', 'supplier', 'status'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for material in self.materials:
                    writer.writerow({
                        'name': material.name,
                        'material_type': material.material_type,
                        'price_per_kg': material.price_per_kg,
                        'stock_quantity': material.stock_quantity,
                        'manufacturer': material.manufacturer,
                        'supplier': material.supplier,
                        'status': material.status
                    })
            
            return True, f"Materiales exportados a {filename}"
        except Exception as e:
            return False, f"Error al exportar materiales: {str(e)}"
    
    def import_materials_from_csv(self, filename: str):
        """Importa materiales desde un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0
                
                for row in reader:
                    name = row.get('name', '')
                    material_type = row.get('material_type', '')
                    price_per_kg = float(row.get('price_per_kg', 0))
                    
                    # Verificar si el material ya existe
                    if not self.get_material_by_name(name):
                        material = Material(name, material_type, price_per_kg)
                        material.manufacturer = row.get('manufacturer', '')
                        material.supplier = row.get('supplier', '')
                        material.stock_quantity = float(row.get('stock_quantity', 0))
                        material.status = row.get('status', 'active')
                        
                        self.materials.append(material)
                        imported_count += 1
                
                self.save_materials()
                return True, f"{imported_count} materiales importados exitosamente"
        except Exception as e:
            return False, f"Error al importar materiales: {str(e)}"
