class I18n:
    def __init__(self, language="es"):
        self.language = language
        self.translations = self.load_translations()
    
    def load_translations(self):
        """Carga las traducciones para el idioma seleccionado."""
        translations = {
            "es": {
                # Títulos y etiquetas generales
                "app_title": "Calculadora 3D Pro",
                "home": "Inicio",
                "calculator": "Calcular",
                "history": "Historial",
                "settings": "Ajustes",
                
                # Vistas
                "home_title": "Bienvenido a Calculadora 3D Pro",
                "calculator_title": "Calculadora de Costos",
                "history_title": "Historial de Cotizaciones",
                "settings_title": "Configuración",
                
                # Etiquetas de campos
                "piece_name": "Nombre de la Pieza",
                "print_time": "Tiempo de Impresión",
                "filament_used": "Filamento Usado (g)",
                "material_cost": "Costo del Material",
                "labor_cost": "Costo de Mano de Obra",
                "total_cost": "Costo Total",
                "profit_margin": "Margen de Ganancia (%)",
                "final_price": "Precio Final",
                
                # Botones
                "calculate": "Calcular",
                "save": "Guardar",
                "export_csv": "Exportar a CSV",
                "clear": "Limpiar",
                "help": "Ayuda",
                
                # Mensajes
                "saved_success": "Cotización guardada exitosamente",
                "saved_error": "Error al guardar la cotización",
                "settings_saved": "Configuración guardada",
                "settings_error": "Error al guardar la configuración",
                "no_history": "No hay cotizaciones guardadas",
                "confirm_delete": "¿Está seguro de que desea eliminar esta cotización?",
                
                # Configuración
                "machine_cost_label": "Costo Máquina por Hora",
                "electricity_price_label": "Costo Electricidad (kWh)",
                "printer_power_label": "Consumo Impresora (Watts)",
                "theme_label": "Tema de la Aplicación",
                "theme_system": "Automático (Sistema)",
                "theme_light": "Claro",
                "theme_dark": "Oscuro",
                
                # Ayuda
                "help_title": "Ayuda",
                "help_content": "Esta aplicación te permite calcular el costo de impresión 3D de tus piezas. Ingresa los datos solicitados y obtén una cotización detallada.",
                
                # Errores
                "error_required_fields": "Por favor, completa todos los campos requeridos",
                "error_numeric_values": "Asegúrate de que los valores numéricos son correctos",
            },
            "en": {
                # General titles and labels
                "app_title": "3D Calculator Pro",
                "home": "Home",
                "calculator": "Calculate",
                "history": "History",
                "settings": "Settings",
                
                # Views
                "home_title": "Welcome to 3D Calculator Pro",
                "calculator_title": "Cost Calculator",
                "history_title": "Quote History",
                "settings_title": "Settings",
                
                # Field labels
                "piece_name": "Piece Name",
                "print_time": "Print Time",
                "filament_used": "Filament Used (g)",
                "material_cost": "Material Cost",
                "labor_cost": "Labor Cost",
                "total_cost": "Total Cost",
                "profit_margin": "Profit Margin (%)",
                "final_price": "Final Price",
                
                # Buttons
                "calculate": "Calculate",
                "save": "Save",
                "export_csv": "Export to CSV",
                "clear": "Clear",
                "help": "Help",
                
                # Messages
                "saved_success": "Quote saved successfully",
                "saved_error": "Error saving quote",
                "settings_saved": "Settings saved",
                "settings_error": "Error saving settings",
                "no_history": "No saved quotes",
                "confirm_delete": "Are you sure you want to delete this quote?",
                
                # Settings
                "machine_cost_label": "Machine Cost per Hour",
                "electricity_price_label": "Electricity Cost (kWh)",
                "printer_power_label": "Printer Power Consumption (Watts)",
                "theme_label": "Application Theme",
                "theme_system": "Automatic (System)",
                "theme_light": "Light",
                "theme_dark": "Dark",
                
                # Help
                "help_title": "Help",
                "help_content": "This application allows you to calculate the cost of 3D printing your parts. Enter the requested data and get a detailed quote.",
                
                # Errors
                "error_required_fields": "Please fill in all required fields",
                "error_numeric_values": "Make sure the numeric values are correct",
            }
        }
        
        return translations.get(self.language, translations["es"])
    
    def get(self, key):
        """Obtiene la traducción para una clave específica."""
        return self.translations.get(key, key)
    
    def set_language(self, language):
        """Cambia el idioma de la aplicación."""
        self.language = language
        self.translations = self.load_translations()
    
    def get_available_languages(self):
        """Devuelve los idiomas disponibles."""
        return ["es", "en"]
    
    def get_language_name(self, language_code):
        """Devuelve el nombre del idioma en su propio idioma."""
        names = {
            "es": "Español",
            "en": "English"
        }
        return names.get(language_code, language_code)
