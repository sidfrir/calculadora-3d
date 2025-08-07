import flet as ft


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/"
        self.page = page
        self.appbar = ft.AppBar(
            title=ft.Text(
                "Calculadora 3D Pro",
                size=22,
                weight=ft.FontWeight.BOLD,
                color="onprimary"
            ),
            bgcolor="primary",
            elevation=8,
            center_title=True,
            shadow_color="black26",
        )
        
        # Crear una interfaz moderna y atractiva con efectos visuales
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(
                                "view_in_ar",
                                size=120,
                                color="primary",
                            ),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=30, bottom=10),
                            animate_scale=ft.Animation(duration=800, curve="easeOutBack"),
                            scale=1.0,
                            bgcolor="primarycontainer",
                            border_radius=60,
                            width=120,
                            height=120,
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=15,
                                color="primarycontainer",
                                offset=ft.Offset(0, 5),
                            ),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    "Calculadora 3D Pro",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                    color="primary",
                                ),
                                ft.Text(
                                    "v2.0",
                                    size=14,
                                    text_align=ft.TextAlign.CENTER,
                                    color="onsurfacevariant",
                                    weight=ft.FontWeight.W_400,
                                )
                            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=20, bottom=10),
                            animate_opacity=ft.Animation(duration=600, curve="easeIn"),
                            opacity=1,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Calcula fácilmente el costo de tus impresiones 3D con precisión profesional",
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                                color="onSurfaceVariant",
                                weight=ft.FontWeight.W_400,
                            ),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=10, bottom=30),
                            animate_offset=ft.Animation(duration=400, curve="easeOut"),
                            offset=ft.Offset(0, 0),
                            padding=ft.padding.symmetric(horizontal=30),
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    # Funcionalidades principales
                                    self._create_feature_card(
                                        "calculate_outlined",
                                        "Calcular Precios",
                                        "Calcula el costo total de tus impresiones considerando material, tiempo y electricidad",
                                        "/calculator"
                                    ),
                                    self._create_feature_card(
                                        "work_outlined",
                                        "Gestión de Proyectos", 
                                        "Administra tus proyectos de impresión 3D, seguimiento de estados y presupuestos",
                                        "/projects"
                                    ),
                                    self._create_feature_card(
                                        "people_outlined",
                                        "Gestión de Clientes",
                                        "Administra tu base de datos de clientes con información de contacto y preferencias",
                                        "/clients" 
                                    ),
                                    # Funcionalidades secundarias
                                    self._create_feature_card(
                                        "history_outlined",
                                        "Historial",
                                        "Guarda y consulta tus cotizaciones anteriores",
                                        "/history"
                                    ),
                                    self._create_feature_card(
                                        "settings_outlined",
                                        "Configuración",
                                        "Personaliza los costos según tu impresora y materiales",
                                        "/settings"
                                    ),
                                ],
                                spacing=20,
                            ),
                            padding=25,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon("calculate", color="onprimary"),
                                        ft.Text(
                                            "Comenzar a calcular", 
                                            size=16, 
                                            weight=ft.FontWeight.BOLD,
                                            color="onprimary"
                                        )
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                    on_click=lambda _: page.go("/calculator"),
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(horizontal=40, vertical=20),
                                        shape=ft.RoundedRectangleBorder(radius=25),
                                        elevation=12,
                                        bgcolor="primary",
                                        animation_duration=200,
                                        shadow_color="primary",
                                    ),
                                    width=280,
                                    height=60,
                                ),
                                ft.Row([
                                    ft.TextButton(
                                        text="Ver Historial",
                                        icon="history",
                                        on_click=lambda _: page.go("/history"),
                                        style=ft.ButtonStyle(
                                            color="primary",
                                        )
                                    ),
                                    ft.TextButton(
                                        text="Configuración",
                                        icon="settings",
                                        on_click=lambda _: page.go("/settings"),
                                        style=ft.ButtonStyle(
                                            color="primary",
                                        )
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=20, bottom=30),
                            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
                            scale=1.0,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                ),
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["background", "surfacevariant"],
                    stops=[0.0, 1.0],
                ),
                padding=ft.padding.all(20),
            )
        ]
    
    def _create_feature_card(self, icon, title, description, route=None):
        def on_card_click(e):
            if route:
                self.page.go(route)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                icon, 
                                size=32, 
                                color="onprimarycontainer"
                            ),
                            bgcolor="primarycontainer",
                            border_radius=20,
                            padding=16,
                            width=64,
                            height=64,
                            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
                            scale=1.0,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=8,
                                color="primarycontainer",
                                offset=ft.Offset(0, 2),
                            ),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    title, 
                                    size=18, 
                                    weight=ft.FontWeight.BOLD, 
                                    color="primary"
                                ),
                                ft.Text(
                                    description, 
                                    size=14, 
                                    color="onsurfacevariant",
                                    weight=ft.FontWeight.W_400
                                ),
                            ],
                            spacing=6,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Icon(
                                "arrow_forward_ios",
                                size=18,
                                color="primary"
                            ),
                            visible=route is not None
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                ),
                padding=20,
                on_click=on_card_click if route else None,
                ink=True if route else False,
            ),
            elevation=6,
            shadow_color="black26",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
            scale=1.0,
            color="surfacevariant",
            margin=ft.margin.symmetric(horizontal=5),
        )
