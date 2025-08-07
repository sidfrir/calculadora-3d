"""
Aplicación de Gestión 3D Pro

Aplicación principal para la gestión de proyectos, clientes, materiales, 
impresoras, tareas, presupuestos y análisis del sistema 3D Pro.
"""

import sys
import os
from datetime import datetime

# Añadir el directorio utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.project_manager import ProjectManager
from utils.client_manager import ClientManager
from utils.material_manager import MaterialManager
from utils.printer_manager import PrinterManager
from utils.task_manager import TaskManager
from utils.budget_manager import BudgetManager
from utils.analytics import Analytics


class Gestion3DPro:
    """Clase principal para la gestión del sistema 3D Pro"""
    
    def __init__(self):
        """Inicializa todos los gestores del sistema"""
        self.project_manager = ProjectManager()
        self.client_manager = ClientManager()
        self.material_manager = MaterialManager()
        self.printer_manager = PrinterManager()
        self.task_manager = TaskManager()
        self.budget_manager = BudgetManager()
        self.analytics = Analytics()
        
        print("Sistema de Gestión 3D Pro inicializado correctamente.")
    
    def run_demo(self):
        """Ejecuta una demostración del sistema"""
        print("\n=== DEMOSTRACIÓN DEL SISTEMA DE GESTIÓN 3D PRO ===\n")
        
        # Demostración de gestión de proyectos
        self._demo_projects()
        
        # Demostración de gestión de clientes
        self._demo_clients()
        
        # Demostración de gestión de materiales
        self._demo_materials()
        
        # Demostración de gestión de impresoras
        self._demo_printers()
        
        # Demostración de gestión de tareas
        self._demo_tasks()
        
        # Demostración de gestión de presupuestos
        self._demo_budgets()
        
        # Demostración de análisis
        self._demo_analytics()
        
        print("\n=== FIN DE LA DEMOSTRACIÓN ===\n")
    
    def _demo_projects(self):
        """Demostración de gestión de proyectos"""
        print("--- Gestión de Proyectos ---")
        
        # Crear un proyecto
        project = self.project_manager.create_project(
            name="Proyecto de Impresión Personalizada",
            description="Creación de piezas personalizadas para cliente importante"
        )
        print(f"✓ Proyecto creado: {project.name} (ID: {project.id})")
        
        # Actualizar el proyecto
        success, msg = self.project_manager.update_project(
            project.id, 
            status="in_progress",
            client="CLI001",
            budget=1500.0
        )
        print(f"✓ Proyecto actualizado: {msg}")
        
        # Registrar análisis
        self.analytics.track_feature_usage("gestion_proyectos")
        
        print()
    
    def _demo_clients(self):
        """Demostración de gestión de clientes"""
        print("--- Gestión de Clientes ---")
        
        # Crear un cliente
        client, msg = self.client_manager.create_client(
            name="Empresa XYZ",
            email="contacto@empresa-xyz.com",
            phone="+1234567890"
        )
        
        if client:
            print(f"✓ Cliente creado: {client.name} (ID: {client.id})")
            
            # Actualizar información del cliente
            success, msg = self.client_manager.update_client(
                client.id,
                company="Empresa XYZ S.A.",
                address="Av. Principal 123, Ciudad",
                preferred_filament="PLA"
            )
            print(f"✓ Cliente actualizado: {msg}")
            
            # Registrar análisis
            self.analytics.track_feature_usage("gestion_clientes")
        
        print()
    
    def _demo_materials(self):
        """Demostración de gestión de materiales"""
        print("--- Gestión de Materiales ---")
        
        # Añadir un material
        material, msg = self.material_manager.add_material(
            name="PLA Premium",
            material_type="PLA",
            price_per_kg=25.0
        )
        
        if material:
            print(f"✓ Material añadido: {material.name} (ID: {material.id})")
            
            # Actualizar stock
            success, msg = self.material_manager.update_stock(material.id, 10.5)
            print(f"✓ Stock actualizado: {msg}")
            
            # Registrar análisis
            self.analytics.track_feature_usage("gestion_materiales")
        
        print()
    
    def _demo_printers(self):
        """Demostración de gestión de impresoras"""
        print("--- Gestión de Impresoras ---")
        
        # Añadir una impresora
        printer, msg = self.printer_manager.add_printer(
            name="Impresora 3D Pro",
            model="Model X200",
            manufacturer="PrintTech"
        )
        
        if printer:
            print(f"✓ Impresora añadida: {printer.name} (ID: {printer.id})")
            
            # Actualizar horas de uso
            success, msg = self.printer_manager.update_print_hours(printer.id, 120.5)
            print(f"✓ Horas de uso actualizadas: {msg}")
            
            # Registrar análisis
            self.analytics.track_feature_usage("gestion_impresoras")
        
        print()
    
    def _demo_tasks(self):
        """Demostración de gestión de tareas"""
        print("--- Gestión de Tareas ---")
        
        # Crear una tarea
        task = self.task_manager.create_task(
            title="Preparar cotización para proyecto XYZ",
            description="Crear cotización detallada para 50 piezas personalizadas"
        )
        
        if task:
            print(f"✓ Tarea creada: {task.title} (ID: {task.id})")
            
            # Asignar etiquetas
            success, msg = self.task_manager.add_task_tag(task.id, "cotización")
            success, msg = self.task_manager.add_task_tag(task.id, "urgente")
            print(f"✓ Etiquetas añadidas")
            
            # Actualizar estado y prioridad
            success, msg = self.task_manager.update_task(task.id, status="in_progress", priority="high")
            print(f"✓ Tarea actualizada: {msg}")
            
            # Registrar análisis
            self.analytics.track_feature_usage("gestion_tareas")
        
        print()
    
    def _demo_budgets(self):
        """Demostración de gestión de presupuestos"""
        print("--- Gestión de Presupuestos ---")
        
        # Crear un presupuesto
        budget = self.budget_manager.create_budget(
            name="Presupuesto Mensual Impresión",
            period="monthly",
            amount=5000.0
        )
        
        if budget:
            print(f"✓ Presupuesto creado: {budget.name} (ID: {budget.id})")
            
            # Añadir una transacción
            transaction = self.budget_manager.add_transaction(
                amount=1200.0,
                description="Compra de filamento PLA",
                budget_id=budget.id,
                category="materiales"
            )
            
            if transaction:
                print(f"✓ Transacción añadida: {transaction.description} (${transaction.amount})")
            
            # Reservar fondos
            success, msg = self.budget_manager.reserve_amount(budget.id, 800.0, "Mantenimiento de impresoras")
            print(f"✓ Fondos reservados: {msg}")
            
            # Registrar análisis
            self.analytics.track_feature_usage("gestion_presupuestos")
        
        print()
    
    def _demo_analytics(self):
        """Demostración de análisis"""
        print("--- Análisis y Métricas ---")
        
        # Registrar eventos adicionales
        self.analytics.track_app_start()
        self.analytics.track_calculation()
        self.analytics.track_quote_saved()
        
        # Obtener resumen
        summary = self.analytics.get_analytics_summary()
        print("✓ Resumen de análisis:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        print()
    
    def get_system_statistics(self):
        """Obtiene estadísticas generales del sistema"""
        stats = {
            "proyectos_activos": self.project_manager.get_active_projects_count(),
            "clientes_registrados": len(self.client_manager.get_clients()),
            "materiales_disponibles": len(self.material_manager.get_materials()),
            "impresoras_activas": self.printer_manager.get_active_printers_count(),
            "tareas_pendientes": len(self.task_manager.get_tasks(status="pending")),
            "presupuestos_activos": len(self.budget_manager.get_budgets(status="active")),
            "analisis_registrados": self.analytics.get_analytics_summary()
        }
        
        return stats
    
    def print_system_statistics(self):
        """Imprime estadísticas del sistema"""
        stats = self.get_system_statistics()
        
        print("\n=== ESTADÍSTICAS DEL SISTEMA ===")
        print(f"Proyectos activos: {stats['proyectos_activos']}")
        print(f"Clientes registrados: {stats['clientes_registrados']}")
        print(f"Materiales disponibles: {stats['materiales_disponibles']}")
        print(f"Impresoras activas: {stats['impresoras_activas']}")
        print(f"Tareas pendientes: {stats['tareas_pendientes']}")
        print(f"Presupuestos activos: {stats['presupuestos_activos']}")
        print("\nAnálisis registrados:")
        for key, value in stats['analisis_registrados'].items():
            print(f"  {key}: {value}")
        print("===============================\n")


def main():
    """Función principal de la aplicación"""
    print("SISTEMA DE GESTIÓN 3D PRO")
    print("=" * 50)
    
    try:
        # Crear instancia del sistema
        sistema = Gestion3DPro()
        
        # Ejecutar demostración
        sistema.run_demo()
        
        # Mostrar estadísticas del sistema
        sistema.print_system_statistics()
        
        print("¡Sistema ejecutado exitosamente!")
        
    except Exception as e:
        print(f"Error al ejecutar el sistema: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
