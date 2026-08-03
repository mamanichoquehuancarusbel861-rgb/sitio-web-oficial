from flask import Blueprint, request, jsonify
from app import db
from app.models.proveedor import Proveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

# 1. CREAR PROVEEDOR (POST)
@proveedor_bp.route('/proveedores', methods=['POST'])
def crear_proveedor():
    data = request.get_json()
    nuevo = Proveedor(
        nombre=data['nombre'],
        telefono=data.get('telefono', ''),
        direccion=data.get('direccion', ''),
        correo=data.get('correo', '')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Proveedor registrado con éxito", "proveedor": nuevo.to_dict()}), 201

# 2. OBTENER TODOS LOS PROVEEDORES (GET)
@proveedor_bp.route('/proveedores', methods=['GET'])
def obtener_proveedores():
    proveedores = Proveedor.query.all()
    return jsonify([p.to_dict() for p in proveedores]), 200

# 3. OBTENER UN PROVEEDOR POR ID (GET)
@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def obtener_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    return jsonify(proveedor.to_dict()), 200

# 4. ACTUALIZAR PROVEEDOR (PUT)
@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
def actualizar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    data = request.get_json()
    
    proveedor.nombre = data.get('nombre', proveedor.nombre)
    proveedor.telefono = data.get('telefono', proveedor.telefono)
    proveedor.direccion = data.get('direccion', proveedor.direccion)
    proveedor.correo = data.get('correo', proveedor.correo)
    
    db.session.commit()
    return jsonify({"mensaje": "Proveedor actualizado con éxito", "proveedor": proveedor.to_dict()}), 200

# 5. ELIMINAR PROVEEDOR (DELETE)
@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"mensaje": "Proveedor eliminado correctamente"}), 200