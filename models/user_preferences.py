import json
import os
from typing import Dict, Any

class UserPreferences:
    def __init__(self, preferences_file="user_preferences.json"):
        self.preferences_file = preferences_file
        self.preferences = self.load_preferences()
    
    def load_preferences(self) -> Dict[str, Any]:
        """Carga las preferencias del usuario desde un archivo JSON."""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.get_default_preferences()
        return self.get_default_preferences()
    
    def get_default_preferences(self) -> Dict[str, Any]:
        """Devuelve las preferencias predeterminadas."""
        return {
            "animations_enabled": True,
            "transition_speed": "normal",
            "startup_view": "/",
            "auto_save_quotes": True,
            "currency_display": "symbol",
            "decimal_places": 2,
            "recent_filaments": [],
            "favorite_settings": {}
        }
    
    def get(self, key: str, default=None):
        """Obtiene un valor de preferencia."""
        return self.preferences.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor de preferencia."""
        self.preferences[key] = value
        self.save_preferences()
    
    def save_preferences(self):
        """Guarda las preferencias en el archivo JSON."""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except IOError as e:
            print(f"Error al guardar preferencias: {e}")
    
    def reset_to_default(self):
        """Restablece todas las preferencias a los valores predeterminados."""
        self.preferences = self.get_default_preferences()
        self.save_preferences()
    
    def update_recent_filaments(self, filament_type: str):
        """Actualiza la lista de filamentos recientes."""
        recent = self.preferences.get("recent_filaments", [])
        if filament_type in recent:
            recent.remove(filament_type)
        recent.insert(0, filament_type)
        # Mantener solo los últimos 5 filamentos
        self.preferences["recent_filaments"] = recent[:5]
        self.save_preferences()
    
    def add_favorite_setting(self, name: str, settings: Dict[str, Any]):
        """Agrega una configuración favorita."""
        favorites = self.preferences.get("favorite_settings", {})
        favorites[name] = settings
        self.preferences["favorite_settings"] = favorites
        self.save_preferences()
    
    def remove_favorite_setting(self, name: str):
        """Elimina una configuración favorita."""
        favorites = self.preferences.get("favorite_settings", {})
        if name in favorites:
            del favorites[name]
            self.preferences["favorite_settings"] = favorites
            self.save_preferences()
