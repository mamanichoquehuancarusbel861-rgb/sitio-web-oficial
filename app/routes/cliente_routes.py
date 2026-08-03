from flask import Blueprint, request, jsonify
from app import db
from app.models.cliente import Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

# 1. CREAR CLIENTE (POST)
@cliente_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    
    existe = Cliente.query.filter_by(dni=data['dni']).first()
    if existe:
        return jsonify({"mensaje": "El DNI del cliente ya existe"}), 400
        
    nuevo = Cliente(
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        dni=data['dni'],
        telefono=data.get('telefono', ''),
        direccion=data.get('direccion', '')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente registrado con éxito", "cliente": nuevo.to_dict()}), 201

# 2. OBTENER TODOS LOS CLIENTES (GET)
@cliente_bp.route('/clientes', methods=['GET'])
def obtener_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

# 3. OBTENER UN CLIENTE POR ID (GET)
@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200

# 4. ACTUALIZAR CLIENTE (PUT)
@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()
    
    cliente.nombres = data.get('nombres', cliente.nombres)
    cliente.apellidos = data.get('apellidos', cliente.apellidos)
    cliente.dni = data.get('dni', cliente.dni)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.direccion = data.get('direccion', cliente.direccion)
    
    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado con éxito", "cliente": cliente.to_dict()}), 200

# 5. ELIMINAR CLIENTE (DELETE)
@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200