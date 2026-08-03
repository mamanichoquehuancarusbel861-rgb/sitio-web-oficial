from app import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = "ventas"
    
    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable=False)
    total = db.Column(db.Float, default=0.0, nullable=False)
    
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            "id_cliente": self.id_cliente,
            "id_empleado": self.id_empleado,
            "total": self.total
        }