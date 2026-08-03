from flask import Blueprint, request, jsonify
from app import db
from app.models.empleado import Empleados

empleado_bp = Blueprint('empleado_bp', __name__)

# 1. CREAR EMPLEADO (POST)
@empleado_bp.route('/empleados', methods=['POST'])
def crear_empleado():
    data = request.get_json()
    nuevo = Empleados(
        nombres=data['nombres'],
        cargo=data['cargo'],
        telefono=data.get('telefono', ''),
        correo=data.get('correo', ''),
        salario=data['salario']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Empleado registrado con éxito", "empleado": nuevo.to_dict()}), 201

# 2. OBTENER TODOS LOS EMPLEADOS (GET)
@empleado_bp.route('/empleados', methods=['GET'])
def obtener_empleados():
    empleados = Empleados.query.all()
    return jsonify([e.to_dict() for e in empleados]), 200

# 3. OBTENER UN EMPLEADO POR ID (GET)
@empleado_bp.route('/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    empleado = Empleados.query.get_or_404(id)
    return jsonify(empleado.to_dict()), 200

# 4. ACTUALIZAR EMPLEADO (PUT)
@empleado_bp.route('/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    empleado = Empleados.query.get_or_404(id)
    data = request.get_json()
    
    empleado.nombres = data.get('nombres', empleado.nombres)
    empleado.cargo = data.get('cargo', empleado.cargo)
    empleado.telefono = data.get('telefono', empleado.telefono)
    empleado.correo = data.get('correo', empleado.correo)
    empleado.salario = data.get('salario', empleado.salario)
    
    db.session.commit()
    return jsonify({"mensaje": "Empleado actualizado con éxito", "empleado": empleado.to_dict()}), 200

# 5. ELIMINAR EMPLEADO (DELETE)
@empleado_bp.route('/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    empleado = Empleados.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"mensaje": "Empleado eliminado correctamente"}), 200