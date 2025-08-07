import requests
import json
import os
from packaging import version

class AppUpdater:
    def __init__(self, current_version="1.0.0", update_url="https://api.github.com/repos/usuario/calculadora-3d/releases/latest"):
        self.current_version = current_version
        self.update_url = update_url
    
    def check_for_updates(self):
        """Verifica si hay actualizaciones disponibles."""
        try:
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data.get("tag_name", "").lstrip("v")
            
            if version.parse(latest_version) > version.parse(self.current_version):
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "current_version": self.current_version,
                    "release_notes": release_data.get("body", ""),
                    "download_url": release_data.get("html_url", ""),
                    "published_at": release_data.get("published_at", "")
                }
            else:
                return {
                    "update_available": False,
                    "latest_version": latest_version,
                    "current_version": self.current_version
                }
        except requests.RequestException as e:
            return {
                "error": f"No se pudo conectar al servidor de actualizaciones: {str(e)}"
            }
        except version.InvalidVersion as e:
            return {
                "error": f"Versión inválida: {str(e)}"
            }
        except Exception as e:
            return {
                "error": f"Error inesperado al verificar actualizaciones: {str(e)}"
            }
    
    def download_update(self, download_url, destination_path):
        """Descarga la actualización (implementación básica)."""
        try:
            response = requests.get(download_url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Error al descargar actualización: {e}")
            return False
    
    def is_update_required(self, min_required_version):
        """Verifica si se requiere una actualización mínima."""
        try:
            return version.parse(self.current_version) < version.parse(min_required_version)
        except version.InvalidVersion:
            return True  # Si no se puede parsear, asumir que se necesita actualización
    
    def get_changelog(self, versions_count=5):
        """Obtiene el registro de cambios de las últimas versiones."""
        try:
            response = requests.get(self.update_url.replace("latest", ""), timeout=10)
            response.raise_for_status()
            
            releases = response.json()
            changelog = []
            
            for release in releases[:versions_count]:
                changelog.append({
                    "version": release.get("tag_name", "").lstrip("v"),
                    "date": release.get("published_at", ""),
                    "notes": release.get("body", "")
                })
            
            return changelog
        except Exception as e:
            return [{"error": f"No se pudo obtener el registro de cambios: {str(e)}"}]
    
    def update_version_file(self, new_version):
        """Actualiza el archivo de versión de la aplicación."""
        try:
            version_file = "version.json"
            version_data = {"version": new_version}
            
            with open(version_file, 'w') as f:
                json.dump(version_data, f, indent=2)
            
            self.current_version = new_version
            return True
        except Exception as e:
            print(f"Error al actualizar archivo de versión: {e}")
            return False
