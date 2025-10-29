# 📋 Sistema de Gestión de Empleados - Ejercicio 14
## 🎯 Descripción del Proyecto
Sistema de gestión de empleados desarrollado en Python con interfaz gráfica Tkinter mejorada y base de datos MySQL. Esta aplicación implementa un CRUD completo con una interfaz visual atractiva que incluye efectos especiales, animaciones y elementos interactivos.

✨ Características Principales
## 🎨 Interfaz Gráfica Mejorada
Fondo personalizado con imagen PNG

Botones con estilo pixel art y efectos hover

Elementos transparentes sobre la imagen de fondo

Tipografía especial (Fixedsys, Consolas)

Colores diferenciados por función de botones

# ⚡ Funcionalidades Especiales
Botón "Hackear Base de Datos" - Exporta registros a CSV

Botón "Mensaje Interesante" - Muestra GIF animado "Hola Mundo"

Botón "Cerrar" escapista - Se mueve aleatoriamente al acercar el cursor

Animaciones suaves y efectos visuales

# 🗄️ Gestión de Datos
CRUD completo (Crear, Leer, Actualizar, Eliminar)

Base de datos MySQL con consultas seguras

Validación de datos en tiempo real

Bú3squeda por ID de empleados

Generación automática de IDs

# 🏗️ Estructura del Proyecto
```bash
text
sistema_empleados_mejorado/
├── 📁 assets/
│   ├── 🖼️ background.png      # Imagen de fondo
│   └── 🎬 hola_mundo.gif      # GIF animado para mensaje
├── 📄 main.py                 # Punto de entrada principal
├── 📄 gui_mejorada.py         # Interfaz gráfica mejorada
├── 📄 database.py             # Gestión de base de datos
├── 📄 empleado.py             # Modelo de datos Empleado
├── 📄 setup_database.py       # Configuración inicial de BD
└── 📄 README.md               # Este archivo
```
##📋 Prerrequisitos
###🛠️ Software Requerido
Python 3.8+

MySQL Server 8.0+

Bibliotecas Python:

bash
pip install mysql-connector-python Pillow
##⚙️ Configuración
1. Configuración de Base de Datos
bash
# Ejecutar una sola vez para crear la base de datos
python setup_database.py
2. Configurar Credenciales MySQL
En database.py, actualiza las credenciales:
```bash
python
connection_config = {
    'host': 'localhost',
    'user': 'tu_usuario',      # ← Cambiar
    'password': 'tu_password', # ← Cambiar
    'database': 'sistema_empleados'
}
```
3. Preparar Assets
Colocar background.png en carpeta assets/

Colocar hola_mundo.gif en carpeta assets/

## 🚀 Ejecución
bash
python main.py
#### 🎮 Funcionalidades Detalladas
#### 👥 Gestión de Empleados
Agregar: Nombre, Sexo (M/F/Otro), Correo electrónico

Visualizar: Lista completa en tabla interactiva

Eliminar: Por selección con confirmación

Buscar: Por ID de empleado

#### 🎪 Funciones Especiales
#### 🔍 Búsqueda Inteligente
Campo de búsqueda por ID

Resaltado automático en la lista

Validación de entrada numérica

## 🕵️ "Hackeo" de Base de Datos
Exporta todos los registros a archivo CSV

Interfaz de guardado personalizada

Formato de datos estructurado

## 💡 Mensaje Interesante
Botón que activa/desactiva GIF animado

Animación fluida de "Hola Mundo"

Fallback a texto animado si no hay GIF

## ❌ Botón Cerrar Escapista
Se mueve aleatoriamente al acercar el cursor

Dificulta el cierre intencional

Implementado con detección de movimiento del mouse

## 🗃️ Estructura de Base de Datos
Tabla: empleados
<img width="1125" height="549" alt="image" src="https://github.com/user-attachments/assets/29a980a5-df55-43e5-b363-749fc7193682" />

Consultas preparadas contra inyección SQL

Validación de datos en frontend y backend

Manejo de errores robusto

Transacciones seguras en base de datos

## 🎨 Personalización Visual
Esquema de Colores
Verde (#27AE60): Agregar empleados

Rojo (#E74C3C): Eliminar/Limpiar

Azul (#3498DB): Búsqueda

Morado (#9B59B6): Exportar datos

Amarillo (#F1C40F): Mensaje especial

Naranja (#E67E22): Botones auxiliares

Efectos Visuales
Hover effects en todos los botones

Bordes redondeados simulados

Animaciones suaves en GIF

Tipografía pixel art para estilo retro

## 🔧 Tecnologías Utilizadas
Frontend: Tkinter (Python)

Backend: Python 3.8+

Base de Datos: MySQL

Procesamiento de Imágenes: Pillow (PIL)

Manejo de Archivos: CSV, OS

## 🐛 Solución de Problemas Comunes
Error: "No such file or directory: 'assets/background.png'"
Verificar que la carpeta assets existe

Confirmar nombres de archivos: background.png y hola_mundo.gif

Error: "Cannot connect to MySQL"
Verificar credenciales en database.py

Ejecutar setup_database.py primero

Confirmar que MySQL esté ejecutándose

Error: "Unknown color name"
Eliminar parámetros bg='' vacíos

Usar bg='systemTransparent' o eliminar el parámetro

## 📝 Registro de Cambios
Versión 2.0 (Ejercicio 14)
✅ Interfaz completamente rediseñada

✅ Elementos transparentes sobre fondo

✅ Botones con efectos especiales

✅ GIF animado interactivo

✅ Botón cerrar que se mueve

✅ Exportación a CSV mejorada

Versión 1.0 (Ejercicio 13)
Funcionalidad CRUD básica

Interfaz tradicional Tkinter

Conexión a base de datos

## 🚀 Próximas Mejoras
Edición directa en la tabla

Filtros avanzados de búsqueda

Exportación a PDF/Excel

Backup automático de BD

Temas de color personalizables

##👨‍💻 Desarrollo
Este proyecto fue desarrollado como parte del Ejercicio 14 de Programación Orientada a Objetos, demostrando:

POO con clases y herencia

Modularidad en la estructura del código

Manejo de eventos y animaciones

Conexión a bases de datos segura

Interfaces gráficas avanzadas
