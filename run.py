from app import create_app, db

# Importamos todos los nuevos modelos para que SQLAlchemy sepa que existen
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.cliente import Cliente
from app.models.empleado import Empleados
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

app = create_app()

with app.app_context():
    db.create_all() # ¡Esto generará las 7 tablas de tu diagrama automáticamente en Laragon!

if __name__ == "__main__":
    app.run(debug=True)