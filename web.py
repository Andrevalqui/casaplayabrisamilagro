import os
from datetime import datetime # <--- 1. IMPORTANTE: Agregamos esta línea arriba
from flask import Flask, render_template

app = Flask(__name__)

# DATOS DE LA CASA
CASA_INFO = {
    "nombre": "Brisa Milagro",
    "ubicacion": "Balneario El Milagro, Pacasmayo",
    "descripcion": "Un refugio exclusivo frente al mar...", # Tu descripción larga aquí
    "precio": "Consultar Vía WhatsApp",
    "whatsapp": "987654321",
    "mapa_link": "https://www.google.com/maps/dir/..." # Tu link largo aquí
}

SERVICIOS = [
    # ... (Tus servicios igual que antes) ...
    {"icono": "fa-wifi", "nombre": "WiFi Alta Velocidad"},
    {"icono": "fa-water", "nombre": "Piscina Privada"},
    {"icono": "fa-snowflake", "nombre": "Aire Acondicionado"},
    {"icono": "fa-car", "nombre": "Estacionamiento Seguro"},
    {"icono": "fa-utensils", "nombre": "Zona de Parrilla"},
    {"icono": "fa-users", "nombre": "Capacidad 10 Personas"},
]

TESTIMONIOS = [
    # ... (Tus testimonios igual que antes) ...
    {"nombre": "Carlos R.", "comentario": "La vista es impagable..."},
    {"nombre": "Ana M.", "comentario": "El mejor fin de semana..."},
    {"nombre": "Grupo Familia Pérez", "comentario": "Excelente para ir con niños..."}
]

@app.route('/')
def home():
    # --- LOGICA IMAGENES ---
    carpeta_img = os.path.join(app.root_path, 'static', 'img')
    archivos = os.listdir(carpeta_img)
    ext_validas = ('.jpg', '.jpeg', '.png', '.webp')
    galeria = [img for img in archivos if img.lower().endswith(ext_validas)]
    
    # --- LOGICA WHATSAPP ---
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    # --- LOGICA AÑO AUTOMATICO ---
    anio_actual = datetime.now().year # <--- 2. Python calcula el año aquí
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS, 
                           galeria=galeria,
                           ws_link=ws_link,
                           anio=anio_actual) # <--- 3. Se lo enviamos al HTML

if __name__ == '__main__':
    app.run()
