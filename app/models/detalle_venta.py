from app import db

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id_detalle": self.id_detalle,
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "subtotal": self.subtotal
        }