import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# DATOS DE LA CASA
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

@app.route('/')
def home():
    carpeta_img = os.path.join(app.root_path, 'static', 'img')
    galeria = []
    
    if os.path.exists(carpeta_img):
        archivos = os.listdir(carpeta_img)
        ext_validas = ('.jpg', '.jpeg', '.png', '.webp')
        galeria = [img for img in archivos if img.lower().endswith(ext_validas)]
    
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS,
                           faqs=FAQS,
                           galeria=galeria,
                           ws_link=ws_link,
                           anio=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)




