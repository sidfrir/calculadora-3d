import requests
import json
import os

class ExternalIntegrations:
    def __init__(self, config_file="integrations_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Carga la configuración de integraciones."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_config(self):
        """Guarda la configuración de integraciones."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False
    
    def send_to_email(self, quote_data, recipient_email, subject="Cotización 3D"):
        """Envía una cotización por correo electrónico (simulado)."""
        # Esta es una implementación simulada
        # En una implementación real, se conectaría a un servicio de correo
        
        try:
            # Verificar si hay configuración de correo
            email_config = self.config.get('email', {})
            
            # Crear contenido del correo
            content = self._format_quote_email(quote_data)
            
            # En una implementación real, aquí se enviaría el correo
            print(f"Enviando correo a {recipient_email} con asunto '{subject}'")
            print(f"Contenido: {content}")
            
            return True, "Correo enviado exitosamente (simulado)"
        except Exception as e:
            return False, f"Error al enviar correo: {str(e)}"
    
    def _format_quote_email(self, quote_data):
        """Formatea los datos de la cotización para correo electrónico."""
        content = f"""
Cotización 3D - {quote_data.get('piece_name', 'Pieza sin nombre')}

Detalles:
- Tiempo de impresión: {quote_data.get('print_time', 0)} horas
- Filamento usado: {quote_data.get('filament_used', 0)} g
- Costo de material: ${quote_data.get('material_cost', 0):.2f}
- Costo de mano de obra: ${quote_data.get('labor_cost', 0):.2f}
- Costo total: ${quote_data.get('total_cost', 0):.2f}
- Margen de ganancia: {quote_data.get('profit_margin', 0)}%
- Precio final: ${quote_data.get('final_price', 0):.2f}

Fecha: {quote_data.get('created_at', 'No disponible')}
        """
        return content
    
    def send_to_cloud(self, quote_data, service="dropbox"):
        """Envía una cotización a un servicio en la nube (simulado)."""
        try:
            # Verificar configuración del servicio
            service_config = self.config.get(service, {})
            
            if not service_config.get('enabled', False):
                return False, f"Servicio {service} no está habilitado"
            
            # En una implementación real, aquí se conectaría al servicio en la nube
            print(f"Enviando datos a {service}")
            print(f"Datos: {json.dumps(quote_data, indent=2)}")
            
            return True, f"Datos enviados a {service} exitosamente (simulado)"
        except Exception as e:
            return False, f"Error al enviar a {service}: {str(e)}"
    
    def get_filament_prices(self, filament_type="PLA"):
        """Obtiene precios actuales de filamentos de una API externa (simulado)."""
        # Esta es una implementación simulada
        # En una implementación real, se conectaría a una API de precios
        
        try:
            # Simular precios de filamentos
            simulated_prices = {
                "PLA": {"price_per_kg": 25.0, "supplier": "Proveedor A"},
                "ABS": {"price_per_kg": 30.0, "supplier": "Proveedor B"},
                "PETG": {"price_per_kg": 28.0, "supplier": "Proveedor A"},
                "TPU": {"price_per_kg": 45.0, "supplier": "Proveedor C"}
            }
            
            return simulated_prices.get(filament_type, 
                                      {"price_per_kg": 0, "supplier": "Desconocido"})
        except Exception as e:
            print(f"Error al obtener precios de filamentos: {str(e)}")
            return {"price_per_kg": 0, "supplier": "Error"}
    
    def get_electricity_price(self, region="default"):
        """Obtiene el precio actual de electricidad de una API externa (simulado)."""
        # Esta es una implementación simulada
        
        try:
            # Simular precios de electricidad por región
            simulated_prices = {
                "default": 0.15,
                "US": 0.13,
                "EU": 0.18,
                "ES": 0.16
            }
            
            return simulated_prices.get(region, 0.15)
        except Exception as e:
            print(f"Error al obtener precio de electricidad: {str(e)}")
            return 0.15
    
    def update_settings_from_api(self, settings_manager):
        """Actualiza la configuración desde una API externa."""
        try:
            # Obtener datos externos
            electricity_price = self.get_electricity_price()
            pla_price = self.get_filament_prices("PLA")
            
            # Actualizar configuración
            current_settings = settings_manager.load_settings()
            
            # Actualizar precio de electricidad si es diferente
            if electricity_price != current_settings.get('electricity_kwh_price', 0):
                current_settings['electricity_kwh_price'] = electricity_price
                
            # Actualizar precio de filamento PLA si es diferente
            if 'filaments' in current_settings and 'PLA' in current_settings['filaments']:
                if pla_price['price_per_kg'] != current_settings['filaments']['PLA'].get('price_per_kg', 0):
                    current_settings['filaments']['PLA']['price_per_kg'] = pla_price['price_per_kg']
                    current_settings['filaments']['PLA']['supplier'] = pla_price['supplier']
            
            # Guardar configuración actualizada
            settings_manager.save_settings(current_settings)
            
            return True, "Configuración actualizada desde API externa"
        except Exception as e:
            return False, f"Error al actualizar configuración: {str(e)}"
    
    def enable_integration(self, service, credentials):
        """Habilita una integración con credenciales."""
        try:
            self.config[service] = {
                "enabled": True,
                "credentials": credentials
            }
            self.save_config()
            return True, f"Integración {service} habilitada exitosamente"
        except Exception as e:
            return False, f"Error al habilitar integración: {str(e)}"
    
    def disable_integration(self, service):
        """Deshabilita una integración."""
        try:
            if service in self.config:
                self.config[service]["enabled"] = False
                self.save_config()
                return True, f"Integración {service} deshabilitada exitosamente"
            else:
                return False, f"Integración {service} no encontrada"
        except Exception as e:
            return False, f"Error al deshabilitar integración: {str(e)}"
    
    def get_available_integrations(self):
        """Devuelve las integraciones disponibles."""
        return [
            {"name": "Email", "description": "Envío de cotizaciones por correo"},
            {"name": "Dropbox", "description": "Almacenamiento en la nube"},
            {"name": "Google Drive", "description": "Almacenamiento en la nube"},
            {"name": "Filament API", "description": "Precios actualizados de filamentos"},
            {"name": "Electricity API", "description": "Precios actualizados de electricidad"}
        ]
