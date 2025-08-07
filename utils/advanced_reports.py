import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AdvancedReports:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def generate_profitability_analysis(self, start_date=None, end_date=None):
        """Genera un análisis de rentabilidad detallado."""
        quotes = self.db_manager.get_all_quotes()
        
        # Filtrar por fechas si se proporcionan
        if start_date:
            quotes = [q for q in quotes if q.created_at >= start_date]
        if end_date:
            quotes = [q for q in quotes if q.created_at <= end_date]
        
        if not quotes:
            return {"error": "No hay datos para el período especificado"}
        
        # Calcular métricas
        total_revenue = sum(q.final_price for q in quotes)
        total_cost = sum(q.total_cost for q in quotes)
        total_profit = total_revenue - total_cost
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Calcular por tipo de filamento
        filament_stats = {}
        for quote in quotes:
            filament = getattr(quote, 'filament_type', 'Desconocido')
            if filament not in filament_stats:
                filament_stats[filament] = {
                    "count": 0,
                    "revenue": 0,
                    "cost": 0,
                    "profit": 0
                }
            
            filament_stats[filament]["count"] += 1
            filament_stats[filament]["revenue"] += quote.final_price
            filament_stats[filament]["cost"] += quote.total_cost
            filament_stats[filament]["profit"] += (quote.final_price - quote.total_cost)
        
        # Calcular estadísticas de tiempo
        total_print_time = sum(q.print_time for q in quotes)
        avg_print_time = total_print_time / len(quotes) if quotes else 0
        
        # Calcular estadísticas de material
        total_filament = sum(q.filament_used for q in quotes)
        avg_filament = total_filament / len(quotes) if quotes else 0
        
        report = {
            "period": {
                "start": start_date,
                "end": end_date
            },
            "summary": {
                "total_quotes": len(quotes),
                "total_revenue": total_revenue,
                "total_cost": total_cost,
                "total_profit": total_profit,
                "profit_margin": profit_margin,
                "total_print_time": total_print_time,
                "avg_print_time": avg_print_time,
                "total_filament_used": total_filament,
                "avg_filament_used": avg_filament
            },
            "filament_breakdown": filament_stats,
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def generate_monthly_trends(self, months=12):
        """Genera un análisis de tendencias mensuales."""
        quotes = self.db_manager.get_all_quotes()
        
        # Agrupar por mes
        monthly_data = {}
        for quote in quotes:
            # Convertir la fecha de creación a objeto datetime
            try:
                quote_date = datetime.fromisoformat(quote.created_at)
                month_key = quote_date.strftime("%Y-%m")
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {
                        "quotes": 0,
                        "revenue": 0,
                        "cost": 0,
                        "profit": 0,
                        "print_time": 0,
                        "filament": 0
                    }
                
                monthly_data[month_key]["quotes"] += 1
                monthly_data[month_key]["revenue"] += quote.final_price
                monthly_data[month_key]["cost"] += quote.total_cost
                monthly_data[month_key]["profit"] += (quote.final_price - quote.total_cost)
                monthly_data[month_key]["print_time"] += quote.print_time
                monthly_data[month_key]["filament"] += quote.filament_used
            except Exception as e:
                print(f"Error procesando cotización: {e}")
                continue
        
        # Ordenar por fecha
        sorted_months = sorted(monthly_data.keys())
        
        # Tomar solo los últimos N meses
        if len(sorted_months) > months:
            sorted_months = sorted_months[-months:]
        
        trends = {
            "months": sorted_months,
            "data": {month: monthly_data[month] for month in sorted_months},
            "generated_at": datetime.now().isoformat()
        }
        
        return trends
    
    def generate_client_analysis(self):
        """Genera un análisis por cliente (si se tiene información de clientes)."""
        quotes = self.db_manager.get_all_quotes()
        
        # Como no tenemos información de clientes en el modelo actual,
        # usaremos el nombre de la pieza como identificador de cliente
        client_stats = {}
        for quote in quotes:
            client = getattr(quote, 'client_name', quote.piece_name)
            
            if client not in client_stats:
                client_stats[client] = {
                    "quotes": 0,
                    "total_spent": 0,
                    "avg_order_value": 0,
                    "first_order": quote.created_at,
                    "last_order": quote.created_at
                }
            
            client_stats[client]["quotes"] += 1
            client_stats[client]["total_spent"] += quote.final_price
            
            # Actualizar fechas
            if quote.created_at < client_stats[client]["first_order"]:
                client_stats[client]["first_order"] = quote.created_at
            if quote.created_at > client_stats[client]["last_order"]:
                client_stats[client]["last_order"] = quote.created_at
        
        # Calcular valores promedio
        for client in client_stats:
            if client_stats[client]["quotes"] > 0:
                client_stats[client]["avg_order_value"] = (
                    client_stats[client]["total_spent"] / client_stats[client]["quotes"]
                )
        
        # Ordenar por total gastado
        sorted_clients = sorted(
            client_stats.items(), 
            key=lambda x: x[1]["total_spent"], 
            reverse=True
        )
        
        report = {
            "clients": dict(sorted_clients[:20]),  # Top 20 clientes
            "summary": {
                "total_clients": len(client_stats),
                "total_quotes": sum(c["quotes"] for c in client_stats.values()),
                "total_revenue": sum(c["total_spent"] for c in client_stats.values())
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def export_report_to_csv(self, report_data, filename):
        """Exporta un informe a formato CSV."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir encabezados
                writer.writerow(["Métrica", "Valor"])
                
                # Escribir datos del resumen
                summary = report_data.get("summary", {})
                for key, value in summary.items():
                    writer.writerow([key, value])
                
                # Escribir datos de desglose por filamento
                writer.writerow([])  # Línea en blanco
                writer.writerow(["Filamento", "Cotizaciones", "Ingresos", "Costos", "Ganancia"])
                
                filament_data = report_data.get("filament_breakdown", {})
                for filament, stats in filament_data.items():
                    writer.writerow([
                        filament,
                        stats.get("count", 0),
                        stats.get("revenue", 0),
                        stats.get("cost", 0),
                        stats.get("profit", 0)
                    ])
            
            return True, f"Informe exportado a {filename}"
        except Exception as e:
            return False, f"Error al exportar informe: {str(e)}"
    
    def generate_comparative_report(self, periods):
        """Genera un informe comparativo entre diferentes períodos."""
        reports = []
        for period in periods:
            start_date = period.get("start")
            end_date = period.get("end")
            label = period.get("label", f"{start_date} a {end_date}")
            
            report = self.generate_profitability_analysis(start_date, end_date)
            report["label"] = label
            reports.append(report)
        
        # Comparar métricas
        comparison = {
            "periods": [r["label"] for r in reports],
            "metrics": {}
        }
        
        # Métricas a comparar
        metrics = ["total_quotes", "total_revenue", "total_cost", "total_profit", "profit_margin"]
        
        for metric in metrics:
            comparison["metrics"][metric] = [
                r.get("summary", {}).get(metric, 0) for r in reports
            ]
        
        comparison["generated_at"] = datetime.now().isoformat()
        
        return comparison
    
    def get_performance_indicators(self):
        """Obtiene indicadores clave de rendimiento (KPIs)."""
        quotes = self.db_manager.get_all_quotes()
        
        if not quotes:
            return {"error": "No hay datos disponibles"}
        
        # Calcular KPIs
        total_quotes = len(quotes)
        total_revenue = sum(q.final_price for q in quotes)
        total_profit = sum((q.final_price - q.total_cost) for q in quotes)
        
        # KPIs de crecimiento
        # Obtener cotizaciones de los últimos 30 días
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_quotes = [q for q in quotes 
                        if datetime.fromisoformat(q.created_at) >= thirty_days_ago]
        
        # Obtener cotizaciones del mes anterior
        sixty_days_ago = datetime.now() - timedelta(days=60)
        previous_month_quotes = [q for q in quotes 
                               if thirty_days_ago > datetime.fromisoformat(q.created_at) >= sixty_days_ago]
        
        # Calcular crecimiento
        current_month_count = len(recent_quotes)
        previous_month_count = len(previous_month_quotes)
        
        growth_rate = 0
        if previous_month_count > 0:
            growth_rate = ((current_month_count - previous_month_count) / previous_month_count) * 100
        
        kpis = {
            "total_quotes": total_quotes,
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "avg_profit_margin": (total_profit / total_revenue * 100) if total_revenue > 0 else 0,
            "recent_activity": {
                "quotes_last_30_days": current_month_count,
                "growth_rate": growth_rate,
                "trend": "positive" if growth_rate > 0 else "negative" if growth_rate < 0 else "stable"
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return kpis
