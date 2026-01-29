import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader

# FIX 1: instance_path='/tmp' evita el error de "Read-only file system"
app = Flask(__name__, instance_path='/tmp')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'brisa_milagro_key_2025')

# FIX 2: Configuración de Base de Datos optimizada para Vercel + Supabase
uri = os.environ.get('DATABASE_URL')
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # Supabase requiere SSL en la mayoría de conexiones externas
    if "?" not in uri:
        uri += "?sslmode=require"
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# CONFIGURACIÓN DE CLOUDINARY
cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

# --- MODELOS DE BASE DE DATOS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class FotoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)

class FechaBloqueada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10), unique=True, nullable=False) # YYYY-MM-DD

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DATOS DE LA CASA (Tu lógica original intacta)
CASA_INFO = {
    "nombre": "Brisa el Milagro",
    "ubicacion": "Balneario El Milagro, Pacasmayo",
    "descripcion": "Un refugio exclusivo frente al mar donde el diseño moderno se encuentra con la naturaleza. Ideal para desconectar y recargar energías.",
    "precio": "Consultar Vía WhatsApp",
    "whatsapp": "51989653311", 
    "mapa_link": "https://www.google.com/maps/dir/Plaza+de+Armas+de+Pacasmayo,+Calle+Manco+C%C3%A1pac,+Pacasmayo/-7.4553359,-79.5764157/@-7.4553192,-79.5764818,87m/data=!3m1!1e3!4m9!4m8!1m5!1m1!1s0x904d46080fc459e5:0xfb2f4f890f3a7d06!2m2!1d-79.5722674!2d-7.40112!1m0!3e0?entry=ttu&g_ep=EgoyMDI2MDEwNy4wIKXMDSoASAFQAw%3D%3D",
    "instagram": "https://www.instagram.com/casa.brisaelmilagro/",
    "facebook": "https://www.facebook.com/people/Casa-de-playa-Brisa-El-Milagro/61586554494381/"
}

SERVICIOS = [
    {"icono": "fa-utensils", "nombre": "Área de Comedor"},
    {"icono": "fa-music", "nombre": "Área de Baile"},
    {"icono": "fa-water", "nombre": "Piscina Privada"},
    {"icono": "fa-fire", "nombre": "Zona de Parrilla"},
    {"icono": "fa-tree", "nombre": "Áreas Verdes"},
    {"icono": "fa-bed", "nombre": "1 Habitación"},
    {"icono": "fa-bath", "nombre": "3 Baños"},
    {"icono": "fa-car", "nombre": "Estacionamiento Seguro"},
    {"icono": "fa-users", "nombre": "Capacidad 50 Personas"},
]

TESTIMONIOS = [
    {"nombre": "Carlos R.", "comentario": "La vista es impagable. La casa estaba impecable y la atención fue de primera."},
    {"nombre": "Ana M.", "comentario": "El mejor fin de semana en años. La piscina es tal cual las fotos."},
    {"nombre": "Grupo Familia Pérez", "comentario": "Excelente para ir con niños, muy seguro y cómodo."}
]

FAQS = [
    {"pregunta": "¿Se permiten mascotas?", "respuesta": "Sí, somos Pet Friendly. Solo pedimos cuidar la limpieza."},
    {"pregunta": "¿Cuál es la hora de Check-in y Check-out?", "respuesta": "Check-in: 12:00 PM | Check-out: 12:00 PM."},
    {"pregunta": "¿Hay agua caliente e internet?", "respuesta": "Actualmente no contamos con Wi-Fi y la terma estará disponible próximamente."},
    {"pregunta": "¿Piden garantía?", "respuesta": "Sí, se solicita una garantía de 200 soles que se devuelve al finalizar la estadía."},
    {"pregunta": "¿Cómo reservo?", "respuesta": "Con el 50% de adelanto vía transferencia o Yape/Plin."}
]

# --- NUEVA RUTA SITEMAP PARA GOOGLE ---
@app.route('/sitemap.xml')
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://casaplayabrisamilagro-w97l.vercel.app/</loc>
            <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>"""
    return Response(xml, mimetype='application/xml')
    
@app.route('/')
def home():
    # 1. Galería estática: Obtenemos SOLO los nombres de archivos (como foto1.jpg)
    carpeta_img = os.path.join(app.root_path, 'static', 'img')
    galeria_estatica = []
    if os.path.exists(carpeta_img):
        archivos = os.listdir(carpeta_img)
        ext_validas = ('.jpg', '.jpeg', '.png', '.webp')
        # Guardamos solo el nombre para que tu url_for del HTML funcione
        galeria_estatica = [img for img in archivos if img.lower().endswith(ext_validas)]
    
    # 2. Galería dinámica (DB/Cloudinary)
    fotos_db = FotoExtra.query.all()
    galeria_dinamica = [f.url for f in fotos_db]
    
    # 3. Fechas bloqueadas
    bloqueadas = [b.fecha for b in FechaBloqueada.query.all()]
    
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS,
                           faqs=FAQS,
                           galeria=galeria_estatica,   # Nombres de archivos locales
                           fotos_extra=galeria_dinamica, # URLs de Cloudinary
                           bloqueadas=bloqueadas,
                           ws_link=ws_link,
                           anio=datetime.now().year)

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('admin_panel'))
        flash('Credenciales incorrectas')
    
    # IMPORTANTE: Debemos pasar info=CASA_INFO para que el HTML no de error
    return render_template('login.html', info=CASA_INFO)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_panel():
    fotos = FotoExtra.query.all()
    fechas = FechaBloqueada.query.all()
    return render_template('admin.html', fotos=fotos, fechas=fechas)

@app.route('/admin/subir', methods=['POST'])
@login_required
def subir_foto():
    file = request.files['archivo']
    if file:
        # Subir a Cloudinary
        res = cloudinary.uploader.upload(file)
        nueva_foto = FotoExtra(url=res['secure_url'])
        db.session.add(nueva_foto)
        db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/eliminar-foto/<int:id>')
@login_required
def eliminar_foto(id):
    foto = FotoExtra.query.get(id)
    if foto:
        db.session.delete(foto)
        db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/bloquear', methods=['POST'])
@login_required
def bloquear_fecha():
    fecha = request.form.get('fecha')
    if fecha:
        existe = FechaBloqueada.query.filter_by(fecha=fecha).first()
        if not existe:
            nueva = FechaBloqueada(fecha=fecha)
            db.session.add(nueva)
            db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/desbloquear/<int:id>')
@login_required
def desbloquear_fecha(id):
    fecha = FechaBloqueada.query.get(id)
    if fecha:
        db.session.delete(fecha)
        db.session.commit()
    return redirect(url_for('admin_panel'))

# FIX 3: Inicialización segura para que no crashee si la DB tarda en responder
with app.app_context():
    try:
        db.create_all()
        # Crear admin original
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password=generate_password_hash('Brisa2025')))
            db.session.commit()
            
        # NUEVO: Crear usuario BrunoTapia
        if not User.query.filter_by(username='BrunoTapia').first():
            bruno_user = User(username='BrunoTapia', password=generate_password_hash('Tapia123*'))
            db.session.add(bruno_user)
            db.session.commit()
            print("Usuario BrunoTapia creado con éxito")
            
    except Exception as e:
        print(f"Error: {e}")
