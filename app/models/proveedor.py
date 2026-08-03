
from app import db

class Proveedor(db.Model):
    __tablename__ = "proveedores"
    
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(150), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    
    # Relación inversa para acceder a sus productos suministrados
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

    def to_dict(self):
        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "correo": self.correo
        }