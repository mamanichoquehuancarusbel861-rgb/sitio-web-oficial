from flask import Blueprint, request, jsonify
from app import db
from app.models.venta import Venta

venta_bp = Blueprint('venta_bp', __name__)

# 1. CREAR VENTA (POST)
@venta_bp.route('/ventas', methods=['POST'])
def crear_venta():
    data = request.get_json()
    
    nueva_venta = Venta(
        id_cliente=data['id_cliente'],
        id_empleado=data['id_empleado'],
        total=data.get('total', 0.0) # Se inicializa en 0 o con el valor enviado
    )
    db.session.add(nueva_venta)
    db.session.commit()
    return jsonify({"mensaje": "Venta registrada con éxito", "venta": nueva_venta.to_dict()}), 201

# 2. OBTENER TODAS LAS VENTAS (GET)
@venta_bp.route('/ventas', methods=['GET'])
def obtener_ventas():
    ventas = Venta.query.all()
    return jsonify([v.to_dict() for v in ventas]), 200

# 3. OBTENER VENTA POR ID (GET)
@venta_bp.route('/ventas/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = Venta.query.get_or_404(id)
    return jsonify(venta.to_dict()), 200

# 4. ACTUALIZAR VENTA (PUT)
@venta_bp.route('/ventas/<int:id>', methods=['PUT'])
def actualizar_venta(id):
    venta = Venta.query.get_or_404(id)
    data = request.get_json()
    
    venta.id_cliente = data.get('id_cliente', venta.id_cliente)
    venta.id_empleado = data.get('id_empleado', venta.id_empleado)
    venta.total = data.get('total', venta.total)
    
    db.session.commit()
    return jsonify({"mensaje": "Venta actualizada correctamente", "venta": venta.to_dict()}), 200

# 5. ELIMINAR/ANULAR VENTA (DELETE)
@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"mensaje": "Venta eliminada correctamente"}), 200