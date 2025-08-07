import math
class CostOptimizer:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
    
    def suggest_cost_savings(self, quote_data):
        """Sugiere formas de reducir costos para una cotización."""
        suggestions = []
        settings = self.settings_manager.load_settings()
        
        # Calcular costos actuales
        current_material_cost = quote_data.get('material_cost', 0)
        current_labor_cost = quote_data.get('labor_cost', 0)
        current_total_cost = quote_data.get('total_cost', 0)
        current_final_price = quote_data.get('final_price', 0)
        
        # Sugerencias para reducir costo de material
        material_savings = self._analyze_material_costs(quote_data, settings)
        if material_savings:
            suggestions.extend(material_savings)
        
        # Sugerencias para reducir costo de mano de obra
        labor_savings = self._analyze_labor_costs(quote_data, settings)
        if labor_savings:
            suggestions.extend(labor_savings)
        
        # Sugerencias generales de optimización
        general_suggestions = self._analyze_general_optimizations(quote_data, settings)
        if general_suggestions:
            suggestions.extend(general_suggestions)
        
        return suggestions
    
    def _analyze_material_costs(self, quote_data, settings):
        """Analiza posibles ahorros en costos de material."""
        suggestions = []
        
        filament_used = quote_data.get('filament_used', 0)
        current_material_cost = quote_data.get('material_cost', 0)
        
        if filament_used <= 0:
            return suggestions
        
        # Calcular costo por gramo actual
        current_cost_per_gram = current_material_cost / filament_used
        
        # Comparar con precios de filamentos en configuración
        filaments = settings.get('filaments', {})
        if filaments:
            cheapest_filament = min(filaments.values(), 
                                  key=lambda x: x.get('price_per_kg', float('inf')))
            cheapest_price_per_gram = cheapest_filament.get('price_per_kg', 0) / 1000
            
            if cheapest_price_per_gram < current_cost_per_gram:
                potential_savings = (current_cost_per_gram - cheapest_price_per_gram) * filament_used
                suggestions.append({
                    "type": "material",
                    "title": "Posible ahorro en material",
                    "description": f"Considera usar {cheapest_filament.get('name', 'filamento más barato')} "
                                  f"para ahorrar ${potential_savings:.2f}",
                    "savings": potential_savings
                })
        
        return suggestions
    
    def _analyze_labor_costs(self, quote_data, settings):
        """Analiza posibles ahorros en costos de mano de obra."""
        suggestions = []
        
        print_time = quote_data.get('print_time', 0)
        current_labor_cost = quote_data.get('labor_cost', 0)
        
        if print_time <= 0:
            return suggestions
        
        # Calcular costo por hora actual
        current_labor_rate = current_labor_cost / print_time if print_time > 0 else 0
        
        # Comparar con configuración
        machine_cost = settings.get('machine_cost_per_hour', 0)
        
        # Si el costo de mano de obra es mayor que el costo de máquina,
        # sugerir optimización
        if current_labor_rate > machine_cost * 1.5:  # 50% más que el costo de máquina
            potential_savings = (current_labor_rate - machine_cost) * print_time
            suggestions.append({
                "type": "labor",
                "title": "Optimización de mano de obra",
                "description": f"El costo de mano de obra es alto. "
                              f"Considera reducirlo para ahorrar ${potential_savings:.2f}",
                "savings": potential_savings
            })
        
        return suggestions
    
    def _analyze_general_optimizations(self, quote_data, settings):
        """Analiza optimizaciones generales."""
        suggestions = []
        
        print_time = quote_data.get('print_time', 0)
        filament_used = quote_data.get('filament_used', 0)
        
        # Sugerir optimización de tiempo de impresión si es muy largo
        if print_time > 24:  # Más de 24 horas
            suggestions.append({
                "type": "time",
                "title": "Optimización de tiempo",
                "description": "El tiempo de impresión es muy largo. "
                              "Considera optimizar el diseño o usar parámetros de impresión más rápidos.",
                "savings": 0
            })
        
        # Sugerir optimización de uso de filamento si es muy alto
        if filament_used > 1000:  # Más de 1kg
            suggestions.append({
                "type": "material",
                "title": "Optimización de material",
                "description": "El uso de filamento es alto. "
                              "Considera optimizar el diseño o usar relleno más eficiente.",
                "savings": 0
            })
        
        return suggestions
    
    def calculate_optimized_quote(self, quote_data, optimization_level="moderate"):
        """Calcula una cotización optimizada según el nivel de optimización."""
        optimized_data = quote_data.copy()
        
        if optimization_level == "aggressive":
            # Reducir costos en un 20%
            optimized_data['material_cost'] *= 0.8
            optimized_data['labor_cost'] *= 0.8
        elif optimization_level == "moderate":
            # Reducir costos en un 10%
            optimized_data['material_cost'] *= 0.9
            optimized_data['labor_cost'] *= 0.9
        elif optimization_level == "conservative":
            # Reducir costos en un 5%
            optimized_data['material_cost'] *= 0.95
            optimized_data['labor_cost'] *= 0.95
        
        # Recalcular costos totales
        optimized_data['total_cost'] = (
            optimized_data['material_cost'] + 
            optimized_data['labor_cost']
        )
        
        profit_margin = quote_data.get('profit_margin', 0)
        optimized_data['final_price'] = (
            optimized_data['total_cost'] * 
            (1 + profit_margin / 100)
        )
        
        return optimized_data
    
    def compare_quotes(self, quote1, quote2):
        """Compara dos cotizaciones y muestra diferencias."""
        comparison = {
            "quote1": quote1,
            "quote2": quote2,
            "differences": {}
        }
        
        fields_to_compare = [
            'print_time', 'filament_used', 'material_cost', 
            'labor_cost', 'total_cost', 'final_price'
        ]
        
        for field in fields_to_compare:
            value1 = quote1.get(field, 0)
            value2 = quote2.get(field, 0)
            
            if value1 != value2:
                difference = value2 - value1
                percentage_change = ((value2 - value1) / value1 * 100) if value1 != 0 else 0
                
                comparison["differences"][field] = {
                    "quote1": value1,
                    "quote2": value2,
                    "difference": difference,
                    "percentage_change": percentage_change
                }
        
        return comparison
    
    def get_cost_breakdown(self, quote_data):
        """Obtiene un desglose detallado de costos."""
        material_cost = quote_data.get('material_cost', 0)
        labor_cost = quote_data.get('labor_cost', 0)
        total_cost = quote_data.get('total_cost', 0)
        final_price = quote_data.get('final_price', 0)
        profit_margin = quote_data.get('profit_margin', 0)
        
        profit_amount = final_price - total_cost if total_cost > 0 else 0
        
        breakdown = {
            "material_cost": {
                "amount": material_cost,
                "percentage": (material_cost / final_price * 100) if final_price > 0 else 0
            },
            "labor_cost": {
                "amount": labor_cost,
                "percentage": (labor_cost / final_price * 100) if final_price > 0 else 0
            },
            "total_cost": {
                "amount": total_cost,
                "percentage": (total_cost / final_price * 100) if final_price > 0 else 0
            },
            "profit": {
                "amount": profit_amount,
                "percentage": profit_margin
            },
            "final_price": {
                "amount": final_price,
                "profit_included": True
            }
        }
        
        return breakdown
