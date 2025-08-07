# 3D Pro - Sistema de Gestión para Impresión 3D

Sistema integral de gestión para empresas dedicadas a la impresión 3D, que incluye herramientas avanzadas para el manejo de proyectos, clientes, materiales, impresoras, tareas y presupuestos.

## Características Principales

- 📁 **Gestión de Proyectos**: Control completo de proyectos de impresión 3D
- 👥 **Gestión de Clientes**: Registro detallado de clientes y seguimiento de relaciones
- 🧱 **Gestión de Materiales**: Inventario y control de materiales de impresión
- 🖨️ **Gestión de Impresoras**: Catálogo y seguimiento de impresoras 3D
- 📋 **Gestión de Tareas**: Sistema de tareas y recordatorios
- 💰 **Gestión de Presupuestos**: Control financiero y planificación presupuestaria
- 📊 **Análisis y Métricas**: Seguimiento de uso y estadísticas del sistema

## Módulos del Sistema

### Gestión de Proyectos (`project_manager.py`)
- Creación, actualización y eliminación de proyectos
- Asociación de cotizaciones a proyectos
- Gestión de presupuestos y fechas límite
- Estados de proyecto y seguimiento de notas

### Gestión de Clientes (`client_manager.py`)
- Registro completo de información de clientes
- Historial de gastos y descuentos personalizados
- Preferencias de materiales y seguimiento de contactos
- Exportación a CSV

### Gestión de Materiales (`material_manager.py`)
- Inventario detallado de materiales
- Control de precios y stock
- Alertas de stock bajo
- Cálculo de costos de materiales

### Gestión de Impresoras (`printer_manager.py`)
- Catálogo de impresoras 3D
- Horas de uso y consumo eléctrico
- Programación de mantenimiento
- Costos de operación

### Gestión de Tareas (`task_manager.py`)
- Sistema de tareas y recordatorios
- Prioridades y estados de tareas
- Fechas límite y asignaciones
- Etiquetas y categorización

### Gestión de Presupuestos (`budget_manager.py`)
- Planificación financiera por períodos
- Seguimiento de gastos y reservas
- Límites y alertas presupuestarias
- Reportes financieros

### Análisis y Métricas (`analytics.py`)
- Seguimiento de uso de la aplicación
- Métricas de rendimiento
- Análisis de características más utilizadas
- Resúmenes estadísticos

## Requisitos del Sistema

- Python 3.6 o superior
- Módulos estándar de Python (json, os, datetime, typing)

## Instalación

1. Clonar el repositorio o descargar los archivos
2. Asegurarse de tener Python 3.6+ instalado
3. No se requieren dependencias externas adicionales

## Uso

Los módulos pueden ser importados individualmente según las necesidades:

```python
from utils.project_manager import ProjectManager
from utils.client_manager import ClientManager
from utils.material_manager import MaterialManager
from utils.printer_manager import PrinterManager
from utils.task_manager import TaskManager
from utils.budget_manager import BudgetManager
from utils.analytics import Analytics

# Ejemplo de uso
pm = ProjectManager()
client_manager = ClientManager()
material_manager = MaterialManager()
```

## Documentación

Para más detalles sobre cada módulo, consulte los archivos individuales en el directorio `utils/`.

## Pruebas

Se incluye un conjunto de pruebas básicas para verificar la importación correcta de los módulos:

```bash
python tests/test_modules.py
```

## Licencia

Este proyecto es parte de la Calculadora 3D Pro y está destinado para uso interno.

## Desarrollado por

Sistema de Gestión 3D Pro - Soluciones integrales para impresión 3D
