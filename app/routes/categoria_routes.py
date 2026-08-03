from flask import Blueprint, request, jsonify
from app import db
from app.models.categoria import Categoria
from sqlalchemy.exc import IntegrityError  # <--- IMPORTANTE: Importar el detector de errores de base de datos

categoria_bp = Blueprint('categoria_bp', __name__)

# 1. CREAR CATEGORÍA (POST)
@categoria_bp.route('/categorias', methods=['POST'])
def crear_categoria():
    data = request.get_json()
    nueva = Categoria(
        nombre=data['nombre'], 
        descripcion=data.get('descripcion', '')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Categoría creada con éxito", "categoria": nueva.to_dict()}), 201

# 2. OBTENER TODAS LAS CATEGORÍAS (GET)
@categoria_bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias]), 200

# 3. OBTENER UNA CATEGORÍA POR ID (GET)
@categoria_bp.route('/categorias/<int:id>', methods=['GET'])
def obtener_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return jsonify(categoria.to_dict()), 200

# 4. ACTUALIZAR CATEGORÍA (PUT)
@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.get_json()
    
    categoria.nombre = data.get('nombre', categoria.nombre)
    categoria.descripcion = data.get('descripcion', categoria.descripcion)
    
    db.session.commit()
    return jsonify({"mensaje": "Categoría actualizada con éxito", "categoria": categoria.to_dict()}), 200

# 5. ELIMINAR CATEGORÍA (DELETE) - ¡CORREGIDO Y SEGURO!
@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    # .get_or_404 buscará la categoría. Si no existe en la base de datos, Postman te responderá un claro "404 Not Found".
    categoria = Categoria.query.get_or_404(id)
    
    try:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({"mensaje": "Categoría eliminada correctamente"}), 200
    except IntegrityError:
        # Si MySQL impide borrar la categoría por tener productos enlazados, capturamos el error
        db.session.rollback()  # Deshace la transacción trabada
        return jsonify({
            "error": "No se puede eliminar la categoría porque hay productos registrados con ella. Primero cambia de categoría o elimina esos productos."
        }), 400