import hashlib
import json
import os
from datetime import datetime, timedelta

class Authentication:
    def __init__(self, auth_file="auth.json"):
        self.auth_file = auth_file
        self.users = self.load_users()
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
    
    def load_users(self):
        """Carga los usuarios desde el archivo de autenticación."""
        if os.path.exists(self.auth_file):
            try:
                with open(self.auth_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_users(self):
        """Guarda los usuarios en el archivo de autenticación."""
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            return True
        except IOError:
            return False
    
    def hash_password(self, password):
        """Genera un hash SHA-256 de la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, role="user"):
        """Crea un nuevo usuario."""
        if username in self.users:
            return False, "El usuario ya existe"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        self.users[username] = {
            "password_hash": self.hash_password(password),
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        self.save_users()
        return True, "Usuario creado exitosamente"
    
    def authenticate_user(self, username, password):
        """Autentica a un usuario."""
        if username not in self.users:
            return False, "Usuario no encontrado"
        
        user = self.users[username]
        if user["password_hash"] != self.hash_password(password):
            return False, "Contraseña incorrecta"
        
        # Actualizar último inicio de sesión
        user["last_login"] = datetime.now().isoformat()
        self.save_users()
        
        # Crear sesión
        self.current_user = username
        self.session_token = self.generate_session_token(username)
        self.session_expiry = datetime.now() + timedelta(hours=24)
        
        return True, "Autenticación exitosa"
    
    def generate_session_token(self, username):
        """Genera un token de sesión."""
        data = f"{username}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def validate_session(self):
        """Valida la sesión actual."""
        if not self.current_user or not self.session_token:
            return False, "No hay sesión activa"
        
        if datetime.now() > self.session_expiry:
            self.logout()
            return False, "Sesión expirada"
        
        return True, "Sesión válida"
    
    def logout(self):
        """Cierra la sesión actual."""
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
        return True, "Sesión cerrada"
    
    def change_password(self, username, old_password, new_password):
        """Cambia la contraseña de un usuario."""
        if username not in self.users:
            return False, "Usuario no encontrado"
        
        user = self.users[username]
        if user["password_hash"] != self.hash_password(old_password):
            return False, "Contraseña actual incorrecta"
        
        if len(new_password) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres"
        
        user["password_hash"] = self.hash_password(new_password)
        self.save_users()
        return True, "Contraseña cambiada exitosamente"
    
    def get_user_role(self, username):
        """Obtiene el rol de un usuario."""
        if username in self.users:
            return self.users[username].get("role", "user")
        return None
    
    def has_permission(self, username, permission):
        """Verifica si un usuario tiene un permiso específico."""
        role = self.get_user_role(username)
        if not role:
            return False
        
        # Definir permisos por rol
        permissions = {
            "admin": ["read", "write", "delete", "export", "import", "settings"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
        
        user_permissions = permissions.get(role, [])
        return permission in user_permissions
    
    def delete_user(self, username, admin_password):
        """Elimina un usuario (requiere autenticación de administrador)."""
        # Verificar que el usuario actual sea administrador
        if not self.current_user:
            return False, "Debes estar autenticado como administrador"
        
        if self.get_user_role(self.current_user) != "admin":
            return False, "Solo los administradores pueden eliminar usuarios"
        
        # Verificar contraseña de administrador
        admin_user = self.users.get(self.current_user, {})
        if admin_user.get("password_hash") != self.hash_password(admin_password):
            return False, "Contraseña de administrador incorrecta"
        
        if username not in self.users:
            return False, "Usuario no encontrado"
        
        # No permitir que un administrador se elimine a sí mismo
        if username == self.current_user:
            return False, "No puedes eliminarte a ti mismo"
        
        del self.users[username]
        self.save_users()
        return True, "Usuario eliminado exitosamente"
    
    def list_users(self):
        """Lista todos los usuarios (solo para administradores)."""
        if not self.current_user:
            return False, "Debes estar autenticado"
        
        if self.get_user_role(self.current_user) != "admin":
            return False, "Solo los administradores pueden listar usuarios"
        
        user_list = []
        for username, user_data in self.users.items():
            user_list.append({
                "username": username,
                "role": user_data.get("role", "user"),
                "created_at": user_data.get("created_at", ""),
                "last_login": user_data.get("last_login", "Nunca")
            })
        
        return True, user_list
    
    def update_user_role(self, username, new_role, admin_password):
        """Actualiza el rol de un usuario (requiere autenticación de administrador)."""
        # Verificar que el usuario actual sea administrador
        if not self.current_user:
            return False, "Debes estar autenticado como administrador"
        
        if self.get_user_role(self.current_user) != "admin":
            return False, "Solo los administradores pueden cambiar roles"
        
        # Verificar contraseña de administrador
        admin_user = self.users.get(self.current_user, {})
        if admin_user.get("password_hash") != self.hash_password(admin_password):
            return False, "Contraseña de administrador incorrecta"
        
        if username not in self.users:
            return False, "Usuario no encontrado"
        
        valid_roles = ["admin", "user", "guest"]
        if new_role not in valid_roles:
            return False, f"Rol inválido. Roles válidos: {valid_roles}"
        
        self.users[username]["role"] = new_role
        self.save_users()
        return True, "Rol de usuario actualizado exitosamente"
    
    def reset_user_password(self, username, admin_password):
        """Restablece la contraseña de un usuario (requiere autenticación de administrador)."""
        # Verificar que el usuario actual sea administrador
        if not self.current_user:
            return False, "Debes estar autenticado como administrador"
        
        if self.get_user_role(self.current_user) != "admin":
            return False, "Solo los administradores pueden restablecer contraseñas"
        
        # Verificar contraseña de administrador
        admin_user = self.users.get(self.current_user, {})
        if admin_user.get("password_hash") != self.hash_password(admin_password):
            return False, "Contraseña de administrador incorrecta"
        
        if username not in self.users:
            return False, "Usuario no encontrado"
        
        # Generar nueva contraseña temporal
        import random
        import string
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        self.users[username]["password_hash"] = self.hash_password(temp_password)
        self.save_users()
        
        return True, f"Contraseña restablecida. Nueva contraseña temporal: {temp_password}"
