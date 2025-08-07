# 📱 Cómo Crear tu Repositorio y Obtener el APK

## Paso 1: Crear Repositorio en GitHub

1. **Abre GitHub en tu navegador:**
   - Ve a [https://github.com](https://github.com)
   - Inicia sesión con tu cuenta

2. **Crea un nuevo repositorio:**
   - Haz clic en el botón verde **"New"** o **"+"** → **"New repository"**
   - **Repository name:** `calculadora-3d`
   - **Description:** "Calculadora de costos para impresión 3D - App Android"
   - **Public** (seleccionado)
   - **NO** marques "Initialize this repository with a README"
   - Haz clic en **"Create repository"**

## Paso 2: Subir tu Código

Una vez creado el repositorio, ejecuta estos comandos en PowerShell:

```powershell
# Ya tenemos el repositorio configurado, solo push:
git push -u origin main
```

## Paso 3: El APK se Genera Automáticamente

1. Ve a tu repositorio: https://github.com/sidfrir/calculadora-3d
2. Haz clic en la pestaña **"Actions"**
3. Verás el workflow **"Build Android APK"** ejecutándose
4. Espera ~10 minutos a que termine

## Paso 4: Descargar el APK

### Opción A: Desde Actions (Rápido)
1. En la pestaña "Actions"
2. Haz clic en el workflow completado (con ✅ verde)
3. Baja a "Artifacts"
4. Descarga **"calculadora-3d-pro-apk"**

### Opción B: Desde Releases (Mejor)
1. Ve a la pestaña **"Releases"** 
2. Descarga el archivo APK
3. ¡Listo para instalar!

## 📲 Instalar en tu Android

1. Transfiere el APK a tu teléfono
2. En Configuración → Seguridad → Habilita "Fuentes desconocidas"
3. Abre el archivo APK
4. Instala y disfruta

---

## 🔗 Links Directos

- Tu repositorio: https://github.com/sidfrir/calculadora-3d
- Actions: https://github.com/sidfrir/calculadora-3d/actions
- Releases: https://github.com/sidfrir/calculadora-3d/releases

---

## ⚡ Resumen Rápido

1. Crea repo en GitHub (2 minutos)
2. Push del código (1 minuto)
3. Espera el build (10 minutos)
4. Descarga el APK
5. ¡Instala y usa!

**Total: ~15 minutos para tener tu APK**
