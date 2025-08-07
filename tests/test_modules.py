"""
Prueba básica de importación de módulos del sistema 3D Pro
"""

import sys
import os

def test_module_import(module_name):
    """Prueba la importación de un módulo específico"""
    try:
        # Añadir el directorio utils al path
        utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils')
        if utils_path not in sys.path:
            sys.path.insert(0, utils_path)
        
        __import__(module_name)
        print(f"✓ {module_name} importado correctamente")
        return True
    except Exception as e:
        print(f"✗ Error al importar {module_name}: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 50)
    print("PRUEBAS DE IMPORTACIÓN DE MÓDULOS")
    print("=" * 50)
    
    # Lista de módulos a probar
    modules = [
        'project_manager',
        'client_manager',
        'material_manager',
        'printer_manager',
        'task_manager',
        'budget_manager',
        'analytics'
    ]
    
    passed = 0
    total = len(modules)
    
    for module in modules:
        if test_module_import(module):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTADOS: {passed}/{total} módulos importados correctamente")
    print("=" * 50)
    
    if passed == total:
        print("\n¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("\nAlgunas pruebas fallaron.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
