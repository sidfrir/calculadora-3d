import flet as ft

class CustomThemes:
    @staticmethod
    def create_light_theme():
        """Crea un tema claro personalizado."""
        return ft.Theme(
            color_scheme_seed="indigo",
        )
    
    @staticmethod
    def create_dark_theme():
        """Crea un tema oscuro personalizado."""
        return ft.Theme(
            color_scheme_seed="indigo",
        )
    
    @staticmethod
    def create_high_contrast_theme():
        """Crea un tema de alto contraste para accesibilidad."""
        return ft.Theme(
            color_scheme_seed="blue",
        )
    
    @staticmethod
    def create_color_blind_friendly_theme():
        """Crea un tema amigable para daltónicos."""
        return ft.Theme(
            color_scheme_seed="blue",
        )
    
    @staticmethod
    def apply_theme(page, theme_mode, user_preferences):
        """Aplica el tema seleccionado a la página."""
        if not user_preferences.get("animations_enabled", True):
            # Tema simplificado si las animaciones están desactivadas
            page.theme = ft.Theme(
                color_scheme_seed="indigo",
            )
            page.dark_theme = ft.Theme(
                color_scheme_seed="indigo",
            )
        else:
            # Aplicar temas completos
            if theme_mode == "light":
                page.theme = CustomThemes.create_light_theme()
            elif theme_mode == "dark":
                page.dark_theme = CustomThemes.create_dark_theme()
            elif theme_mode == "high_contrast":
                page.theme = CustomThemes.create_high_contrast_theme()
            elif theme_mode == "color_blind":
                page.theme = CustomThemes.create_color_blind_friendly_theme()
            else:
                # Tema predeterminado del sistema
                page.theme = CustomThemes.create_light_theme()
                page.dark_theme = CustomThemes.create_dark_theme()
