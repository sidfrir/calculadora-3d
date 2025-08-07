import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Quote:
    """Modelo simple para una cotización"""
    def __init__(self, piece_name: str, weight_g: float, total_hours: float, 
                 filament_type: str, material_cost: float, print_time_cost: float,
                 electricity_cost: float, profit_margin_percent: float, final_price: float):
        self.id = self._generate_id()
        self.piece_name = piece_name
        self.weight_g = weight_g
        self.total_hours = total_hours
        self.filament_type = filament_type
        self.material_cost = material_cost
        self.print_time_cost = print_time_cost
        self.electricity_cost = electricity_cost
        self.profit_margin_percent = profit_margin_percent
        self.final_price = final_price
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _generate_id(self):
        """Genera un ID único"""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte la cotización a diccionario"""
        return {
            'id': self.id,
            'piece_name': self.piece_name,
            'weight_g': self.weight_g,
            'total_hours': self.total_hours,
            'filament_type': self.filament_type,
            'material_cost': self.material_cost,
            'print_time_cost': self.print_time_cost,
            'electricity_cost': self.electricity_cost,
            'profit_margin_percent': self.profit_margin_percent,
            'final_price': self.final_price,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una cotización desde un diccionario"""
        quote = cls(
            piece_name=data['piece_name'],
            weight_g=data['weight_g'],
            total_hours=data['total_hours'],
            filament_type=data['filament_type'],
            material_cost=data['material_cost'],
            print_time_cost=data['print_time_cost'],
            electricity_cost=data['electricity_cost'],
            profit_margin_percent=data['profit_margin_percent'],
            final_price=data['final_price']
        )
        quote.id = data.get('id', quote.id)
        quote.timestamp = data.get('timestamp', quote.timestamp)
        return quote

class DatabaseManager:
    """Gestor de base de datos simplificado usando JSON"""
    
    def __init__(self, db_filename="quotes.json"):
        self.db_filename = db_filename
        self.quotes = self.load_quotes()
    
    def load_quotes(self) -> List[Quote]:
        """Carga las cotizaciones desde el archivo JSON"""
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Quote.from_dict(quote_data) for quote_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar cotizaciones: {e}")
                return []
        return []
    
    def save_quotes(self):
        """Guarda las cotizaciones en el archivo JSON"""
        try:
            with open(self.db_filename, 'w', encoding='utf-8') as f:
                json.dump([quote.to_dict() for quote in self.quotes], f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar cotizaciones: {e}")
            return False
    
    def save_quote(self, quote_data: dict) -> bool:
        """Guarda una nueva cotización"""
        try:
            quote = Quote(
                piece_name=quote_data['piece_name'],
                weight_g=quote_data['weight_g'],
                total_hours=quote_data['total_hours'],
                filament_type=quote_data['filament_type'],
                material_cost=quote_data['material_cost'],
                print_time_cost=quote_data['print_time_cost'],
                electricity_cost=quote_data['electricity_cost'],
                profit_margin_percent=quote_data['profit_margin_percent'],
                final_price=quote_data['final_price']
            )
            
            self.quotes.append(quote)
            return self.save_quotes()
        except Exception as e:
            print(f"Error al guardar cotización: {e}")
            return False
    
    def get_all_quotes(self) -> List[Quote]:
        """Obtiene todas las cotizaciones"""
        return self.quotes
    
    def get_recent_quotes(self, limit: int = 10) -> List[Quote]:
        """Obtiene las cotizaciones más recientes"""
        sorted_quotes = sorted(self.quotes, key=lambda q: q.timestamp, reverse=True)
        return sorted_quotes[:limit]
    
    def delete_quote(self, quote_id: str) -> bool:
        """Elimina una cotización por ID"""
        try:
            self.quotes = [q for q in self.quotes if q.id != quote_id]
            return self.save_quotes()
        except Exception as e:
            print(f"Error al eliminar cotización: {e}")
            return False
    
    def search_quotes(self, search_term: str) -> List[Quote]:
        """Busca cotizaciones por nombre de pieza"""
        search_term = search_term.lower()
        return [
            quote for quote in self.quotes 
            if search_term in quote.piece_name.lower() or search_term in quote.filament_type.lower()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas básicas"""
        if not self.quotes:
            return {
                'total_quotes': 0,
                'total_revenue': 0,
                'avg_price': 0,
                'most_used_filament': 'N/A'
            }
        
        total_revenue = sum(quote.final_price for quote in self.quotes)
        avg_price = total_revenue / len(self.quotes)
        
        # Filamento más usado
        filament_counts = {}
        for quote in self.quotes:
            filament = quote.filament_type
            filament_counts[filament] = filament_counts.get(filament, 0) + 1
        
        most_used_filament = max(filament_counts.items(), key=lambda x: x[1])[0] if filament_counts else 'N/A'
        
        return {
            'total_quotes': len(self.quotes),
            'total_revenue': total_revenue,
            'avg_price': avg_price,
            'most_used_filament': most_used_filament
        }
