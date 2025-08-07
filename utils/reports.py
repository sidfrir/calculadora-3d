import json
from datetime import datetime, timedelta
class ReportGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def generate_summary_report(self, start_date=None, end_date=None):
        """Genera un reporte resumido de cotizaciones."""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            # Filtrar por fechas si se proporcionan
            if start_date:
                quotes = [q for q in quotes if q.created_at >= start_date]
            if end_date:
                quotes = [q for q in quotes if q.created_at <= end_date]
            
            if not quotes:
                return {"error": "No hay datos para generar el reporte"}
            
            total_quotes = len(quotes)
            total_revenue = sum(q.final_price for q in quotes)
            avg_quote_value = total_revenue / total_quotes if total_quotes > 0 else 0
            
            # Calcular totales por tipo de costo
            total_material_cost = sum(q.material_cost for q in quotes)
            total_labor_cost = sum(q.labor_cost for q in quotes)
            
            # Encontrar cotización más cara y más barata
            most_expensive = max(quotes, key=lambda x: x.final_price) if quotes else None
            least_expensive = min(quotes, key=lambda x: x.final_price) if quotes else None
            
            report = {
                "report_date": datetime.now().isoformat(),
                "period": {
                    "start": start_date.isoformat() if start_date else None,
                    "end": end_date.isoformat() if end_date else None
                },
                "summary": {
                    "total_quotes": total_quotes,
                    "total_revenue": total_revenue,
                    "average_quote_value": avg_quote_value,
                    "total_material_cost": total_material_cost,
                    "total_labor_cost": total_labor_cost
                },
                "extremes": {
                    "most_expensive": {
                        "piece_name": most_expensive.piece_name if most_expensive else None,
                        "final_price": most_expensive.final_price if most_expensive else 0
                    },
                    "least_expensive": {
                        "piece_name": least_expensive.piece_name if least_expensive else None,
                        "final_price": least_expensive.final_price if least_expensive else 0
                    }
                }
            }
            
            return report
        except Exception as e:
            return {"error": f"Error al generar reporte resumido: {str(e)}"}
    
    def generate_detailed_report(self, start_date=None, end_date=None):
        """Genera un reporte detallado de cotizaciones."""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            # Filtrar por fechas si se proporcionan
            if start_date:
                quotes = [q for q in quotes if q.created_at >= start_date]
            if end_date:
                quotes = [q for q in quotes if q.created_at <= end_date]
            
            if not quotes:
                return {"error": "No hay datos para generar el reporte"}
            
            # Agrupar por mes
            monthly_data = {}
            for quote in quotes:
                # Extraer mes y año
                quote_date = datetime.fromisoformat(quote.created_at)
                month_key = quote_date.strftime("%Y-%m")
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {
                        "quote_count": 0,
                        "total_revenue": 0,
                        "total_material_cost": 0,
                        "total_labor_cost": 0,
                        "quotes": []
                    }
                
                monthly_data[month_key]["quote_count"] += 1
                monthly_data[month_key]["total_revenue"] += quote.final_price
                monthly_data[month_key]["total_material_cost"] += quote.material_cost
                monthly_data[month_key]["total_labor_cost"] += quote.labor_cost
                monthly_data[month_key]["quotes"].append({
                    "id": quote.id,
                    "piece_name": quote.piece_name,
                    "final_price": quote.final_price,
                    "created_at": quote.created_at
                })
            
            report = {
                "report_date": datetime.now().isoformat(),
                "period": {
                    "start": start_date.isoformat() if start_date else None,
                    "end": end_date.isoformat() if end_date else None
                },
                "monthly_data": monthly_data,
                "total_quotes": len(quotes),
                "total_revenue": sum(q.final_price for q in quotes)
            }
            
            return report
        except Exception as e:
            return {"error": f"Error al generar reporte detallado: {str(e)}"}
    
    def generate_material_usage_report(self):
        """Genera un reporte de uso de materiales."""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            if not quotes:
                return {"error": "No hay datos para generar el reporte"}
            
            material_usage = {}
            total_filament_used = 0
            
            for quote in quotes:
                total_filament_used += quote.filament_used
                
                # Aquí podríamos agregar lógica para rastrear por tipo de filamento
                # si se almacenara esa información
            
            report = {
                "report_date": datetime.now().isoformat(),
                "total_filament_used": total_filament_used,
                "average_filament_per_quote": total_filament_used / len(quotes) if quotes else 0,
                "material_usage": material_usage
            }
            
            return report
        except Exception as e:
            return {"error": f"Error al generar reporte de uso de materiales: {str(e)}"}
    
    def generate_profitability_report(self):
        """Genera un reporte de rentabilidad."""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            if not quotes:
                return {"error": "No hay datos para generar el reporte"}
            
            total_revenue = sum(q.final_price for q in quotes)
            total_costs = sum(q.total_cost for q in quotes)
            total_profit = total_revenue - total_costs
            profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            avg_profit_per_quote = total_profit / len(quotes) if quotes else 0
            
            report = {
                "report_date": datetime.now().isoformat(),
                "financial_summary": {
                    "total_revenue": total_revenue,
                    "total_costs": total_costs,
                    "total_profit": total_profit,
                    "profit_margin_percent": profit_margin,
                    "average_profit_per_quote": avg_profit_per_quote
                }
            }
            
            return report
        except Exception as e:
            return {"error": f"Error al generar reporte de rentabilidad: {str(e)}"}
    
    def export_report_to_json(self, report_data, file_path):
        """Exporta un reporte a un archivo JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al exportar reporte: {e}")
            return False
    
    def get_report_statistics(self):
        """Obtiene estadísticas generales para reportes."""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            if not quotes:
                return {"error": "No hay datos disponibles"}
            
            # Calcular estadísticas
            total_quotes = len(quotes)
            
            # Cotizaciones por período
            today = datetime.now()
            last_7_days = today - timedelta(days=7)
            last_30_days = today - timedelta(days=30)
            
            quotes_last_7_days = [q for q in quotes 
                                if datetime.fromisoformat(q.created_at) >= last_7_days]
            quotes_last_30_days = [q for q in quotes 
                                 if datetime.fromisoformat(q.created_at) >= last_30_days]
            
            stats = {
                "total_quotes": total_quotes,
                "quotes_last_7_days": len(quotes_last_7_days),
                "quotes_last_30_days": len(quotes_last_30_days),
                "average_quotes_per_day": total_quotes / 30 if total_quotes > 0 else 0
            }
            
            return stats
        except Exception as e:
            return {"error": f"Error al obtener estadísticas: {str(e)}"}
