import re
from datetime import datetime
class SearchFilter:
    @staticmethod
    def filter_quotes(quotes, filters):
        """Filtra las cotizaciones según los criterios proporcionados."""
        filtered_quotes = quotes
        
        # Filtrar por nombre de pieza
        if "piece_name" in filters and filters["piece_name"]:
            piece_name = filters["piece_name"].lower()
            filtered_quotes = [q for q in filtered_quotes 
                             if piece_name in q.piece_name.lower()]
        
        # Filtrar por rango de fechas
        if "start_date" in filters and filters["start_date"]:
            try:
                start_date = datetime.fromisoformat(filters["start_date"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if datetime.fromisoformat(q.created_at) >= start_date]
            except ValueError:
                pass  # Ignorar fechas inválidas
        
        if "end_date" in filters and filters["end_date"]:
            try:
                end_date = datetime.fromisoformat(filters["end_date"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if datetime.fromisoformat(q.created_at) <= end_date]
            except ValueError:
                pass  # Ignorar fechas inválidas
        
        # Filtrar por rango de precios
        if "min_price" in filters and filters["min_price"] is not None:
            try:
                min_price = float(filters["min_price"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if q.final_price >= min_price]
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        if "max_price" in filters and filters["max_price"] is not None:
            try:
                max_price = float(filters["max_price"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if q.final_price <= max_price]
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        # Filtrar por rango de tiempo de impresión
        if "min_time" in filters and filters["min_time"] is not None:
            try:
                min_time = float(filters["min_time"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if q.print_time >= min_time]
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        if "max_time" in filters and filters["max_time"] is not None:
            try:
                max_time = float(filters["max_time"])
                filtered_quotes = [q for q in filtered_quotes 
                                 if q.print_time <= max_time]
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        return filtered_quotes
    
    @staticmethod
    def search_quotes(quotes, query):
        """Busca cotizaciones que coincidan con la consulta."""
        if not query:
            return quotes
        
        query = query.lower().strip()
        if not query:
            return quotes
        
        # Buscar en nombre de pieza
        matching_quotes = []
        for quote in quotes:
            if query in quote.piece_name.lower():
                matching_quotes.append(quote)
        
        return matching_quotes
    
    @staticmethod
    def sort_quotes(quotes, sort_by="created_at", reverse=True):
        """Ordena las cotizaciones según el criterio especificado."""
        try:
            if sort_by == "piece_name":
                return sorted(quotes, key=lambda x: x.piece_name.lower(), reverse=reverse)
            elif sort_by == "print_time":
                return sorted(quotes, key=lambda x: x.print_time, reverse=reverse)
            elif sort_by == "filament_used":
                return sorted(quotes, key=lambda x: x.filament_used, reverse=reverse)
            elif sort_by == "final_price":
                return sorted(quotes, key=lambda x: x.final_price, reverse=reverse)
            elif sort_by == "created_at":
                return sorted(quotes, key=lambda x: x.created_at, reverse=reverse)
            else:
                # Orden por defecto (fecha de creación)
                return sorted(quotes, key=lambda x: x.created_at, reverse=reverse)
        except Exception as e:
            print(f"Error al ordenar cotizaciones: {e}")
            return quotes
    
    @staticmethod
    def get_filter_options(quotes):
        """Obtiene opciones de filtrado basadas en los datos existentes."""
        if not quotes:
            return {
                "date_range": {"min": None, "max": None},
                "price_range": {"min": 0, "max": 0},
                "time_range": {"min": 0, "max": 0}
            }
        
        # Rango de fechas
        dates = [datetime.fromisoformat(q.created_at) for q in quotes]
        min_date = min(dates) if dates else None
        max_date = max(dates) if dates else None
        
        # Rango de precios
        prices = [q.final_price for q in quotes]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        
        # Rango de tiempos
        times = [q.print_time for q in quotes]
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        
        return {
            "date_range": {
                "min": min_date.isoformat() if min_date else None,
                "max": max_date.isoformat() if max_date else None
            },
            "price_range": {
                "min": min_price,
                "max": max_price
            },
            "time_range": {
                "min": min_time,
                "max": max_time
            }
        }
    
    @staticmethod
    def advanced_search(quotes, search_params):
        """Realiza una búsqueda avanzada con múltiples criterios."""
        # Esta función combina búsqueda y filtrado
        # Primero aplicamos filtros
        filtered_quotes = SearchFilter.filter_quotes(quotes, search_params)
        
        # Luego aplicamos búsqueda textual si se proporciona
        if "query" in search_params and search_params["query"]:
            filtered_quotes = SearchFilter.search_quotes(filtered_quotes, search_params["query"])
        
        # Finalmente aplicamos ordenamiento si se especifica
        if "sort_by" in search_params:
            reverse = search_params.get("sort_order", "desc") == "desc"
            filtered_quotes = SearchFilter.sort_quotes(filtered_quotes, 
                                                     search_params["sort_by"], 
                                                     reverse)
        
        return filtered_quotes
    
    @staticmethod
    def fuzzy_search(quotes, query, threshold=0.6):
        """Realiza una búsqueda difusa (aproximada) en los nombres de piezas."""
        if not query:
            return quotes
        
        query = query.lower().strip()
        if not query:
            return quotes
        
        matching_quotes = []
        for quote in quotes:
            piece_name = quote.piece_name.lower()
            # Calcular similitud simple (esto es una implementación básica)
            if query in piece_name:
                matching_quotes.append(quote)
            elif any(word in piece_name for word in query.split()):
                matching_quotes.append(quote)
        
        return matching_quotes
