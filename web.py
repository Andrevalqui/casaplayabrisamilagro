import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# DATOS DE LA CASA
CASA_INFO = {
    "nombre": "Brisa Milagro",
    "ubicacion": "Balneario El Milagro, Pacasmayo",
    "descripcion": "Un refugio exclusivo frente al mar donde el diseño moderno se encuentra con la naturaleza. Ideal para desconectar y recargar energías.",
    "precio": "Consultar Vía WhatsApp",
    "whatsapp": "987654321",
    "mapa_link": "https://www.google.com/maps/dir/Plaza+de+Armas+de+Pacasmayo,+Calle+Manco+C%C3%A1pac,+Pacasmayo/-7.4553016,-79.5761959/@-7.4238644,-79.5677181,14z/data=!4m9!4m8!1m5!1m1!1s0x904d46080fc459e5:0xfb2f4f890f3a7d06!2m2!1d-79.5722674!2d-7.40112!1m0!3e0?entry=ttu&g_ep=EgoyMDI2MDEwNy4wIKXMDSoASAFQAw%3D%3D",
    # REDES SOCIALES
    "instagram": "https://www.instagram.com/casa.brisaelmilagro/",
    "facebook": "https://www.facebook.com/people/Casa-de-playa-Brisa-El-Milagro/61586554494381/?mibextid=wwXIfr&rdid=LauYjsGBeXeunVXp&share_url=https%253A%252F%252Fwww.facebook.com%252Fshare%252F1Coy6aLzqM%252F%253Fmibextid%253DwwXIfr"
}

# --- LISTA DE SERVICIOS ---
SERVICIOS = [
    {"icono": "fa-utensils", "nombre": "Área de Comedor"},
    {"icono": "fa-music", "nombre": "Área de Baile"},
    {"icono": "fa-water", "nombre": "Piscina Privada"},
    {"icono": "fa-fire", "nombre": "Zona de Parrilla"},
    {"icono": "fa-tree", "nombre": "Áreas Verdes"},
    {"icono": "fa-bed", "nombre": "1 Habitación"},
    {"icono": "fa-bath", "nombre": "2 Baños"},
    {"icono": "fa-car", "nombre": "Estacionamiento Seguro"},
    {"icono": "fa-users", "nombre": "Capacidad 25 Personas"},
]

TESTIMONIOS = [
    {"nombre": "Carlos R.", "comentario": "La vista es impagable. La casa estaba impecable y la atención fue de primera."},
    {"nombre": "Ana M.", "comentario": "El mejor fin de semana en años. La piscina es tal cual las fotos."},
    {"nombre": "Grupo Familia Pérez", "comentario": "Excelente para ir con niños, muy seguro y cómodo."}
]

@app.route('/')
def home():
    carpeta_img = os.path.join(app.root_path, 'static', 'img')
    archivos = os.listdir(carpeta_img)
    ext_validas = ('.jpg', '.jpeg', '.png', '.webp')
    galeria = [img for img in archivos if img.lower().endswith(ext_validas)]
    
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    anio_actual = datetime.now().year
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS, 
                           galeria=galeria,
                           ws_link=ws_link,
                           anio=anio_actual)

if __name__ == '__main__':
    app.run()
