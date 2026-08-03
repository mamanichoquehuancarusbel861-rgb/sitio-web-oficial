from app import db

class Cliente(db.Model):
    __tablename__ = "clientes"
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(150), nullable=True)
    
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "dni": self.dni,
            "telefono": self.telefono,
            "direccion": self.direccion
        }