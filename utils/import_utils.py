import csv
import json
import xml.etree.ElementTree as ET

class ImportUtils:
    @staticmethod
    def import_from_csv(file_path):
        """Importa cotizaciones desde un archivo CSV."""
        try:
            quotes = []
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    quotes.append({
                        'id': int(row['id']),
                        'piece_name': row['piece_name'],
                        'print_time': float(row['print_time']),
                        'filament_used': float(row['filament_used']),
                        'material_cost': float(row['material_cost']),
                        'labor_cost': float(row['labor_cost']),
                        'total_cost': float(row['total_cost']),
                        'profit_margin': float(row['profit_margin']),
                        'final_price': float(row['final_price']),
                        'created_at': row['created_at']
                    })
            return quotes
        except Exception as e:
            print(f"Error al importar desde CSV: {e}")
            return []
    
    @staticmethod
    def import_from_json(file_path):
        """Importa cotizaciones desde un archivo JSON."""
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                quotes = json.load(jsonfile)
            return quotes
        except Exception as e:
            print(f"Error al importar desde JSON: {e}")
            return []
    
    @staticmethod
    def import_from_xml(file_path):
        """Importa cotizaciones desde un archivo XML."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            quotes = []
            for quote_elem in root.findall('quote'):
                quote = {}
                for child in quote_elem:
                    if child.tag in ['id', 'print_time', 'filament_used', 
                                   'material_cost', 'labor_cost', 'total_cost', 
                                   'profit_margin', 'final_price']:
                        quote[child.tag] = float(child.text) if '.' in child.text else int(child.text)
                    else:
                        quote[child.tag] = child.text
                quotes.append(quote)
            
            return quotes
        except Exception as e:
            print(f"Error al importar desde XML: {e}")
            return []
    
    @staticmethod
    def validate_quote_data(quote_data):
        """Valida los datos de una cotización importada."""
        required_fields = ['piece_name', 'print_time', 'filament_used', 
                          'material_cost', 'labor_cost', 'total_cost', 
                          'profit_margin', 'final_price']
        
        for field in required_fields:
            if field not in quote_data:
                return False, f"Campo requerido faltante: {field}"
        
        # Validar tipos de datos
        try:
            float(quote_data['print_time'])
            float(quote_data['filament_used'])
            float(quote_data['material_cost'])
            float(quote_data['labor_cost'])
            float(quote_data['total_cost'])
            float(quote_data['profit_margin'])
            float(quote_data['final_price'])
        except (ValueError, TypeError):
            return False, "Error en tipos de datos numéricos"
        
        return True, "Datos válidos"
    
    @staticmethod
    def get_import_formats():
        """Devuelve los formatos de importación disponibles."""
        return [
            {"name": "CSV", "extension": ".csv", "function": ImportUtils.import_from_csv},
            {"name": "JSON", "extension": ".json", "function": ImportUtils.import_from_json},
            {"name": "XML", "extension": ".xml", "function": ImportUtils.import_from_xml}
        ]
