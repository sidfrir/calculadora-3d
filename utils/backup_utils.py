import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class BackupUtils:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Asegura que el directorio de backups exista."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def backup_database(self, db_path, backup_name=None):
        """Crea un backup de la base de datos."""
        try:
            if not os.path.exists(db_path):
                return False, "Base de datos no encontrada"
            
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"database_backup_{timestamp}.db"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(db_path, backup_path)
            
            return True, f"Backup creado: {backup_path}"
        except Exception as e:
            return False, f"Error al crear backup: {str(e)}"
    
    def backup_settings(self, settings_path, backup_name=None):
        """Crea un backup de los archivos de configuración."""
        try:
            if not os.path.exists(settings_path):
                return False, "Archivo de configuración no encontrado"
            
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"settings_backup_{timestamp}.json"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(settings_path, backup_path)
            
            return True, f"Backup de configuración creado: {backup_path}"
        except Exception as e:
            return False, f"Error al crear backup de configuración: {str(e)}"
    
    def backup_all(self, db_path, settings_path):
        """Crea un backup completo de la aplicación."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"full_backup_{timestamp}"
            
            # Crear directorio para este backup
            backup_path = os.path.join(self.backup_dir, backup_name)
            os.makedirs(backup_path, exist_ok=True)
            
            # Copiar base de datos
            if os.path.exists(db_path):
                shutil.copy2(db_path, os.path.join(backup_path, "calculator_app.db"))
            
            # Copiar configuración
            if os.path.exists(settings_path):
                shutil.copy2(settings_path, os.path.join(backup_path, "settings.json"))
            
            # Crear archivo de información del backup
            info = {
                "backup_date": datetime.now().isoformat(),
                "backup_name": backup_name,
                "files_included": ["calculator_app.db", "settings.json"]
            }
            
            with open(os.path.join(backup_path, "backup_info.json"), 'w') as f:
                json.dump(info, f, indent=2)
            
            return True, f"Backup completo creado: {backup_path}"
        except Exception as e:
            return False, f"Error al crear backup completo: {str(e)}"
    
    def restore_database(self, backup_path, db_path):
        """Restaura la base de datos desde un backup."""
        try:
            if not os.path.exists(backup_path):
                return False, "Backup no encontrado"
            
            shutil.copy2(backup_path, db_path)
            return True, f"Base de datos restaurada desde: {backup_path}"
        except Exception as e:
            return False, f"Error al restaurar base de datos: {str(e)}"
    
    def restore_settings(self, backup_path, settings_path):
        """Restaura la configuración desde un backup."""
        try:
            if not os.path.exists(backup_path):
                return False, "Backup no encontrado"
            
            shutil.copy2(backup_path, settings_path)
            return True, f"Configuración restaurada desde: {backup_path}"
        except Exception as e:
            return False, f"Error al restaurar configuración: {str(e)}"
    
    def list_backups(self):
        """Lista todos los backups disponibles."""
        try:
            backups = []
            for item in os.listdir(self.backup_dir):
                item_path = os.path.join(self.backup_dir, item)
                if os.path.isfile(item_path):
                    backups.append({
                        "name": item,
                        "path": item_path,
                        "size": os.path.getsize(item_path),
                        "modified": os.path.getmtime(item_path)
                    })
                elif os.path.isdir(item_path):
                    # Para backups completos
                    info_file = os.path.join(item_path, "backup_info.json")
                    if os.path.exists(info_file):
                        with open(info_file, 'r') as f:
                            info = json.load(f)
                        backups.append({
                            "name": item,
                            "path": item_path,
                            "info": info,
                            "modified": os.path.getmtime(item_path)
                        })
            
            # Ordenar por fecha de modificación (más reciente primero)
            backups.sort(key=lambda x: x["modified"], reverse=True)
            return backups
        except Exception as e:
            print(f"Error al listar backups: {str(e)}")
            return []
    
    def delete_backup(self, backup_name):
        """Elimina un backup específico."""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if os.path.exists(backup_path):
                if os.path.isfile(backup_path):
                    os.remove(backup_path)
                elif os.path.isdir(backup_path):
                    shutil.rmtree(backup_path)
                return True, f"Backup eliminado: {backup_name}"
            else:
                return False, "Backup no encontrado"
        except Exception as e:
            return False, f"Error al eliminar backup: {str(e)}"
    
    def get_backup_info(self, backup_name):
        """Obtiene información detallada de un backup."""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                return None
            
            if os.path.isfile(backup_path):
                # Backup simple
                return {
                    "name": backup_name,
                    "path": backup_path,
                    "size": os.path.getsize(backup_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(backup_path)).isoformat()
                }
            elif os.path.isdir(backup_path):
                # Backup completo
                info_file = os.path.join(backup_path, "backup_info.json")
                if os.path.exists(info_file):
                    with open(info_file, 'r') as f:
                        info = json.load(f)
                    return {
                        "name": backup_name,
                        "path": backup_path,
                        "info": info,
                        "modified": datetime.fromtimestamp(os.path.getmtime(backup_path)).isoformat()
                    }
            return None
        except Exception as e:
            print(f"Error al obtener información del backup: {str(e)}")
            return None
