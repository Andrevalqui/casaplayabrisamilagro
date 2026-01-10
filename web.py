from flask import Flask, render_template

app = Flask(__name__)

# DATOS DE LA CASA (Aquí editas tu info de marketing)
CASA_INFO = {
    "nombre": "Brisa Milagro",
    "ubicacion": "Balneario El Milagro, Pacasmayo",
    "descripcion": "Un refugio exclusivo frente al mar donde el diseño moderno se encuentra con la naturaleza. Ideal para desconectar y recargar energías.",
    "precio": "Consultar Vía WhatsApp",
    "whatsapp": "987654321",
    "video_id": "dQw4w9WgXcQ" # ID del video de YouTube (solo el ID)
}

# CARACTERISTICAS (Iconos usaremos FontAwesome en el HTML)
SERVICIOS = [
    {"icono": "fa-wifi", "nombre": "WiFi Alta Velocidad"},
    {"icono": "fa-water", "nombre": "Piscina Privada"},
    {"icono": "fa-snowflake", "nombre": "Aire Acondicionado"},
    {"icono": "fa-car", "nombre": "Estacionamiento Seguro"},
    {"icono": "fa-utensils", "nombre": "Zona de Parrilla"},
    {"icono": "fa-users", "nombre": "Capacidad 10 Personas"},
]

# PRUEBA SOCIAL (Tus reviews reales)
TESTIMONIOS = [
    {"nombre": "Carlos R.", "comentario": "La vista es impagable. La casa estaba impecable y la atención fue de primera."},
    {"nombre": "Ana M.", "comentario": "El mejor fin de semana en años. La piscina es tal cual las fotos."},
    {"nombre": "Grupo Familia Pérez", "comentario": "Excelente para ir con niños, muy seguro y cómodo."}
]

# LISTA DE FOTOS (Nombres de archivos en tu carpeta static/img)
GALERIA = ["foto1.jpg", "foto2.jpg", "foto3.jpg", "foto4.jpg"]

@app.route('/')
def home():
    # Creamos el link de WhatsApp con mensaje pre-rellenado
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS, 
                           galeria=GALERIA,
                           ws_link=ws_link)

if __name__ == '__main__':
    app.run()