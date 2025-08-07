"""
Demostración del Sistema de Gestión 3D Pro

Este script muestra cómo utilizar los principales módulos del sistema.
"""

import sys
import os
from datetime import datetime, timedelta

# Añadir el directorio utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def demo_project_management():
    """Demostración del módulo de gestión de proyectos"""
    print("=== Gestión de Proyectos ===")
    
    from project_manager import ProjectManager
    
    # Crear instancia del gestor de proyectos
    pm = ProjectManager("demo_projects.json")
    
    # Crear un nuevo proyecto
    project = pm.create_project(
        name="Proyecto de Impresión Personalizada",
        description="Creación de piezas personalizadas para cliente importante"
    )
    
    print(f"Proyecto creado: {project.name} (ID: {project.id})")
    
    # Actualizar el proyecto
    success, msg = pm.update_project(
        project.id, 
        status="in_progress",
        deadline=(datetime.now() + timedelta(days=30)).isoformat(),
        client="CLI001",
        budget=1500.0
    )
    
    print(f"Proyecto actualizado: {msg}")
    
    # Asociar una cotización al proyecto
    success, msg = pm.add_quote_to_project(project.id, "QUOTE001")
    print(f"Cotización asociada: {msg}")
    
    # Obtener estadísticas
    stats = pm.get_project_statistics(project.id)
    print(f"Estadísticas del proyecto: {stats}")
    
    return project.id

def demo_client_management():
    """Demostración del módulo de gestión de clientes"""
    print("\n=== Gestión de Clientes ===")
    
    from client_manager import ClientManager
    
    # Crear instancia del gestor de clientes
    cm = ClientManager("demo_clients.json")
    
    # Crear un nuevo cliente
    client, msg = cm.create_client(
        name="Empresa XYZ",
        email="contacto@empresa-xyz.com",
        phone="+1234567890"
    )
    
    if client:
        print(f"Cliente creado: {client.name} (ID: {client.id})")
        
        # Actualizar información del cliente
        success, msg = cm.update_client(
            client.id,
            company="Empresa XYZ S.A.",
            address="Av. Principal 123, Ciudad",
            preferred_filament="PLA"
        )
        
        print(f"Cliente actualizado: {msg}")
        
        # Añadir una nota
        success, msg = cm.add_client_note(client.id, "Cliente interesado en grandes volúmenes")
        print(f"Nota añadida: {msg}")
        
        # Actualizar gasto
        cm.update_client_spending(client.id, 2500.0)
        
        # Obtener estadísticas
        stats = cm.get_client_statistics(client.id)
        print(f"Estadísticas del cliente: Gasto total: ${stats['total_spent']}")
    
    return client.id if client else None

def demo_material_management():
    """Demostración del módulo de gestión de materiales"""
    print("\n=== Gestión de Materiales ===")
    
    from material_manager import MaterialManager
    
    # Crear instancia del gestor de materiales
    mm = MaterialManager("demo_materials.json")
    
    # Añadir un nuevo material
    material, msg = mm.add_material(
        name="PLA Premium",
        material_type="PLA",
        price_per_kg=25.0
    )
    
    if material:
        print(f"Material añadido: {material.name} (ID: {material.id})")
        
        # Actualizar stock
        success, msg = mm.update_stock(material.id, 10.5)  # Agregar 10.5kg
        print(f"Stock actualizado: {msg}")
        
        # Calcular costo para 2kg (2000g)
        cost, msg = mm.calculate_material_cost(material.id, 2000.0)
        print(f"Costo para 2kg: ${cost}")
        
        # Obtener materiales con stock bajo
        low_stock = mm.get_low_stock_materials()
        print(f"Materiales con stock bajo: {len(low_stock)}")
    
    return material.id if material else None

def demo_printer_management():
    """Demostración del módulo de gestión de impresoras"""
    print("\n=== Gestión de Impresoras ===")
    
    from printer_manager import PrinterManager
    
    # Crear instancia del gestor de impresoras
    pm = PrinterManager("demo_printers.json")
    
    # Añadir una nueva impresora
    printer, msg = pm.add_printer(
        name="Impresora 3D Pro",
        model="Model X200",
        manufacturer="PrintTech"
    )
    
    if printer:
        print(f"Impresora añadida: {printer.name} (ID: {printer.id})")
        
        # Actualizar horas de uso
        success, msg = pm.update_print_hours(printer.id, 120.5)
        print(f"Horas de uso actualizadas: {msg}")
        
        # Registrar mantenimiento
        success, msg = pm.record_maintenance(printer.id)
        print(f"Mantenimiento registrado: {msg}")
        
        # Calcular costo de uso
        cost_breakdown, msg = pm.calculate_printer_cost(printer.id, 5.5, 0.15)  # 5.5 horas, $0.15/kWh
        print(f"Costo para 5.5 horas de uso: ${cost_breakdown['total_cost']}")
    
    return printer.id if printer else None

