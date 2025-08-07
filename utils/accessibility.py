import flet as ft

class Accessibility:
    def __init__(self, page: ft.Page):
        self.page = page
        self.font_scaling = 1.0
        self.high_contrast = False
        self.reduce_motion = False
        self.screen_reader = False
    
    def set_font_scaling(self, scale_factor):
        """Ajusta el tamaño de fuente de la aplicación."""
        if 0.5 <= scale_factor <= 2.0:
            self.font_scaling = scale_factor
            # Aplicar el cambio de escala
            self.apply_font_scaling()
            return True
        return False
    
    def apply_font_scaling(self):
        """Aplica el cambio de escala de fuente a toda la aplicación."""
        # Esta función requeriría modificaciones en los estilos de la aplicación
        # para aplicar el factor de escala a todas las fuentes
        print(f"Aplicando escala de fuente: {self.font_scaling}x")
        return True
    
    def toggle_high_contrast(self, enabled=None):
        """Activa o desactiva el modo de alto contraste."""
        if enabled is not None:
            self.high_contrast = enabled
        else:
            self.high_contrast = not self.high_contrast
        
        # Aplicar el cambio de alto contraste
        self.apply_high_contrast()
        return self.high_contrast
    
    def apply_high_contrast(self):
        """Aplica el modo de alto contraste a la aplicación."""
        if self.high_contrast:
            print("Modo de alto contraste activado")
            # Aquí se aplicarían los cambios de tema para alto contraste
        else:
            print("Modo de alto contraste desactivado")
            # Aquí se restauraría el tema normal
        return True
    
    def toggle_reduce_motion(self, enabled=None):
        """Activa o desactiva la reducción de movimiento."""
        if enabled is not None:
            self.reduce_motion = enabled
        else:
            self.reduce_motion = not self.reduce_motion
        
        # Aplicar el cambio de reducción de movimiento
        self.apply_reduce_motion()
        return self.reduce_motion
    
    def apply_reduce_motion(self):
        """Aplica la reducción de movimiento a la aplicación."""
        if self.reduce_motion:
            print("Reducción de movimiento activada")
            # Aquí se desactivarían las animaciones
        else:
            print("Reducción de movimiento desactivada")
            # Aquí se reactivarían las animaciones
        return True
    
    def toggle_screen_reader(self, enabled=None):
        """Activa o desactiva el soporte para lector de pantalla."""
        if enabled is not None:
            self.screen_reader = enabled
        else:
            self.screen_reader = not self.screen_reader
        
        # Aplicar el cambio de soporte para lector de pantalla
        self.apply_screen_reader()
        return self.screen_reader
    
    def apply_screen_reader(self):
        """Aplica el soporte para lector de pantalla."""
        if self.screen_reader:
            print("Soporte para lector de pantalla activado")
            # Aquí se añadirían etiquetas de accesibilidad
        else:
            print("Soporte para lector de pantalla desactivado")
            # Aquí se removerían etiquetas de accesibilidad
        return True
    
    def get_accessibility_settings(self):
        """Devuelve las configuraciones de accesibilidad actuales."""
        return {
            "font_scaling": self.font_scaling,
            "high_contrast": self.high_contrast,
            "reduce_motion": self.reduce_motion,
            "screen_reader": self.screen_reader
        }
    
    def load_accessibility_settings(self, settings_dict):
        """Carga las configuraciones de accesibilidad desde un diccionario."""
        if "font_scaling" in settings_dict:
            self.set_font_scaling(settings_dict["font_scaling"])
        
        if "high_contrast" in settings_dict:
            self.toggle_high_contrast(settings_dict["high_contrast"])
        
        if "reduce_motion" in settings_dict:
            self.toggle_reduce_motion(settings_dict["reduce_motion"])
        
        if "screen_reader" in settings_dict:
            self.toggle_screen_reader(settings_dict["screen_reader"])
        
        return True
    
    def increase_font_size(self):
        """Aumenta el tamaño de fuente en un incremento estándar."""
        new_scale = min(self.font_scaling + 0.1, 2.0)
        return self.set_font_scaling(new_scale)
    
    def decrease_font_size(self):
        """Disminuye el tamaño de fuente en un incremento estándar."""
        new_scale = max(self.font_scaling - 0.1, 0.5)
        return self.set_font_scaling(new_scale)
