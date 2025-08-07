import flet as ft

class NotificationManager:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def show_snackbar(self, message: str, bgcolor="primary", duration=4000):
        """Muestra una notificación tipo snackbar."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=bgcolor,
            duration=duration,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_success(self, message: str, duration=4000):
        """Muestra una notificación de éxito."""
        self.show_snackbar(message, ft.colors.GREEN, duration)
    
    def show_error(self, message: str, duration=4000):
        """Muestra una notificación de error."""
        self.show_snackbar(message, ft.colors.RED, duration)
    
    def show_warning(self, message: str, duration=4000):
        """Muestra una notificación de advertencia."""
        self.show_snackbar(message, ft.colors.ORANGE, duration)
    
    def show_info(self, message: str, duration=4000):
        """Muestra una notificación de información."""
        self.show_snackbar(message, ft.colors.BLUE, duration)
    
    def show_dialog(self, title: str, content: str, actions=None):
        """Muestra un diálogo de notificación."""
        if actions is None:
            actions = [
                ft.TextButton("Aceptar", on_click=lambda e: self.page.close_dialog())
            ]
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(content),
            actions=actions,
        )
        self.page.open_dialog()
    
    def show_confirmation_dialog(self, title: str, content: str, on_confirm, on_cancel=None):
        """Muestra un diálogo de confirmación."""
        actions = [
            ft.TextButton("Cancelar", on_click=on_cancel or (lambda e: self.page.close_dialog())),
            ft.TextButton("Confirmar", on_click=on_confirm),
        ]
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(content),
            actions=actions,
        )
        self.page.open_dialog()
    
    def show_toast(self, message: str, duration=3000):
        """Muestra una notificación tipo toast (implementación futura)."""
        # Esta es una implementación base para futura expansión
        print(f"Toast: {message}")
        # En una implementación futura, aquí se mostraría una notificación toast
        return True
