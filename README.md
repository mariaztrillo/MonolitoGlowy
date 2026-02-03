# 🧴 Glowy - Sistema Monolítico CRUD de Skincare Coreano

## 📖 Descripción General

Aplicación web monolítica para gestionar productos de una tienda de skincare coreano. 

**Arquitectura:** Monolito tradicional con FastAPI + Jinja2 Templates

**Tecnologías:**
- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 Templates + Bootstrap 5
- **Base de datos:** MySQL con SQL directo (sin ORM)
- **Validaciones:** Pydantic

---

## 🏗️ Estructura del Proyecto

```
glowy/
├── app/
│   ├── database.py                  # SQL directo (CRUD)
│   ├── main.py                      # Rutas + Lógica
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css          # Estilos personalizados
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       └── pages/
│           ├── index.html           # Página principal (tabla)
│           ├── nuevo_producto.html  # Formulario crear
│           └── editar_producto.html # Formulario editar
├── docs/
│   └── init_db.sql                 # Script de base de datos
├── requirements.txt
├── env.back                        # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

---

## 📋 Requisitos Previos

- **Python 3.10+**
- **MySQL/MariaDB** (XAMPP, MAMP o MySQL standalone)
- **Navegador web moderno**

---

## 🚀 Instalación Paso a Paso

### 1️⃣ Descargar el proyecto
```bash
cd ~/Downloads/glowy-monolitico
```

### 2️⃣ Crear y activar entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar MySQL

Inicia MySQL:
```bash
# Si usas Homebrew (Mac):
brew services start mysql

# Si usas XAMPP/MAMP:
# Inicia los servicios desde la aplicación
```

### 5️⃣ Crear la base de datos

**Desde phpMyAdmin:**
1. Ve a http://localhost/phpmyadmin
2. Clic en "Importar"
3. Selecciona `docs/init_db.sql`
4. Clic en "Continuar"

**Desde terminal:**
```bash
mysql -u root -p < docs/init_db.sql
```

### 6️⃣ Configurar variables de entorno

Crea un archivo `.env` desde el ejemplo:
```bash
cp env.back .env
nano .env  # o: code .env
```

Edita con tus credenciales:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=glowy_db
DB_PORT=3306        # 8889 para MAMP
```

### 7️⃣ Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🌐 Acceder a la Aplicación

### Interfaz Web Principal
```
http://localhost:8000
```

Funcionalidades:
- ✅ Ver todos los productos en tabla
- ✅ Crear nuevo producto (botón "Nuevo Producto")
- ✅ Editar producto (icono lápiz)
- ✅ Eliminar producto (icono basura + confirmación)
- ✅ Notificaciones de éxito/error
- ✅ Validaciones en formularios

---

## 📱 Páginas de la Aplicación

### 1. Página Principal (`/`)
- Lista todos los productos en tabla
- Botón para crear nuevo producto
- Botones de editar y eliminar por producto
- Modal de confirmación para eliminar
- Alertas de éxito/error

### 2. Nuevo Producto (`/productos/nuevo`)
- Formulario para crear producto
- Validaciones en frontend y backend
- Redirección al inicio si éxito
- Muestra errores si validación falla

### 3. Editar Producto (`/productos/editar/{id}`)
- Formulario precargado con datos del producto
- Mismas validaciones que crear
- Botón cancelar vuelve al inicio

---

## 🔗 Endpoints de la API

| Método | Ruta                       | Descripción                    |
|--------|----------------------------|--------------------------------|
| GET    | `/`                        | Página principal (tabla)       |
| GET    | `/productos/nuevo`         | Formulario nuevo producto      |
| POST   | `/productos/nuevo`         | Guardar nuevo producto         |
| GET    | `/productos/editar/{id}`   | Formulario editar producto     |
| POST   | `/productos/editar/{id}`   | Actualizar producto            |
| DELETE | `/productos/{id}`          | Eliminar producto (AJAX)       |

---

## ✅ Validaciones Implementadas

### **Campo: nombre**
- Requerido
- Mínimo 3 caracteres
- Máximo 150 caracteres
- No puede estar vacío

