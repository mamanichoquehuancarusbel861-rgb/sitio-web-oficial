from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # <-- 1. IMPORTAMOS CORS
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS para que cualquier interfaz web se conecte a tu API
    CORS(app)  # <-- 2. INICIALIZAMOS CORS
    
    # Configuración de la base de datos de tu ferretería en Laragon
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    # --- REGISTRO INDEPENDIENTE DE TODOS LOS BLUEPRINTS ---
    from app.routes.producto_routes import producto_bp
    from app.routes.categoria_routes import categoria_bp
    from app.routes.proveedor_routes import proveedor_bp
    from app.routes.cliente_routes import cliente_bp
    from app.routes.empleado_routes import empleado_bp
    from app.routes.venta_routes import venta_bp
    from app.routes.detalle_venta_routes import detalle_venta_bp
    
    app.register_blueprint(producto_bp, url_prefix='/api')
    app.register_blueprint(categoria_bp, url_prefix='/api')
    app.register_blueprint(proveedor_bp, url_prefix='/api')
    app.register_blueprint(cliente_bp, url_prefix='/api')
    app.register_blueprint(empleado_bp, url_prefix='/api')
    app.register_blueprint(venta_bp, url_prefix='/api')
    app.register_blueprint(detalle_venta_bp, url_prefix='/api')
    
    @app.route("/")
    def home():
        return {"mensaje": "API de Ferretería funcionando correctamente"}
        
    return app