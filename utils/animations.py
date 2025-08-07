import flet as ft

class Animations:
    @staticmethod
    def fade_in_animation(duration=500, delay=0):
        """Crea una animación de aparición suave."""
        return ft.Animation(duration, "easeIn", delay)
    
    @staticmethod
    def scale_animation(duration=300, delay=0, curve="easeOutBack"):
        """Crea una animación de escala."""
        return ft.Animation(duration, curve, delay)
    
    @staticmethod
    def slide_in_animation(duration=400, delay=0, direction="up"):
        """Crea una animación de deslizamiento."""
        return ft.Animation(duration, "easeOutCubic", delay)
    
    @staticmethod
    def bounce_animation(duration=600, delay=0):
        """Crea una animación de rebote suave."""
        return ft.Animation(duration, "easeOutBounce", delay)
    
    @staticmethod
    def create_scale_transform(scale=1):
        """Crea una transformación de escala."""
        return ft.Scale(scale=scale)
    
    @staticmethod
    def create_offset_transform(x=0, y=0):
        """Crea una transformación de desplazamiento."""
        return ft.Offset(x, y)
    
    @staticmethod
    def create_rotate_transform(angle=0):
        """Crea una transformación de rotación."""
        return ft.Rotate(angle=angle)
    
    @staticmethod
    def pulse_animation(duration=1000, scale_min=0.95, scale_max=1.05):
        """Crea una animación de pulso (agrandar y reducir cíclicamente)."""
        return {
            "scale_min": scale_min,
            "scale_max": scale_max,
            "duration": duration,
            "curve": "easeInOut"
        }
    
    @staticmethod
    def shake_animation(duration=300, intensity=5):
        """Crea una animación de sacudida."""
        return {
            "intensity": intensity,
            "duration": duration,
            "curve": "easeInOut"
        }
    
    @staticmethod
    def flip_animation(duration=500):
        """Crea una animación de giro (volteo)."""
        return {
            "duration": duration,
            "curve": "easeOutCubic"
        }
    
    @staticmethod
    def color_transition_animation(duration=400):
        """Crea una animación de transición de color."""
        return ft.Animation(duration, "easeInOut")
