import flet as ft

class HelpSystem:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tutorials = self._load_tutorials()
        self.faq = self._load_faq()
    
    def _load_tutorials(self):
        """Carga los tutoriales disponibles."""
        return {
            "getting_started": {
                "title": "Primeros Pasos",
                "description": "Aprende a usar la calculadora 3D Pro",
                "steps": [
                    "Configura tus costos en la sección de Configuración",
                    "Ingresa los datos de tu pieza en la calculadora",
                    "Ajusta el margen de ganancia según tus necesidades",
                    "Guarda la cotización para futuras referencias"
                ]
            },
            "cost_setup": {
                "title": "Configuración de Costos",
                "description": "Cómo configurar correctamente los costos de tu impresora",
                "steps": [
                    "Establece el costo por hora de tu máquina",
                    "Ingresa el precio de la electricidad en tu zona",
                    "Define el consumo en watts de tu impresora",
                    "Configura los precios de tus filamentos"
                ]
            },
            "advanced_features": {
                "title": "Funciones Avanzadas",
                "description": "Descubre las funciones avanzadas de la aplicación",
                "steps": [
                    "Usa plantillas para cotizaciones recurrentes",
                    "Exporta tus cotizaciones en diferentes formatos",
                    "Genera reportes de rentabilidad",
                    "Configura copias de seguridad automáticas"
                ]
            }
        }
    
    def _load_faq(self):
        """Carga las preguntas frecuentes."""
        return [
            {
                "question": "¿Cómo se calcula el costo de material?",
                "answer": "El costo de material se calcula multiplicando el peso del filamento usado (en kg) por el precio por kg del filamento seleccionado."
            },
            {
                "question": "¿Qué incluye el costo de mano de obra?",
                "answer": "El costo de mano de obra incluye el tiempo de impresión multiplicado por el costo por hora de la máquina, más el costo de electricidad consumida durante la impresión."
            },
            {
                "question": "¿Cómo cambio el tema de la aplicación?",
                "answer": "Puedes cambiar el tema en la sección de Configuración, en la pestaña de Apariencia."
            },
            {
                "question": "¿Puedo exportar mis cotizaciones?",
                "answer": "Sí, puedes exportar tus cotizaciones en formato CSV, JSON, XML, TXT y HTML desde el historial."
            },
            {
                "question": "¿Cómo hago copias de seguridad?",
                "answer": "Puedes crear copias de seguridad de tus datos desde la sección de Configuración, en la pestaña de Copias de Seguridad."
            }
        ]
    
    def show_tutorial(self, tutorial_id):
        """Muestra un tutorial específico."""
        if tutorial_id not in self.tutorials:
            return False, "Tutorial no encontrado"
        
        tutorial = self.tutorials[tutorial_id]
        
        # Crear contenido del tutorial
        content_controls = [
            ft.Text(tutorial["title"], size=24, weight=ft.FontWeight.BOLD, color="primary"),
            ft.Text(tutorial["description"], size=16, italic=True),
            ft.Divider(height=20),
        ]
        
        for i, step in enumerate(tutorial["steps"], 1):
            content_controls.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(str(i), color="onprimary", size=14, weight=ft.FontWeight.BOLD),
                        width=24,
                        height=24,
                        bgcolor="primary",
                        border_radius=12,
                        alignment=ft.alignment.center
                    ),
                    ft.Text(step, size=14)
                ], spacing=10)
            )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Tutorial", weight=ft.FontWeight.BOLD),
            content=ft.Column(content_controls, spacing=15, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        
        self.page.dialog = dialog
        self.page.open_dialog()
        
        return True, "Tutorial mostrado"
    
    def show_faq(self):
        """Muestra las preguntas frecuentes."""
        content_controls = [
            ft.Text("Preguntas Frecuentes", size=24, weight=ft.FontWeight.BOLD, color="primary"),
            ft.Divider(height=20),
        ]
        
        for item in self.faq:
            content_controls.append(
                ft.Column([
                    ft.Text(item["question"], size=16, weight=ft.FontWeight.W_500),
                    ft.Text(item["answer"], size=14),
                ], spacing=5)
            )
            content_controls.append(ft.Divider(height=10))
        
        dialog = ft.AlertDialog(
            title=ft.Text("Ayuda - Preguntas Frecuentes", weight=ft.FontWeight.BOLD),
            content=ft.Column(content_controls, spacing=10, scroll=ft.ScrollMode.AUTO, height=400),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        
        self.page.dialog = dialog
        self.page.open_dialog()
        
        return True, "FAQ mostrado"
    
    def show_quick_help(self, context="general"):
        """Muestra ayuda rápida según el contexto."""
        help_texts = {
            "calculator": [
                "Ingresa el tiempo de impresión en horas",
                "Ingresa el peso de filamento usado en gramos",
                "Ajusta el margen de ganancia según tu negocio",
                "Haz clic en Calcular para obtener el precio"
            ],
            "settings": [
                "Configura los costos reales de tu impresora",
                "Establece precios actualizados de filamentos",
                "Guarda los cambios para aplicar la configuración"
            ],
            "history": [
                "Visualiza todas tus cotizaciones guardadas",
                "Filtra por nombre de pieza o rango de fechas",
                "Exporta tus cotizaciones en diferentes formatos"
            ],
            "general": [
                "Usa la barra de navegación inferior para moverte entre secciones",
                "Accede a la configuración desde el menú de la barra superior",
                "Encuentra ayuda en cualquier momento con el botón de ayuda"
            ]
        }
        
        texts = help_texts.get(context, help_texts["general"])
        
        content_controls = [
            ft.Text("Ayuda Rápida", size=20, weight=ft.FontWeight.BOLD, color="primary"),
        ]
        
        for text in texts:
            content_controls.append(ft.Text(f"• {text}", size=14))
        
        dialog = ft.AlertDialog(
            content=ft.Column(content_controls, spacing=10),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        
        self.page.dialog = dialog
        self.page.open_dialog()
        
        return True, "Ayuda rápida mostrada"
    
    def show_about(self):
        """Muestra información sobre la aplicación."""
        content_controls = [
            ft.Text("Calculadora 3D Pro", size=24, weight=ft.FontWeight.BOLD, color="primary"),
            ft.Text("Versión 1.0.0", size=16, italic=True),
            ft.Divider(height=20),
            ft.Text("Una aplicación para calcular costos de impresión 3D de manera precisa y profesional."),
            ft.Divider(height=20),
            ft.Text("Características principales:", weight=ft.FontWeight.W_500),
            ft.Text("• Cálculo preciso de costos de material y mano de obra"),
            ft.Text("• Configuración personalizable de costos"),
            ft.Text("• Historial de cotizaciones"),
            ft.Text("• Exportación en múltiples formatos"),
            ft.Text("• Generación de reportes"),
            ft.Text("• Copias de seguridad"),
            ft.Divider(height=20),
            ft.Text("Desarrollado por: Equipo de Desarrollo 3D", italic=True),
        ]
        
        dialog = ft.AlertDialog(
            title=ft.Text("Acerca de", weight=ft.FontWeight.BOLD),
            content=ft.Column(content_controls, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        
        self.page.dialog = dialog
        self.page.open_dialog()
        
        return True, "Información mostrada"
    
    def get_available_tutorials(self):
        """Devuelve la lista de tutoriales disponibles."""
        return [
            {"id": key, "title": value["title"], "description": value["description"]}
            for key, value in self.tutorials.items()
        ]
