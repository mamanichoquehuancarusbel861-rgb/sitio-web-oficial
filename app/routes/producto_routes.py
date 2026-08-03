from flask import Blueprint, request, jsonify
from app import db
from app.models.producto import Producto

producto_bp = Blueprint('producto_bp', __name__)

# 1. CREAR PRODUCTO (POST)
@producto_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    
    # Validar que el código no se repita
    existe = Producto.query.filter_by(codigo=data['codigo']).first()
    if existe:
        return jsonify({"mensaje": "El código de producto ya existe"}), 400
        
    nuevo_producto = Producto(
        codigo=data['codigo'],
        nombre=data['nombre'],
        marca=data['marca'],
        precio_compra=data['precio_compra'],
        precio_venta=data['precio_venta'],
        stock=data['stock'],
        id_categoria=data['id_categoria'],
        id_proveedor=data['id_proveedor']
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto registrado con éxito", "producto": nuevo_producto.to_dict()}), 201
    
# 2. OBTENER TODOS LOS PRODUCTOS (GET)
@producto_bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos]), 200

# 3. OBTENER UN PRODUCTO POR ID (GET)
@producto_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict()), 200

# 4. ACTUALIZAR PRODUCTO (PUT)
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()
    
    producto.codigo = data.get('codigo', producto.codigo)
    producto.nombre = data.get('nombre', producto.nombre)
    producto.marca = data.get('marca', producto.marca)
    producto.precio_compra = data.get('precio_compra', producto.precio_compra)
    producto.precio_venta = data.get('precio_venta', producto.precio_venta)
    producto.stock = data.get('stock', producto.stock)
    producto.id_categoria = data.get('id_categoria', producto.id_categoria)
    producto.id_proveedor = data.get('id_proveedor', producto.id_proveedor)
    
    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado con éxito", "producto": producto.to_dict()}), 200

# 5. ELIMINAR PRODUCTO (DELETE)
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200