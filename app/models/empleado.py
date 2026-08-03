from app import db

class Empleados(db.Model):
    __tablename__ = "empleados"
    
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    salario = db.Column(db.Float, nullable=False)
    
    ventas = db.relationship('Venta', backref='empleado', lazy=True)

    def to_dict(self):
        return {
            "id_empleado": self.id_empleado,
            "nombres": self.nombres,
            "cargo": self.cargo,
            "telefono": self.telefono,
            "correo": self.correo,
            "salario": self.salario
        }