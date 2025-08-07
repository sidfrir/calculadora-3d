import json
import os

class SettingsManager:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        
        # Definir monedas disponibles
        self.currencies = {
            "USD": {
                "symbol": "$",
                "name": "Dólares (USD)",
                "code": "USD"
            },
            "ARS": {
                "symbol": "$",
                "name": "Pesos Argentinos (ARS)", 
                "code": "ARS"
            }
        }
        
        self.default_settings = {
            "theme_mode": "system",
            "currency": "USD",  # Código de moneda
            "currency_symbol": "$",
            "currency_name": "Dólares (USD)",
            "machine_cost_per_hour": 0.50,
            "electricity_kwh_price": 0.15,
            "printer_power_watts": 150,
            "filaments": {
                "PLA": {"price_per_kg": 25.00},
                "PETG": {"price_per_kg": 30.00},
                "ABS": {"price_per_kg": 28.00},
                "TPU": {"price_per_kg": 40.00},
                "Wood": {"price_per_kg": 35.00},
                "Carbon Fiber": {"price_per_kg": 60.00}
            }
        }
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return self.default_settings
        else:
            self.save_settings(self.default_settings)
            return self.default_settings

    def save_settings(self, settings_data):
        with open(self.settings_file, 'w') as f:
            json.dump(settings_data, f, indent=4)
        self.settings = settings_data

    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Actualiza una configuración y la guarda"""
        self.settings[key] = value
        self.save_settings(self.settings)
    
    def update_currency(self, currency_code):
        """Actualiza la configuración de moneda"""
        if currency_code in self.currencies:
            currency_info = self.currencies[currency_code]
            self.settings["currency"] = currency_code
            self.settings["currency_symbol"] = currency_info["symbol"]
            self.settings["currency_name"] = currency_info["name"]
            self.save_settings(self.settings)
            return True
        return False
    
    def get_currency_info(self):
        """Obtiene información completa de la moneda actual"""
        currency_code = self.settings.get("currency", "USD")
        return self.currencies.get(currency_code, self.currencies["USD"])
    
    def get_available_currencies(self):
        """Obtiene lista de monedas disponibles"""
        return self.currencies
