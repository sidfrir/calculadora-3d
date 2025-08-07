import flet as ft
import json
import os
from datetime import datetime

class SimpleCalculator:
    def __init__(self):
        self.settings = {
            'machine_cost_per_hour': 5.0,
            'electricity_kwh_price': 0.15,
            'printer_power_watts': 200,
            'filaments': {
                'PLA': {'price_per_kg': 25.0},
                'ABS': {'price_per_kg': 30.0},
                'PETG': {'price_per_kg': 35.0}
            },
            'currency_symbol': '$'
        }
    
    def calculate_cost(self, weight_g, hours, filament_type, margin_percent):
        weight_kg = weight_g / 1000
        filament_cost = weight_kg * self.settings['filaments'][filament_type]['price_per_kg']
        machine_cost = hours * self.settings['machine_cost_per_hour']
        electricity_cost = (self.settings['printer_power_watts'] / 1000) * hours * self.settings['electricity_kwh_price']
        
        subtotal = filament_cost + machine_cost + electricity_cost
        margin = subtotal * (margin_percent / 100)
        total = subtotal + margin
        
        return {
            'filament_cost': filament_cost,
            'machine_cost': machine_cost,
            'electricity_cost': electricity_cost,
            'subtotal': subtotal,
            'margin': margin,
            'total': total
        }

def main(page: ft.Page):
    page.title = "Calculadora 3D Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 700
    
    calculator = SimpleCalculator()
    
    # Campos de entrada
    piece_name = ft.TextField(label="Nombre de la pieza", width=300)
    weight_field = ft.TextField(label="Peso (gramos)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    hours_field = ft.TextField(label="Horas de impresión", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    filament_dropdown = ft.Dropdown(
        label="Filamento",
        width=300,
        options=[
            ft.dropdown.Option("PLA"),
            ft.dropdown.Option("ABS"),
            ft.dropdown.Option("PETG")
        ],
        value="PLA"
    )
    
    margin_field = ft.TextField(label="Margen (%)", keyboard_type=ft.KeyboardType.NUMBER, width=300, value="20")
    
    # Resultado
    result_text = ft.Text(value="", size=16)
    
    def calculate_click(e):
        try:
            weight = float(weight_field.value)
            hours = float(hours_field.value)
            margin = float(margin_field.value)
            filament = filament_dropdown.value
            
            result = calculator.calculate_cost(weight, hours, filament, margin)
            
            result_text.value = f"""
Costo de Filamento: ${result['filament_cost']:.2f}
Costo de Máquina: ${result['machine_cost']:.2f}
Costo de Electricidad: ${result['electricity_cost']:.2f}
Subtotal: ${result['subtotal']:.2f}
Margen: ${result['margin']:.2f}
TOTAL: ${result['total']:.2f}
            """
            page.update()
        except ValueError:
            result_text.value = "Error: Verifica los valores ingresados"
            page.update()
    
    calculate_button = ft.ElevatedButton(
        "Calcular",
        on_click=calculate_click,
        width=300,
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE
    )
    
    page.add(
        ft.Column([
            ft.Text("Calculadora 3D Pro", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            piece_name,
            weight_field,
            hours_field,
            filament_dropdown,
            margin_field,
            ft.Container(height=10),
            calculate_button,
            ft.Container(height=10),
            result_text
        ], alignment=ft.MainAxisAlignment.START, spacing=10)
    )

if __name__ == "__main__":
    ft.app(target=main)
