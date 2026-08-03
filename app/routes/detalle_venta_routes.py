from flask import Blueprint, request, jsonify
from app import db
from app.models.detalle_venta import DetalleVenta

detalle_venta_bp = Blueprint('detalle_venta_bp', __name__)

# 1. OBTENER TODOS LOS DETALLES (GET)
@detalle_venta_bp.route('/detalle_ventas', methods=['GET'])
def obtener_detalles():
    try:
        detalles = DetalleVenta.query.all()
        return jsonify([d.to_dict() for d in detalles]), 200
    except Exception as e:
        return jsonify({"error": f"Error al leer los detalles: {str(e)}"}), 500

# 2. OBTENER UN DETALLE ESPECÍFICO POR ID (GET)
@detalle_venta_bp.route('/detalle_ventas/<int:id>', methods=['GET'])
def obtener_detalle(id):
    try:
        detalle = DetalleVenta.query.get_or_404(id)
        return jsonify(detalle.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo encontrar el detalle: {str(e)}"}), 404

# 3. CREAR DETALLE (POST)
@detalle_venta_bp.route('/detalle_ventas', methods=['POST'])
def crear_detalle():
    try:
        data = request.get_json()
        
        # Soportar 'precio' o 'precio_unitario' desde la petición
        precio = data.get('precio_unitario', data.get('precio', 0))
        cantidad = data.get('cantidad', 1)
        
        # Calcular subtotal si no viene explícito
        subtotal_calculado = data.get('subtotal', cantidad * precio)
        
        nuevo_detalle = DetalleVenta(
            id_venta=data['id_venta'],
            id_producto=data['id_producto'],
            cantidad=cantidad,
            precio=precio,
            subtotal=subtotal_calculado
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        return jsonify({"mensaje": "Detalle creado con éxito", "detalle": nuevo_detalle.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"No se pudo crear el detalle: {str(e)}"}), 400

# 4. ACTUALIZAR DETALLE (PUT)
@detalle_venta_bp.route('/detalle_ventas/<int:id>', methods=['PUT'])
def actualizar_detalle(id):
    try:
        detalle = DetalleVenta.query.get_or_404(id)
        data = request.get_json()
        
        detalle.id_venta = data.get('id_venta', detalle.id_venta)
        detalle.id_producto = data.get('id_producto', detalle.id_producto)
        detalle.cantidad = data.get('cantidad', detalle.cantidad)
        
        precio_actualizado = data.get('precio_unitario', data.get('precio', getattr(detalle, 'precio', 0)))
        if hasattr(detalle, 'precio'):
            detalle.precio = precio_actualizado
            
        detalle.subtotal = data.get('subtotal', detalle.cantidad * precio_actualizado)
        
        db.session.commit()
        return jsonify({"mensaje": "Detalle actualizado con éxito", "detalle": detalle.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"No se pudo actualizar el detalle: {str(e)}"}), 400

# 5. ELIMINAR DETALLE DE VENTA (DELETE)
@detalle_venta_bp.route('/detalle_ventas/<int:id>', methods=['DELETE'])
def eliminar_detalle(id):
    try:
        detalle = DetalleVenta.query.get_or_404(id)
        db.session.delete(detalle)
        db.session.commit()
        return jsonify({"mensaje": "Detalle de venta eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"No se pudo eliminar el detalle: {str(e)}"}), 400