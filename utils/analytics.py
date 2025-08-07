import json
import os
from datetime import datetime
class Analytics:
    def __init__(self, analytics_file="analytics.json"):
        self.analytics_file = analytics_file
        self.analytics_data = self.load_analytics()
    
    def load_analytics(self):
        """Carga los datos de análisis desde un archivo JSON."""
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.get_default_analytics()
        return self.get_default_analytics()
    
    def get_default_analytics(self):
        """Devuelve los datos de análisis predeterminados."""
        return {
            "app_starts": 0,
            "calculations_made": 0,
            "quotes_saved": 0,
            "csv_exports": 0,
            "settings_changes": 0,
            "time_spent": 0,  # en segundos
            "last_used": None,
            "most_used_features": {},
            "user_preferences": {}
        }
    
    def save_analytics(self):
        """Guarda los datos de análisis en el archivo JSON."""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics_data, f, indent=2)
        except IOError as e:
            print(f"Error al guardar análisis: {e}")
    
    def track_app_start(self):
        """Registra el inicio de la aplicación."""
        self.analytics_data["app_starts"] += 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_calculation(self):
        """Registra una cotización realizada."""
        self.analytics_data["calculations_made"] += 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_quote_saved(self):
        """Registra una cotización guardada."""
        self.analytics_data["quotes_saved"] += 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_csv_export(self):
        """Registra una exportación a CSV."""
        self.analytics_data["csv_exports"] += 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_settings_change(self):
        """Registra un cambio en la configuración."""
        self.analytics_data["settings_changes"] += 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_time_spent(self, seconds):
        """Registra el tiempo pasado en la aplicación."""
        self.analytics_data["time_spent"] += seconds
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def track_feature_usage(self, feature_name):
        """Registra el uso de una característica específica."""
        if feature_name in self.analytics_data["most_used_features"]:
            self.analytics_data["most_used_features"][feature_name] += 1
        else:
            self.analytics_data["most_used_features"][feature_name] = 1
        self.analytics_data["last_used"] = datetime.now().isoformat()
        self.save_analytics()
    
    def get_analytics_summary(self):
        """Devuelve un resumen de los datos de análisis."""
        return {
            "Total inicios de aplicación": self.analytics_data["app_starts"],
            "Cotizaciones realizadas": self.analytics_data["calculations_made"],
            "Cotizaciones guardadas": self.analytics_data["quotes_saved"],
            "Exportaciones CSV": self.analytics_data["csv_exports"],
            "Cambios de configuración": self.analytics_data["settings_changes"],
            "Tiempo total usado (minutos)": round(self.analytics_data["time_spent"] / 60, 2),
            "Último uso": self.analytics_data["last_used"],
            "Características más usadas": self.analytics_data["most_used_features"]
        }
    
    def reset_analytics(self):
        """Restablece todos los datos de análisis."""
        self.analytics_data = self.get_default_analytics()
        self.save_analytics()
