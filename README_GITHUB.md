# 📱 Calculadora 3D Pro - Android App

Aplicación móvil para cálculo de costos de impresión 3D con gestión empresarial completa.

## 🚀 Generar APK Automáticamente

### Pasos:

1. **Crea un repositorio en GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/calculadora-3d-pro.git
   git push -u origin main
   ```

2. **El APK se genera automáticamente**
   - Ve a la pestaña "Actions" en GitHub
   - Verás el workflow ejecutándose
   - En ~10 minutos tendrás tu APK

3. **Descarga el APK**
   - Ve a "Releases" en tu repositorio
   - Descarga el archivo APK
   - ¡Listo para instalar!

## 📦 Archivos Importantes

- `main_mobile.py` - Aplicación principal móvil
- `pyproject.toml` - Configuración del proyecto
- `.github/workflows/build-apk.yml` - Automatización del build

## ⚙️ Características

- ✅ Calculadora de costos completa
- ✅ Historial de cotizaciones
- ✅ Base de datos JSON local
- ✅ Configuración de moneda USD/ARS
- ✅ Interfaz optimizada para móviles

## 📲 Instalación en Android

1. Descarga el APK desde Releases
2. En tu Android, ve a Configuración > Seguridad
3. Habilita "Fuentes desconocidas"
4. Abre el archivo APK e instala
5. ¡Disfruta la app!

## 🛠️ Desarrollo Local

```bash
# Instalar dependencias
pip install flet==0.24.1

# Ejecutar app móvil
python main_mobile.py

# Generar APK (requiere Flutter)
flet build apk
```

## 📄 Licencia

MIT License - Uso libre

---
Desarrollado con ❤️ para profesionales de impresión 3D
