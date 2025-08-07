import flet as ft

class VisualEffects:
    @staticmethod
    def create_gradient_background(colors, begin=ft.alignment.top_left, end=ft.alignment.bottom_right):
        """Crea un fondo degradado."""
        return ft.LinearGradient(
            begin=begin,
            end=end,
            colors=colors,
        )
    
    @staticmethod
    def create_shadow(elevation=5, color="black26"):
        """Crea un efecto de sombra."""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=elevation,
            color=color,
        )
    
    @staticmethod
    def create_blur_effect(sigma_x=10, sigma_y=10):
        """Crea un efecto de desenfoque."""
        return ft.Blur(sigma_x, sigma_y, ft.BlurTileMode.MIRROR)
    
    @staticmethod
    def create_card_elevation(elevation=8):
        """Crea una elevación para tarjetas."""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=elevation,
            color="black26",
        )
    
    @staticmethod
    def create_glass_effect(blur_sigma=10, opacity=0.8):
        """Crea un efecto de vidrio esmerilado."""
        return {
            "blur": ft.Blur(blur_sigma, blur_sigma, ft.BlurTileMode.MIRROR),
            "opacity": opacity
        }
    
    @staticmethod
    def create_ripple_effect(color=ft.colors.PRIMARY, duration=200):
        """Crea un efecto de onda al hacer clic."""
        return {
            "color": color,
            "duration": duration
        }
    
    @staticmethod
    def create_hover_elevation(elevation=12):
        """Crea un efecto de elevación al pasar el mouse."""
        return ft.BoxShadow(
            spread_radius=2,
            blur_radius=elevation,
            color="black38",
        )
    
    @staticmethod
    def create_border_radius(radius=12):
        """Crea un borde redondeado."""
        return ft.border_radius.all(radius)
    
    @staticmethod
    def create_soft_border(color=ft.colors.OUTLINE_VARIANT, width=1):
        """Crea un borde suave."""
        return ft.BorderSide(width, color)
    
    @staticmethod
    def create_neumorphic_effect():
        """Crea un efecto neumórfico (soft UI)."""
        return {
            "light_shadow": ft.BoxShadow(
                spread_radius=-1,
                blur_radius=5,
                color=ft.colors.WHITE24,
                offset=ft.Offset(-1, -1)
            ),
            "dark_shadow": ft.BoxShadow(
                spread_radius=-1,
                blur_radius=5,
                color="black26",
                offset=ft.Offset(1, 1)
            )
        }
    
    @staticmethod
    def create_floating_effect():
        """Crea un efecto de flotación."""
        return {
            "shadow": ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color="black26",
            ),
            "transform": ft.Scale(scale=1.02)
        }