### **Campo: categoria**
- Requerido
- Valores permitidos: Serum, Cleanser, Moisturizer, Toner, Sunscreen, Mask, Exfoliator, Eye Cream, Ampoule, Essence

### **Campo: precio**
- Requerido
- Mayor a 0
- Máximo 999.99€
- 2 decimales

### **Campo: stock**
- Requerido
- No negativo (mínimo 0)
- Máximo 9999 unidades

### **Campo: descripcion**
- Opcional
- Máximo 500 caracteres

---

## 🎨 Diseño

- **Framework CSS:** Bootstrap 5
- **Iconos:** Bootstrap Icons
- **Fuente:** Raleway (Google Fonts)
- **Colores:**
  - Principal: Rosa (#ff6b9d)
  - Gradientes pasteles
  - Stock bajo: Rojo
- **Responsive:** Compatible con móviles

---

## 🎯 Características Técnicas

### ✅ Cumple con los requisitos del taller:

- **Tema realista:** Tienda de skincare coreano
- **Una tabla:** `productos`
- **SQL directo:** Sin ORM, usando `mysql-connector-python`
- **CRUD completo:** Create, Read, Update, Delete
- **Validaciones Pydantic:** En todos los campos
- **Código organizado:** Separación de responsabilidades
- **Frontend:** Interfaz web completa con formularios
- **Arquitectura monolítica:** Todo en una aplicación

---

## 🔄 Flujo de Trabajo

### Crear Producto:
1. Usuario hace clic en "Nuevo Producto"
2. Rellena formulario → Submit (POST)
3. Backend valida con Pydantic
4. Si OK: Inserta en BD → Redirige a `/` con `?msg=success`
5. Si error: Vuelve al formulario con lista de errores

### Editar Producto:
1. Usuario hace clic en icono lápiz
2. Backend carga datos del producto
3. Muestra formulario precargado
4. Usuario modifica → Submit (POST)
5. Backend valida → Actualiza BD → Redirige

### Eliminar Producto:
1. Usuario hace clic en icono basura
2. JavaScript muestra modal de confirmación
3. Si confirma: Fetch DELETE a `/productos/{id}`
4. Backend elimina → Responde JSON
5. JavaScript redirige a `/` con `?msg=deleted`

---

## 📦 Arquitectura Monolítica

```
┌──────────────────────────────────────┐
│       Navegador (Usuario)            │
└────────────┬─────────────────────────┘
             │
             │ HTTP Requests
             ▼
┌──────────────────────────────────────┐
│    FastAPI (app/main.py)             │
│  ┌────────────────────────────────┐  │
│  │  Rutas + Lógica + Validaciones │  │
│  │  Renderiza Templates Jinja2    │  │
│  └───────────┬────────────────────┘  │
│              │                        │
│              ▼                        │
│  ┌──────────────────────────────┐   │
│  │   database.py                 │   │
│  │   (SQL directo)               │   │
│  └───────────┬──────────────────┘   │
└──────────────┼──────────────────────┘
               │
               ▼
      ┌────────────────┐
      │  MySQL DB      │
      │  (glowy_db)    │
      └────────────────┘
```

---

## 🐛 Solución de Problemas

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté ejecutándose
- Revisa credenciales en `.env`
- Verifica el puerto (3306 o 8889 para MAMP)

### Error: "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Table 'productos' doesn't exist"
- Ejecuta el script `docs/init_db.sql`

### La página no carga estilos
- Verifica que la carpeta `app/static` exista
- Asegúrate de ejecutar desde la raíz del proyecto

---

## 📤 Subir a GitHub

```bash
git init
git add .
git commit -m "Glowy - CRUD Monolítico de Skincare Coreano"
git remote add origin https://github.com/tu-usuario/glowy.git
git push -u origin main
```

**Nota:** El archivo `.env` NO se sube (está en `.gitignore`)

---

## 👨‍💻 Autor

**Nombre:** [Tu nombre]  
**Email:** [tu-email@example.com]  
**Asignatura:** Acceso a Datos  
**Proyecto:** CRUD Monolítico con FastAPI

---

## 📝 Licencia

Proyecto educativo para uso académico.

---

**¡Disfruta gestionando tu tienda de skincare! 🧴✨**