def demo_task_management():
    """Demostración del módulo de gestión de tareas"""
    print("\n=== Gestión de Tareas ===")
    
    from task_manager import TaskManager
    
    # Crear instancia del gestor de tareas
    tm = TaskManager("demo_tasks.json")
    
    # Crear una nueva tarea
    task = tm.create_task(
        title="Preparar cotización para proyecto XYZ",
        description="Crear cotización detallada para 50 piezas personalizadas"
    )
    
    if task:
        print(f"Tarea creada: {task.title} (ID: {task.id})")
        
        # Asignar etiquetas
        success, msg = tm.add_task_tag(task.id, "cotización")
        success, msg = tm.add_task_tag(task.id, "urgente")
        print(f"Etiquetas añadidas")
        
        # Actualizar estado y prioridad
        success, msg = tm.update_task(task.id, status="in_progress", priority="high")
        print(f"Tarea actualizada: {msg}")
        
        # Establecer fecha de vencimiento
        due_date = (datetime.now() + timedelta(days=3)).isoformat()
        success, msg = tm.set_due_date(task.id, due_date)
        print(f"Fecha de vencimiento establecida: {msg}")
        
        # Obtener tareas pendientes
        pending_tasks = tm.get_tasks(status="pending")
        print(f"Tareas pendientes: {len(pending_tasks)}")
    
    return task.id if task else None

def demo_budget_management():
    """Demostración del módulo de gestión de presupuestos"""
    print("\n=== Gestión de Presupuestos ===")
    
    from budget_manager import BudgetManager
    
    # Crear instancia del gestor de presupuestos
    bm = BudgetManager("demo_budgets.json", "demo_transactions.json")
    
    # Crear un nuevo presupuesto
    budget = bm.create_budget(
        name="Presupuesto Mensual Impresión",
        period="monthly",
        amount=5000.0
    )
    
    if budget:
        print(f"Presupuesto creado: {budget.name} (ID: {budget.id})")
        
        # Añadir una transacción
        transaction = bm.add_transaction(
            amount=1200.0,
            description="Compra de filamento PLA",
            budget_id=budget.id,
            category="materiales"
        )
        
        if transaction:
            print(f"Transacción añadida: {transaction.description} (${transaction.amount})")
        
        # Reservar fondos
        success, msg = bm.reserve_amount(budget.id, 800.0, "Mantenimiento de impresoras")
        print(f"Fondos reservados: {msg}")
        
        # Obtener utilización del presupuesto
        utilization = bm.get_budget_utilization(budget.id)
        print(f"Utilización del presupuesto: {utilization}%")
    
    return budget.id if budget else None

def demo_analytics():
    """Demostración del módulo de análisis"""
    print("\n=== Análisis y Métricas ===")
    
    from analytics import Analytics
    
    # Crear instancia del analizador
    analytics = Analytics("demo_analytics.json")
    
    # Registrar eventos
    analytics.track_app_start()
    analytics.track_calculation()
    analytics.track_quote_saved()
    analytics.track_feature_usage("gestion_proyectos")
    analytics.track_feature_usage("gestion_clientes")
    
    # Obtener resumen
    summary = analytics.get_analytics_summary()
    print("Resumen de análisis:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

def main():
    """Función principal de demostración"""
    print("SISTEMA DE GESTIÓN 3D PRO - DEMO")
    print("=" * 50)
    
    try:
        # Ejecutar demostraciones de cada módulo
        project_id = demo_project_management()
        client_id = demo_client_management()
        material_id = demo_material_management()
        printer_id = demo_printer_management()
        task_id = demo_task_management()
        budget_id = demo_budget_management()
        demo_analytics()
        
        print("\n" + "=" * 50)
        print("¡Demostración completada exitosamente!")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()
    
    # Limpiar archivos de demostración
    demo_files = [
        "demo_projects.json",
        "demo_clients.json",
        "demo_materials.json",
        "demo_printers.json",
        "demo_tasks.json",
        "demo_budgets.json",
        "demo_transactions.json",
        "demo_analytics.json"
    ]
    
    for filename in demo_files:
        filepath = os.path.join(os.path.dirname(__file__), 'utils', filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

if __name__ == "__main__":
    main()
