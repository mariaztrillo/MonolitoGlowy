from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional, List

# Importamos funciones de base de datos
from app.database import (
    fetch_all_productos,
    insert_producto,
    delete_producto,
    fetch_producto_by_id,
    update_producto
)

# --------------------------------------------------
# MODELOS Pydantic
# --------------------------------------------------

# Modelo base con validaciones comunes
class ProductoBase(BaseModel):
    nombre: str
    categoria: str
    precio: float
    stock: int
    descripcion: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        v = v.strip()
        if len(v) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        if len(v) > 150:
            raise ValueError('El nombre no puede exceder 150 caracteres')
        return v
    
    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('La categoría no puede estar vacía')
        v = v.strip()
        categorias_validas = [
            'Serum', 'Cleanser', 'Moisturizer', 
            'Toner', 'Sunscreen', 'Mask', 'Exfoliator',
            'Eye Cream', 'Ampoule', 'Essence'
        ]
        if v.title() not in categorias_validas:
            raise ValueError(f'Categoría no válida. Debe ser una de: {", ".join(categorias_validas)}')
        return v.title()
    
    @field_validator('precio')
    @classmethod
    def validar_precio(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        if v > 999.99:
            raise ValueError('El precio no puede exceder 999.99€')
        return round(v, 2)
    
    @field_validator('stock')
    @classmethod
    def validar_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        if v > 9999:
            raise ValueError('El stock no puede exceder 9999 unidades')
        return v
    
    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == '':
            return None
        v = v.strip()
        if len(v) > 500:
            raise ValueError('La descripción no puede exceder 500 caracteres')
        return v


class ProductoDB(ProductoBase):
    id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(title="Glowy – Tienda de Skincare Coreano")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")


# --------------------------------------------------
# UTILIDAD
# --------------------------------------------------
def map_rows_to_productos(rows: List[dict]) -> List[ProductoDB]:
    """
    Convierte las filas del SELECT * FROM productos (dict) 
    en objetos ProductoDB.
    """
    return [ProductoDB(**row) for row in rows]


# --------------------------------------------------
# RUTAS
# --------------------------------------------------

# --- GET principal ---
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, msg: str = None):
    # 1️⃣ Obtenemos los datos desde MySQL
    rows = fetch_all_productos()

    # 2️⃣ Convertimos cada fila a Producto
    productos = map_rows_to_productos(rows)

    # Lógica para decidir qué mensaje mostrar
    mensaje_exito = None
    if msg == "success":
        mensaje_exito = "¡Producto creado con éxito!"
    elif msg == "updated":
        mensaje_exito = "¡Producto actualizado correctamente!"
    elif msg == "deleted":
        mensaje_exito = "El producto ha sido eliminado."

    # 3️⃣ Enviamos a la plantilla
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "productos": productos,
            "mensaje_exito": mensaje_exito,
            "msg": msg
        }
    )


# --- GET formulario nuevo producto ---
@app.get("/productos/nuevo", response_class=HTMLResponse)
def get_nuevo_producto(request: Request):
    return templates.TemplateResponse(
        "pages/nuevo_producto.html",
        {"request": request}
    )


# --- POST guardar nuevo producto ---
@app.post("/productos/nuevo")
def post_nuevo_producto(
    request: Request,
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: Optional[str] = Form(None)
):
    try:
        # 1. Validamos los datos con Pydantic
        producto = ProductoCreate(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            descripcion=descripcion
        )

        # 2. Insertamos en la base de datos MySQL
        insert_producto(**producto.model_dump())
        
        # 3. ÉXITO: Redirigimos al inicio con el parámetro de éxito en la URL
        return RedirectResponse(url="/?msg=success", status_code=303)

    except ValidationError as e:
        # ERROR: Si Pydantic detecta fallos, volvemos al formulario con la lista de errores
        errores = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "pages/nuevo_producto.html",
            {
                "request": request,
                "errores": errores
            },
            status_code=422
        )


# --- DELETE eliminar producto ---
@app.delete("/productos/{producto_id}")
def delete_producto_endpoint(producto_id: int):
    if not delete_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return JSONResponse({"mensaje": "Producto eliminado"})


# --- GET formulario editar producto ---
@app.get("/productos/editar/{producto_id}", response_class=HTMLResponse)
def get_editar_producto(request: Request, producto_id: int):
    """
    Endpoint para mostrar el formulario de edición con datos precargados.
    """
    # Obtenemos los datos del producto
    data = fetch_producto_by_id(producto_id)
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Convertimos a modelo ProductoDB para mostrar en formulario
    producto = ProductoDB(**data)
    return templates.TemplateResponse(
        "pages/editar_producto.html",
        {"request": request, "producto": producto}
    )


# --- POST actualizar producto a través de su id ---
@app.post("/productos/editar/{producto_id}")
def post_editar_producto(
    request: Request,
    producto_id: int,
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: Optional[str] = Form(None)
):
    try:
        producto = ProductoUpdate(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            descripcion=descripcion
        )

        if not update_producto(producto_id, **producto.model_dump()):
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return RedirectResponse(url="/?msg=updated", status_code=303)

    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]
        producto_temp = ProductoDB(id=producto_id, **producto.model_dump())
        return templates.TemplateResponse(
            "pages/editar_producto.html",
            {
                "request": request,
                "producto": producto_temp,
                "errores": errores
            },
            status_code=422
        )
    
    except Exception as e:
        # Error crítico (Base de datos, servidor, etc.)
        print(f"Error inesperado: {e}")
        return RedirectResponse(url="/?msg=error", status_code=303)
