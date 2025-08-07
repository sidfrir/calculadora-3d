"""
Configuración del Sistema 3D Pro

Este archivo contiene la configuración global del sistema de gestión 3D Pro.
"""

import os

# Configuración de archivos de datos
DATA_DIR = "data"
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
MATERIALS_FILE = os.path.join(DATA_DIR, "materials.json")
PRINTERS_FILE = os.path.join(DATA_DIR, "printers.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
ANALYTICS_FILE = os.path.join(DATA_DIR, "analytics.json")

# Configuración de directorios
EXPORTS_DIR = "exports"
IMPORTS_DIR = "imports"
BACKUPS_DIR = "backups"

# Crear directorios si no existen
for directory in [DATA_DIR, EXPORTS_DIR, IMPORTS_DIR, BACKUPS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Configuración de la aplicación
APP_NAME = "3D Pro - Sistema de Gestión para Impresión 3D"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Equipo de Desarrollo 3D Pro"

# Configuración de la base de datos
DATABASE_URL = "sqlite:///3dpro.db"

# Configuración de seguridad
SECRET_KEY = "3dpro_secret_key_2023"

# Configuración de archivos de registro
LOG_FILE = os.path.join(DATA_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(DATA_DIR, "error.log")

# Configuración de exportación
DEFAULT_EXPORT_FORMAT = "csv"

# Configuración de moneda
DEFAULT_CURRENCY = "USD"
CURRENCY_SYMBOL = "$"

# Configuración de alertas
LOW_STOCK_THRESHOLD = 5.0  # kg
BUDGET_ALERT_THRESHOLD = 0.8  # 80%

# Configuración de mantenimiento
DEFAULT_MAINTENANCE_HOURS = 100  # horas

# Configuración de electricidad
DEFAULT_ELECTRICITY_PRICE = 0.15  # $/kWh

# Configuración de impresión
DEFAULT_NOZZLE_DIAMETER = 0.4  # mm
DEFAULT_LAYER_HEIGHT = 0.2  # mm

# Configuración de análisis
ANALYTICS_ENABLED = True

# Configuración de interfaz
THEME = "light"
LANGUAGE = "es"  # español

# Configuración de copias de seguridad
AUTO_BACKUP_ENABLED = True
BACKUP_INTERVAL_DAYS = 7

# Configuración de notificaciones
NOTIFICATIONS_ENABLED = True

# Configuración de tareas
DEFAULT_TASK_PRIORITY = "medium"
DEFAULT_TASK_STATUS = "pending"

# Configuración de proyectos
DEFAULT_PROJECT_STATUS = "active"

# Configuración de clientes
DEFAULT_CLIENT_STATUS = "active"

# Configuración de materiales
DEFAULT_MATERIAL_STATUS = "active"

# Configuración de impresoras
DEFAULT_PRINTER_STATUS = "active"

# Configuración de presupuestos
DEFAULT_BUDGET_PERIOD = "monthly"
DEFAULT_BUDGET_CATEGORY = "general"
DEFAULT_BUDGET_STATUS = "active"

# Configuración de autenticación
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT_MINUTES = 30

# Configuración de red
API_TIMEOUT_SECONDS = 30

# Configuración de impresión 3D
DEFAULT_PRINT_TECHNOLOGY = "FDM"

# Configuración de exportación de datos
EXPORT_COMPRESSION = True

# Configuración de importación de datos
IMPORT_OVERWRITE = False

# Configuración de registro
LOG_LEVEL = "INFO"
LOG_MAX_SIZE_MB = 10
LOG_BACKUP_COUNT = 5

# Configuración de rendimiento
MAX_RECORDS_PER_PAGE = 100
CACHE_ENABLED = True
CACHE_TIMEOUT_SECONDS = 300

# Configuración de internacionalización
SUPPORTED_LANGUAGES = ["es", "en"]
DEFAULT_TIMEZONE = "America/New_York"

# Configuración de validación
VALIDATION_STRICT_MODE = False

# Configuración de depuración
DEBUG_MODE = False

# Configuración de prueba
TEST_MODE = False

# Configuración de desarrollo
DEVELOPMENT_MODE = False

# Configuración de producción
PRODUCTION_MODE = True

# Configuración de características
FEATURE_PROJECT_MANAGEMENT = True
FEATURE_CLIENT_MANAGEMENT = True
FEATURE_MATERIAL_MANAGEMENT = True
FEATURE_PRINTER_MANAGEMENT = True
FEATURE_TASK_MANAGEMENT = True
FEATURE_BUDGET_MANAGEMENT = True
FEATURE_ANALYTICS = True
FEATURE_REPORTING = True
FEATURE_EXPORT_IMPORT = True
FEATURE_NOTIFICATIONS = True
FEATURE_BACKUP_RESTORE = True
FEATURE_USER_MANAGEMENT = True
FEATURE_SETTINGS = True
FEATURE_HELP = True

# Configuración de integración
INTEGRATION_API_ENABLED = False
INTEGRATION_API_KEY = ""

# Configuración de actualización
AUTO_UPDATE_CHECK = True
UPDATE_CHECK_INTERVAL_DAYS = 1

# Configuración de almacenamiento
STORAGE_LIMIT_GB = 10

# Configuración de seguridad de datos
DATA_ENCRYPTION_ENABLED = False

# Configuración de privacidad
PRIVACY_MODE = False

# Configuración de cumplimiento
COMPLIANCE_MODE = False

# Configuración de accesibilidad
ACCESSIBILITY_MODE = False

# Configuración de personalización
CUSTOMIZATION_ENABLED = True

# Configuración de temas
THEMES_ENABLED = True

# Configuración de extensiones
EXTENSIONS_ENABLED = False

# Configuración de plugins
PLUGINS_ENABLED = False

# Configuración de módulos
MODULES_ENABLED = True

# Configuración de componentes
COMPONENTS_ENABLED = True

# Configuración de servicios
SERVICES_ENABLED = True

# Configuración de herramientas
TOOLS_ENABLED = True

# Configuración de utilidades
UTILITIES_ENABLED = True

# Configuración de características experimentales
EXPERIMENTAL_FEATURES = False

# Configuración de características beta
BETA_FEATURES = False

# Configuración de características avanzadas
ADVANCED_FEATURES = False

# Configuración de características profesionales
PROFESSIONAL_FEATURES = False

# Configuración de características empresariales
ENTERPRISE_FEATURES = False

# Configuración de características educativas
EDUCATIONAL_FEATURES = False

# Configuración de características de demostración
DEMO_FEATURES = False

# Configuración de características de prueba
TRIAL_FEATURES = False

# Configuración de características limitadas
LIMITED_FEATURES = False

# Configuración de características gratuitas
FREE_FEATURES = True

# Configuración de características premium
PREMIUM_FEATURES = False

# Configuración de características de suscripción
SUBSCRIPTION_FEATURES = False

# Configuración de características de pago
PAID_FEATURES = False

# Configuración de características de compra
PURCHASE_FEATURES = False

# Configuración de características de alquiler
RENTAL_FEATURES = False

# Configuración de características de licencia
LICENSED_FEATURES = False

# Configuración de características de suscripción mensual
MONTHLY_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción anual
ANNUAL_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción vitalicia
LIFETIME_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción gratuita
FREE_SUBSCRIPTION_FEATURES = True

# Configuración de características de suscripción de prueba
TRIAL_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción limitada
LIMITED_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción ilimitada
UNLIMITED_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción básica
BASIC_SUBSCRIPTION_FEATURES = True

# Configuración de características de suscripción estándar
STANDARD_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción premium
PREMIUM_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción empresarial
ENTERPRISE_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción educativa
EDUCATIONAL_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción de demostración
DEMO_SUBSCRIPTION_FEATURES = False

# Configuración de características de suscripción de prueba
TEST_SUBSCRIPTION_FEATURES = False
