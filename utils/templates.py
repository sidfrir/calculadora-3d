import json
import os

class QuoteTemplate:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = templates_dir
        self.ensure_templates_dir()
    
    def ensure_templates_dir(self):
        """Asegura que el directorio de plantillas exista."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
    
    def save_template(self, name, quote_data):
        """Guarda una cotización como plantilla."""
        try:
            # Eliminar campos que no deberían guardarse en plantillas
            template_data = quote_data.copy()
            fields_to_remove = ['id', 'created_at', 'final_price']
            for field in fields_to_remove:
                template_data.pop(field, None)
            
            # Añadir metadatos de la plantilla
            template_data['_template_name'] = name
            template_data['_template_created'] = __import__('datetime').datetime.now().isoformat()
            
            template_path = os.path.join(self.templates_dir, f"{name}.json")
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Plantilla '{name}' guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar plantilla: {str(e)}"
    
    def load_template(self, name):
        """Carga una plantilla por nombre."""
        try:
            template_path = os.path.join(self.templates_dir, f"{name}.json")
            if not os.path.exists(template_path):
                return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # Eliminar metadatos de la plantilla
            template_data.pop('_template_name', None)
            template_data.pop('_template_created', None)
            
            return template_data
        except Exception as e:
            print(f"Error al cargar plantilla: {str(e)}")
            return None
    
    def list_templates(self):
        """Lista todas las plantillas disponibles."""
        try:
            templates = []
            if os.path.exists(self.templates_dir):
                for filename in os.listdir(self.templates_dir):
                    if filename.endswith('.json'):
                        template_name = filename[:-5]  # Remover .json
                        template_path = os.path.join(self.templates_dir, filename)
                        
                        # Obtener información de la plantilla
                        try:
                            with open(template_path, 'r', encoding='utf-8') as f:
                                template_data = json.load(f)
                            
                            templates.append({
                                "name": template_name,
                                "created": template_data.get('_template_created', ''),
                                "piece_name": template_data.get('piece_name', 'Sin nombre')
                            })
                        except Exception:
                            templates.append({
                                "name": template_name,
                                "created": "Desconocido",
                                "piece_name": "Error al cargar"
                            })
            
            return templates
        except Exception as e:
            print(f"Error al listar plantillas: {str(e)}")
            return []
    
    def delete_template(self, name):
        """Elimina una plantilla por nombre."""
        try:
            template_path = os.path.join(self.templates_dir, f"{name}.json")
            if os.path.exists(template_path):
                os.remove(template_path)
                return True, f"Plantilla '{name}' eliminada exitosamente"
            else:
                return False, f"Plantilla '{name}' no encontrada"
        except Exception as e:
            return False, f"Error al eliminar plantilla: {str(e)}"
    
    def get_template_info(self, name):
        """Obtiene información detallada de una plantilla."""
        try:
            template_path = os.path.join(self.templates_dir, f"{name}.json")
            if not os.path.exists(template_path):
                return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            info = {
                "name": name,
                "created": template_data.get('_template_created', ''),
                "piece_name": template_data.get('piece_name', ''),
                "print_time": template_data.get('print_time', 0),
                "filament_used": template_data.get('filament_used', 0),
                "material_cost": template_data.get('material_cost', 0),
                "labor_cost": template_data.get('labor_cost', 0),
                "profit_margin": template_data.get('profit_margin', 0)
            }
            
            return info
        except Exception as e:
            print(f"Error al obtener información de plantilla: {str(e)}")
            return None
    
    def create_default_templates(self):
        """Crea plantillas predeterminadas útiles."""
        default_templates = [
            {
                "name": "pieza_pequena",
                "data": {
                    "piece_name": "Pieza Pequeña",
                    "print_time": 1.5,
                    "filament_used": 25,
                    "material_cost": 0.75,
                    "labor_cost": 5.0,
                    "profit_margin": 30.0
                }
            },
            {
                "name": "pieza_mediana",
                "data": {
                    "piece_name": "Pieza Mediana",
                    "print_time": 4.0,
                    "filament_used": 100,
                    "material_cost": 3.0,
                    "labor_cost": 15.0,
                    "profit_margin": 30.0
                }
            },
            {
                "name": "pieza_grande",
                "data": {
                    "piece_name": "Pieza Grande",
                    "print_time": 12.0,
                    "filament_used": 300,
                    "material_cost": 9.0,
                    "labor_cost": 40.0,
                    "profit_margin": 30.0
                }
            }
        ]
        
        results = []
        for template in default_templates:
            success, message = self.save_template(template["name"], template["data"])
            results.append({"name": template["name"], "success": success, "message": message})
        
        return results
    
    def apply_template_to_quote(self, template_name, quote_data=None):
        """Aplica una plantilla a una cotización existente o crea una nueva."""
        template = self.load_template(template_name)
        if not template:
            return None
        
        if quote_data is None:
            quote_data = {}
        
        # Aplicar datos de la plantilla a la cotización
        for key, value in template.items():
            if key not in quote_data or quote_data[key] is None or quote_data[key] == '':
                quote_data[key] = value
        
        return quote_data
