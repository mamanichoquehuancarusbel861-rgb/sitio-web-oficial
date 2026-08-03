from app import db

class Producto(db.Model):
    __tablename__ = "productos"
    
    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    precio_compra = db.Column(db.Float, nullable=False)  # Agregado del diagrama
    precio_venta = db.Column(db.Float, nullable=False)   # Agregado del diagrama
    stock = db.Column(db.Integer, nullable=False)
    
    # Llaves Foráneas (FK) agregadas de tu diagrama
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    
    detalles = db.relationship('DetalleVenta', backref='producto', lazy=True)

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "marca": self.marca,
            "precio_compra": self.precio_compra,
            "precio_venta": self.precio_venta,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            "id_proveedor": self.id_proveedor
        }