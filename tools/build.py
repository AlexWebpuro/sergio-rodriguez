#!/usr/bin/env python3
"""
Generador del sitio del Ing. Sergio Rodríguez.

Edita los textos y datos aquí y ejecuta:
    python3 tools/build.py
El HTML resultante queda en la raíz del repositorio (lo que publica GitHub Pages).
"""
import json
import os
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
DOMAIN = "biomedico.alexmonroy.com"          # subdominio (también va en el archivo CNAME)
SITE_URL = f"https://{DOMAIN}"
BASE = "/"                                      # ruta base de los enlaces
NAME = "Ing. Sergio Rodríguez"
ROLE = "Ingeniero Biomédico"
PHONE_DISPLAY = "301 449 7065"
PHONE_TEL = "+573014497065"
WA_NUMBER = "573014497065"
EMAIL = "sergiodavid.r46@gmail.com"
WEB3FORMS_KEY = "PON_AQUI_TU_ACCESS_KEY"        # clave de web3forms.com; mientras no exista, el formulario abre WhatsApp
GA_ID = ""                                       # opcional: ID de Google Analytics 4 (G-XXXXXXX)
TODAY = date.today().isoformat()

ZONES_MAIN = "Suba"
ZONES_BOGOTA = ["Suba", "Usaquén", "Engativá", "Barrios Unidos", "Chapinero"]
ZONES_SUBA = ["Niza", "Colina Campestre", "Mazurén", "Prado Veraniego", "Lisboa", "Tibabuyes", "Pinar de Suba", "Cerros de Suba"]
ZONES_MUNI = ["Chía", "Cota", "Cajicá"]
AREA_SERVED = ZONES_BOGOTA + ZONES_MUNI

WA_TEXT = "Hola Sergio, vi tu página web y necesito ayuda con un equipo."


def wa_link(text=WA_TEXT):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def url(path=""):
    return BASE + path


# ---------------------------------------------------------------------------
# Iconos (SVG en línea, sin dependencias)
# ---------------------------------------------------------------------------
ICONS = {
    "cpap": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="12" height="10" rx="2"/><path d="M7 12h4"/><path d="M15 12c3 0 3-6 6-6"/><circle cx="20.5" cy="6" r="1.5"/></svg>',
    "oxygen": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="16" rx="3"/><path d="M9 21h6"/><circle cx="12" cy="10" r="3"/><path d="M10 15h4"/></svg>',
    "tower": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="6" rx="1"/><rect x="5" y="9" width="14" height="5" rx="1"/><rect x="5" y="15" width="14" height="4" rx="1"/><path d="M7 22l1-3M17 22l-1-3"/></svg>',
    "scope": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h6v4H3z"/><path d="M9 7h3c4 0 4 6 0 6H8c-4 0-4 7 1 7h11"/><circle cx="20" cy="20" r="1"/></svg>',
    "bed": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7v13M21 13v7"/><path d="M3 16h18"/><path d="M3 13h18v3"/><circle cx="7" cy="10" r="2"/><path d="M11 10h8a2 2 0 0 1 2 2v1"/></svg>',
    "train": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>',
    "check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>',
    "pin": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
    "wa": '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>',
    "phone": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
}

LOGO = '<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#0d2340"/><path d="M6 21h7l3-7 5 13 3-6h10" fill="none" stroke="#2fd1b8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

PHOTOS = {
 "cpap-resmed-airsense-10-prueba-presion": "Verificación de presión de un CPAP ResMed AirSense 10 con manómetro",
 "banco-trabajo-mantenimiento-cpap": "Mantenimiento de un CPAP Philips DreamStation en el banco de trabajo",
 "turbina-cpap-philips-dreamstation": "Turbina de un CPAP Philips DreamStation durante el mantenimiento",
 "turbina-cpap-resmed-desarmada": "Turbina de un CPAP ResMed desarmada para limpieza y revisión",
 "cambio-filtro-cpap-resmed": "Cambio de filtro sucio en un CPAP ResMed",
 "humidificador-cpap-dreamstation-limpio": "Cámara del humidificador de un CPAP DreamStation después de la limpieza",
 "concentrador-oxigeno-o2-tiger-m50": "Concentrador de oxígeno O2 Tiger M50 después del mantenimiento",
 "compresor-concentrador-oxigeno": "Compresor de un concentrador de oxígeno durante la revisión",
 "filtro-entrada-concentrador-oxigeno": "Cambio del filtro de entrada de un concentrador de oxígeno",
 "concentrador-portatil-inogen-one-g4": "Concentrador de oxígeno portátil Inogen One G4 en prueba de funcionamiento",
 "interior-concentrador-portatil-inogen": "Interior de un concentrador portátil Inogen durante el mantenimiento",
 "mantenimiento-fuente-de-luz-olympus": "Mantenimiento de una fuente de luz Olympus de endoscopia en una clínica",
 "optica-fuente-de-luz-endoscopia": "Revisión de la óptica interna de una fuente de luz de endoscopia",
 "fuente-de-luz-led-endoscopia-interior": "Interior de una fuente de luz LED de endoscopia",
 "camara-endoscopia-hd-desarmada": "Cabezal de cámara de endoscopia HD desarmado para reparación",
 "vaina-endoscopio-rigido-desarmada": "Vaina de endoscopio rígido desarmada para limpieza y mantenimiento",
 "vaina-endoscopio-rigido-llaves": "Revisión de las llaves de irrigación de una vaina de endoscopio rígido",
 "vaina-endoscopio-rigido-ensamblada": "Vaina de endoscopio rígido ensamblada después del mantenimiento",
 "desfibrilador-mindray-beneheart-d3-prueba-energia": "Prueba de energía de un desfibrilador Mindray BeneHeart D3"
}

HOME_GALLERY = [
    "cpap-resmed-airsense-10-prueba-presion", "concentrador-portatil-inogen-one-g4",
    "mantenimiento-fuente-de-luz-olympus", "desfibrilador-mindray-beneheart-d3-prueba-energia",
    "turbina-cpap-philips-dreamstation", "compresor-concentrador-oxigeno",
    "camara-endoscopia-hd-desarmada", "vaina-endoscopio-rigido-desarmada",
]


def photo_src(name, small=False):
    return url(f"assets/fotos/{name}{'-600' if small else ''}.webp")


def gallery_html(names):
    items = "".join(
        f'<figure><a href="{photo_src(n)}" target="_blank" rel="noopener"><img src="{photo_src(n, True)}" alt="{escape(PHOTOS[n])}" loading="lazy" width="600" height="600"></a><figcaption>{escape(PHOTOS[n])}</figcaption></figure>'
        for n in names
    )
    return f'<div class="gallery">{items}</div>'


# ---------------------------------------------------------------------------
# Servicios (una página por línea de equipos)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "mantenimiento-cpap-bpap-bogota",
        "photos": ['cpap-resmed-airsense-10-prueba-presion', 'turbina-cpap-philips-dreamstation', 'turbina-cpap-resmed-desarmada', 'cambio-filtro-cpap-resmed', 'humidificador-cpap-dreamstation-limpio', 'banco-trabajo-mantenimiento-cpap'],
        "img": "cpap",
        "icon": "cpap",
        "short": "CPAP y BPAP",
        "audience": "pacientes",
        "title": "Mantenimiento y reparación de CPAP y BPAP en Bogotá | Suba",
        "h1": "Mantenimiento y reparación de CPAP y BPAP en Bogotá",
        "description": "Revisión, mantenimiento y reparación de equipos CPAP y BPAP en Suba y el norte de Bogotá. Diagnóstico por un ingeniero biomédico. Escríbeme por WhatsApp.",
        "card": "Tu equipo no enciende, hace ruido, no da la presión o el humidificador gotea. Lo revisamos y te decimos qué tiene.",
        "intro": "Si usas un CPAP o BPAP para la apnea del sueño u otra condición respiratoria, sabes que una noche sin equipo se nota. Voy a tu casa en Suba y el norte de Bogotá a revisar y reparar tu equipo, con diagnóstico claro antes de hacer cualquier trabajo.",
        "symptoms": [
            "No enciende o se apaga solo",
            "Hace más ruido de lo normal",
            "Sientes que no llega la presión",
            "Muestra un error o alarma en pantalla",
            "El humidificador gotea o no calienta",
            "Huele a quemado o se calienta mucho",
        ],
        "includes": [
            "Diagnóstico del equipo y explicación de lo que encontré.",
            "Limpieza interna y revisión del motor y la turbina.",
            "Revisión de sensores, humidificador, placa calefactora y conexiones.",
            "Cambio de filtros y suministro de repuestos cuando se necesitan.",
            "Prueba de funcionamiento antes de entregarte el equipo.",
            "Recomendaciones de uso y cuidado para que dure más.",
        ],
        "notice": "<strong>Importante:</strong> la presión de tu equipo la define tu médico. El mantenimiento revisa que el equipo funcione bien; no cambia tu prescripción. Si tienes dudas con tu tratamiento, consulta a tu médico.",
        "faq": [
            ("¿Cada cuánto debo hacerle mantenimiento a mi CPAP?", "Lo recomendable es revisar el equipo al menos una vez al año, o antes si notas ruido, olor, alarmas o que la presión no se siente igual. Los filtros y la limpieza de la máscara y la manguera los debes hacer tú con más frecuencia, según el manual del fabricante."),
            ("¿Reparan BPAP además de CPAP?", "Sí. Atiendo tanto equipos CPAP como BPAP (bi-nivel). Escríbeme la marca y el modelo para orientarte desde el primer mensaje."),
            ("¿Cuánto cuesta el mantenimiento de un CPAP?", "Depende del modelo y de lo que tenga el equipo. Primero hago el diagnóstico y te doy el valor antes de hacer cualquier trabajo, para que decidas con la información completa."),
            ("¿Van a domicilio?", "Sí. Voy a tu casa en Suba, Usaquén, Engativá, Barrios Unidos, Chapinero, Chía, Cota y Cajicá. Escríbeme y coordinamos la visita."),
        ],
    },
    {
        "slug": "mantenimiento-concentradores-oxigeno-bogota",
        "photos": ['concentrador-oxigeno-o2-tiger-m50', 'compresor-concentrador-oxigeno', 'filtro-entrada-concentrador-oxigeno', 'concentrador-portatil-inogen-one-g4', 'interior-concentrador-portatil-inogen'],
        "img": "concentrador",
        "icon": "oxygen",
        "short": "Concentradores de oxígeno",
        "audience": "pacientes",
        "title": "Mantenimiento de concentradores de oxígeno en Bogotá | Suba",
        "h1": "Mantenimiento y reparación de concentradores de oxígeno en Bogotá",
        "description": "Mantenimiento preventivo y correctivo de concentradores de oxígeno en Suba y el norte de Bogotá. Revisión de alarmas, flujo y concentración. Escríbeme por WhatsApp.",
        "card": "Alarmas, ruido, calentamiento o baja concentración. Revisamos el equipo para que siga entregando el oxígeno que necesitas.",
        "intro": "Un concentrador de oxígeno trabaja muchas horas seguidas y necesita mantenimiento para seguir entregando el oxígeno que el paciente necesita. Voy a tu casa a hacer el mantenimiento preventivo y correctivo de tu concentrador, en Suba y sus alrededores.",
        "symptoms": [
            "Suena una alarma o se enciende un indicador",
            "Hace ruido fuerte o vibra",
            "Se calienta más de lo normal",
            "El flujo se siente bajo",
            "No enciende o se apaga",
            "Hace tiempo no recibe mantenimiento",
        ],
        "includes": [
            "Diagnóstico y revisión de alarmas.",
            "Limpieza y cambio de filtros.",
            "Revisión del compresor, válvulas y ventilación.",
            "Verificación del flujo y de la concentración de oxígeno entregada.",
            "Suministro de repuestos cuando se necesitan.",
            "Recomendaciones de uso y cuidado diario.",
        ],
        "notice": "<strong>Si el paciente depende del oxígeno:</strong> ten siempre un respaldo (por ejemplo, un cilindro) y, ante cualquier síntoma o una falla total del equipo, comunícate con tu médico, tu EPS o tu proveedor de oxígeno de inmediato.",
        "faq": [
            ("¿Cada cuánto se le hace mantenimiento a un concentrador de oxígeno?", "Depende del uso y del fabricante, pero un equipo que trabaja todos los días debería revisarse periódicamente, al menos una vez al año. Los filtros externos se limpian con más frecuencia, según el manual."),
            ("Mi concentrador pita, ¿qué hago?", "Revisa primero que la manguera no esté doblada y que el equipo tenga buena ventilación. Si la alarma sigue, usa tu respaldo de oxígeno y escríbeme para revisarlo. No ignores una alarma persistente."),
            ("¿Cuánto cuesta el mantenimiento?", "Depende del modelo y del estado del equipo. Te doy el valor después del diagnóstico y antes de hacer cualquier trabajo."),
            ("¿Atienden a domicilio?", "Sí, el servicio es a domicilio en Suba, Usaquén, Engativá, Barrios Unidos, Chapinero, Chía, Cota y Cajicá."),
        ],
    },
    {
        "slug": "mantenimiento-torres-endoscopia-laparoscopia-bogota",
        "photos": ['mantenimiento-fuente-de-luz-olympus', 'optica-fuente-de-luz-endoscopia', 'fuente-de-luz-led-endoscopia-interior', 'camara-endoscopia-hd-desarmada'],
        "img": "torre-endoscopia",
        "icon": "tower",
        "short": "Torres de endoscopia y laparoscopia",
        "audience": "clinicas",
        "title": "Mantenimiento de torres de endoscopia y laparoscopia en Bogotá",
        "h1": "Mantenimiento de torres de endoscopia y laparoscopia en Bogotá",
        "description": "Mantenimiento preventivo y correctivo de torres de endoscopia y laparoscopia para clínicas e IPS en Bogotá: fuente de luz, video, insuflador. Ingeniero biomédico.",
        "card": "Fuentes de luz, procesadores de video, cámaras, insufladores y monitores. Mantenimiento con reporte técnico para tu servicio.",
        "intro": "Cuando una torre de endoscopia o laparoscopia falla, se cancelan procedimientos. Voy a tu clínica, IPS o centro de procedimientos en Bogotá a hacer el mantenimiento preventivo y correctivo, con reportes técnicos que respaldan la gestión de tu tecnología biomédica.",
        "symptoms": [
            "Imagen oscura, con ruido o colores alterados",
            "La fuente de luz no enciende o pierde intensidad",
            "El insuflador no mantiene la presión",
            "Cortes de video entre procesador y monitor",
            "Cables o conectores con falsos contactos",
            "Mantenimiento preventivo vencido",
        ],
        "includes": [
            "Mantenimiento preventivo programado de la torre completa.",
            "Mantenimiento correctivo y diagnóstico de fallas.",
            "Revisión de fuente de luz, procesador de video, cámara, insuflador y monitor.",
            "Suministro de repuestos o alternativas de operación para no detener el servicio.",
            "Reporte técnico de cada intervención para la hoja de vida del equipo.",
            "Capacitación al personal en manejo y cuidado del equipo.",
        ],
        "notice": "",
        "faq": [
            ("¿Entregan reporte de mantenimiento?", "Sí. Cada intervención queda documentada con un reporte técnico que puedes anexar a la hoja de vida del equipo dentro de tu programa de mantenimiento."),
            ("¿Pueden hacer un plan de mantenimiento preventivo para mi clínica?", "Sí. Revisamos tus equipos, definimos la frecuencia de mantenimiento y programamos las visitas para no interrumpir tu agenda de procedimientos."),
            ("¿Qué pasa si la torre falla en medio de la agenda?", "Escríbeme por WhatsApp con la falla. Hago el diagnóstico y, cuando es posible, propongo una alternativa de operación mientras se resuelve la reparación."),
            ("¿Atienden fuera de Bogotá?", "Atiendo Bogotá y municipios cercanos como Chía, Cota y Cajicá. Para otras zonas, escríbeme y lo revisamos."),
        ],
    },
    {
        "slug": "mantenimiento-endoscopios-rigidos-flexibles-bogota",
        "photos": ['vaina-endoscopio-rigido-desarmada', 'vaina-endoscopio-rigido-llaves', 'vaina-endoscopio-rigido-ensamblada'],
        "img": "endoscopio",
        "icon": "scope",
        "short": "Endoscopios rígidos y flexibles",
        "audience": "clinicas",
        "title": "Mantenimiento de endoscopios rígidos y flexibles en Bogotá",
        "h1": "Mantenimiento de endoscopios rígidos y flexibles en Bogotá",
        "description": "Evaluación, mantenimiento y gestión de reparación de endoscopios rígidos y flexibles para clínicas e IPS en Bogotá. Prueba de fugas, angulación y óptica.",
        "card": "Fugas, angulación, imagen borrosa o canal de trabajo obstruido. Evaluación y mantenimiento para alargar la vida útil.",
        "intro": "Un endoscopio es de los equipos más costosos y delicados de un servicio. Detectar a tiempo una fuga o un daño en la óptica evita reparaciones mayores. Hago evaluación y mantenimiento de endoscopios rígidos y flexibles para clínicas e IPS en Bogotá.",
        "symptoms": [
            "Falla en la prueba de fugas",
            "Angulación limitada o dura",
            "Imagen borrosa, manchada o con puntos negros",
            "Canal de trabajo obstruido o dañado",
            "Daños en el tubo de inserción",
            "Ópticas rígidas con imagen opaca",
        ],
        "includes": [
            "Evaluación técnica y prueba de fugas.",
            "Revisión de angulación, canales, óptica y tubo de inserción.",
            "Mantenimiento preventivo y correctivo.",
            "Suministro de repuestos o alternativas de operación.",
            "Reporte técnico para la hoja de vida del equipo.",
            "Capacitación al personal en manejo y cuidado para prevenir daños.",
        ],
        "notice": "",
        "faq": [
            ("¿Cada cuánto se debe revisar un endoscopio flexible?", "Depende del uso, pero la prueba de fugas debe hacerse en cada ciclo de reprocesamiento, y la revisión técnica de forma periódica dentro del programa de mantenimiento del servicio."),
            ("¿Atienden endoscopios rígidos y flexibles?", "Sí, ambos. Escríbeme la marca, el modelo y la falla para orientarte desde el primer mensaje."),
            ("¿La capacitación sirve para reducir daños?", "Sí. Muchos daños vienen del manejo y el reprocesamiento. Capacitar al personal es de las formas más efectivas de alargar la vida útil del equipo."),
        ],
    },
    {
        "slug": "mantenimiento-mobiliario-hospitalario-bogota",
        "img": "cama-hospitalaria",
        "icon": "bed",
        "short": "Mobiliario hospitalario",
        "audience": "ambos",
        "title": "Mantenimiento de camas hospitalarias y mobiliario en Bogotá",
        "h1": "Mantenimiento de camas hospitalarias y mobiliario hospitalario en Bogotá",
        "description": "Reparación y mantenimiento de camas hospitalarias eléctricas y manuales, camillas y mobiliario hospitalario en Suba y el norte de Bogotá. Para hogares y clínicas.",
        "card": "Camas eléctricas y manuales, camillas y mobiliario. Motores, controles, barandas, frenos y ruedas, en casa o en tu institución.",
        "intro": "Una cama hospitalaria que no sube, no baja o tiene las barandas sueltas es un riesgo para el paciente. Voy a tu casa o a tu institución a hacer el mantenimiento de camas hospitalarias y mobiliario, en Suba y el norte de Bogotá.",
        "symptoms": [
            "El motor no responde o el control está dañado",
            "La cama no sube, no baja o no inclina",
            "Barandas sueltas o que no aseguran",
            "Frenos o ruedas en mal estado",
            "Manivelas duras o rotas",
            "Ruidos al mover la cama",
        ],
        "includes": [
            "Diagnóstico de camas eléctricas y manuales.",
            "Revisión de motores, controles y sistema eléctrico.",
            "Ajuste de barandas, frenos, ruedas y mecanismos.",
            "Suministro de repuestos cuando se necesitan.",
            "Mantenimiento preventivo de camillas y mobiliario.",
            "Prueba de funcionamiento y seguridad al terminar.",
        ],
        "notice": "",
        "faq": [
            ("¿Reparan camas hospitalarias para uso en casa?", "Sí. Atiendo tanto a familias con pacientes en casa como a clínicas e instituciones. Escríbeme con la falla y la marca de la cama."),
            ("¿Qué incluye el mantenimiento de una cama eléctrica?", "Revisión de motores, control y cableado, ajuste de mecanismos, barandas, frenos y ruedas, y una prueba de funcionamiento completa."),
            ("¿Cuánto cuesta?", "Depende del tipo de cama y de la falla. Te doy el valor después del diagnóstico y antes de hacer cualquier trabajo."),
        ],
    },
]

FAQ_HOME = [
    ("¿Qué equipos atiendes?", "CPAP y BPAP, concentradores de oxígeno, torres de endoscopia y laparoscopia, endoscopios rígidos y flexibles, y mobiliario hospitalario como camas y camillas."),
    ("¿Atiendes a domicilio?", "Sí, todo mi servicio es a domicilio: voy a tu casa, clínica, IPS o consultorio. Atiendo a ambos. Muchos de mis clientes son familias con equipos en casa, como CPAP, concentradores o camas hospitalarias, y también atiendo clínicas, IPS y consultorios."),
    ("¿En qué zonas de Bogotá trabajas?", "Estoy en Suba y atiendo también Usaquén, Engativá, Barrios Unidos y Chapinero, además de Chía, Cota y Cajicá."),
    ("¿Cómo sé cuánto me va a costar?", "Primero hago el diagnóstico y te explico qué tiene el equipo. Te doy el valor antes de hacer cualquier trabajo, sin sorpresas."),
]


# ---------------------------------------------------------------------------
# Plantillas
# ---------------------------------------------------------------------------
def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": SITE_URL + "/#negocio",
        "name": f"{NAME} — {ROLE}",
        "description": "Mantenimiento preventivo, correctivo y predictivo de equipos biomédicos en Bogotá: CPAP, BPAP, concentradores de oxígeno, endoscopia, laparoscopia y mobiliario hospitalario.",
        "url": SITE_URL + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "image": SITE_URL + "/assets/og-image.png",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Bogotá",
            "addressRegion": "Bogotá D.C.",
            "addressCountry": "CO",
        },
        "areaServed": [{"@type": "Place", "name": z} for z in AREA_SERVED],
        "founder": {"@type": "Person", "name": "Sergio Rodríguez", "jobTitle": ROLE},
        "knowsAbout": [s["short"] for s in SERVICES],
    }


def faq_schema(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + url(p)} for i, (n, p) in enumerate(items)
        ],
    }


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


NAV = [
    ("Inicio", ""),
    ("Servicios", "servicios/"),
    ("Cobertura", "cobertura/"),
    ("Contacto", "contacto/"),
]


def header(current):
    links = "".join(
        f'<li><a href="{url(p)}"{" aria-current=\"page\"" if p == current else ""}>{n}</a></li>' for n, p in NAV
    )
    return f"""<header class="site-header">
  <div class="container nav">
    <a class="brand" href="{url()}" aria-label="{NAME}, inicio">{LOGO}<div><strong>{NAME}</strong><span>{ROLE}</span></div></a>
    <button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <ul class="nav-links">{links}<li class="nav-cta"><a class="btn btn-wa btn-sm" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} WhatsApp</a></li></ul>
  </div>
</header>"""


def footer():
    svc = "".join(f'<li><a href="{url("servicios/" + s["slug"] + "/")}">{s["short"]}</a></li>' for s in SERVICES)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h3>{NAME}</h3>
        <p>{ROLE}. Mantenimiento a domicilio de equipos biomédicos en Suba y el norte de Bogotá.</p>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{', '.join(ZONES_BOGOTA)}, {', '.join(ZONES_MUNI)}</li>
        </ul>
      </div>
      <div><h3>Servicios</h3><ul>{svc}</ul></div>
      <div><h3>Enlaces</h3><ul>
        <li><a href="{url('cobertura/')}">Zonas de cobertura</a></li>
        <li><a href="{url('contacto/')}">Solicitar cotización</a></li>
        <li><a href="{wa_link()}" target="_blank" rel="noopener">Escribir por WhatsApp</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">© {date.today().year} {NAME} · {ROLE} · Bogotá, Colombia</div>
  </div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{ICONS['wa']}</a>"""


def ga():
    if not GA_ID:
        return ""
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""


def page(path, title, description, body, current="", schemas=(), robots="index,follow"):
    canonical = SITE_URL + url(path)
    ld = "\n".join(jsonld(s) for s in schemas)
    return f"""<!doctype html>
<html lang="es-CO" data-base="{BASE}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0d2340">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{url('assets/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{url('assets/styles.css')}">
{ld}
{ga()}
</head>
<body>
{header(current)}
<main>
{body}
</main>
{footer()}
<script src="{url('assets/phone-input.js')}" defer></script>
<script src="{url('assets/main.js')}" defer></script>
</body>
</html>
"""


def faq_html(faq):
    items = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faq)
    return f'<div class="faq">{items}</div>'


def cta_band(title="¿Tu equipo necesita revisión?", text="Escríbeme por WhatsApp con la marca, el modelo y la falla. Te respondo y coordinamos."):
    return f"""<div class="cta-band">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="btn-row"><a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} Escribir por WhatsApp</a><a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="tel:{PHONE_TEL}">{ICONS['phone']} Llamar</a></div>
</div>"""


def card_img(s):
    if s.get("photos"):
        n = s["photos"][0]
        return f'<img class="card-img photo" src="{photo_src(n, True)}" alt="{escape(PHOTOS[n])}" width="600" height="400" loading="lazy">'
    return f'<img class="card-img" src="{url("assets/img/" + s["img"] + ".svg")}" alt="{s["short"]}" width="480" height="320" loading="lazy">'


def hero_img(s):
    if s.get("photos"):
        n = s["photos"][0]
        return f'<img class="hero-img photo" src="{photo_src(n)}" alt="{escape(PHOTOS[n])}" width="1200" height="900" fetchpriority="high">'
    return f'<img class="hero-img" src="{url("assets/img/" + s["img"] + ".svg")}" alt="{s["short"]}" width="480" height="320" fetchpriority="high">'


def service_card(s):
    return f"""<a class="card" href="{url('servicios/' + s['slug'] + '/')}">
  {card_img(s)}
  <h3>{s['short']}</h3>
  <p>{s['card']}</p>
  <span class="more">Ver servicio →</span>
</a>"""


def zones_html():
    items = f'<li class="main">{ICONS["pin"]} {ZONES_MAIN}</li>' + "".join(f"<li>{z}</li>" for z in ZONES_BOGOTA[1:] + ZONES_MUNI)
    return f'<ul class="zones">{items}</ul>'


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------
def build_home():
    pacientes = [s for s in SERVICES if s["audience"] in ("pacientes", "ambos")]
    clinicas = [s for s in SERVICES if s["audience"] in ("clinicas", "ambos")]
    li = lambda lst: "".join(f'<li><a href="{url("servicios/" + s["slug"] + "/")}">{s["short"]}</a></li>' for s in lst)
    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">Ingeniero biomédico en Suba, Bogotá</span>
      <h1>Mantenimiento de equipos biomédicos en Bogotá</h1>
      <p class="lead">Reviso, mantengo y reparo CPAP, BPAP, concentradores de oxígeno, torres de endoscopia y laparoscopia, endoscopios y camas hospitalarias. Voy a tu casa, clínica o consultorio en Suba y sus alrededores.</p>
      <div class="btn-row">
        <a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} Escríbeme por WhatsApp</a>
        <a class="btn btn-ghost" href="{url('contacto/')}">Solicitar cotización</a>
      </div>
      <div class="trust-row">
        <span>{ICONS['check']} Ingeniero biomédico</span>
        <span>{ICONS['check']} Servicio a domicilio</span>
        <span>{ICONS['check']} Diagnóstico antes de cobrar</span>
        <span>{ICONS['pin']} Suba y norte de Bogotá</span>
      </div>
    </div>
    <aside class="hero-card" aria-label="Qué incluye">
      <svg class="pulse" viewBox="0 0 300 56" aria-hidden="true"><path d="M0 30h80l12-18 16 36 14-26 10 8h168"/></svg>
      <h2>Mantenimiento preventivo, correctivo y predictivo</h2>
      <ul class="check-list">
        <li>Diagnóstico claro de lo que tiene tu equipo</li>
        <li>Suministro de repuestos o alternativas de operación</li>
        <li>Reporte técnico de cada intervención</li>
        <li>Capacitación en el manejo y cuidado del equipo</li>
      </ul>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><span class="eyebrow">¿A quién atiendo?</span><h2>Para tu casa o para tu institución</h2></div>
    <div class="grid grid-2" style="margin-top:28px">
      <div class="card audience">
        <span class="tag">Pacientes y familias</span>
        <h3>Tienes un equipo médico en casa</h3>
        <p>Tu CPAP no da la presión, el concentrador pita o la cama no sube. Te ayudo a que tu equipo vuelva a funcionar bien y te explico cómo cuidarlo.</p>
        <ul class="check-list">{li(pacientes)}</ul>
      </div>
      <div class="card audience b2b">
        <span class="tag">Clínicas, IPS y consultorios</span>
        <h3>Necesitas continuidad en tu servicio</h3>
        <p>Mantenimiento programado, respuesta ante fallas y reportes técnicos para la hoja de vida de tus equipos, sin detener tu agenda.</p>
        <ul class="check-list">{li(clinicas)}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="servicios">
  <div class="container">
    <div class="center"><span class="eyebrow">Servicios</span><h2>Equipos que atiendo</h2>
    <p class="lead">Mantenimiento preventivo, correctivo y suministro de repuestos o alternativas de operación en estas líneas.</p></div>
    <div class="grid grid-3" style="margin-top:28px">
      {''.join(service_card(s) for s in SERVICES)}
      <div class="card">
        <div class="icon">{ICONS['train']}</div>
        <h3>Capacitación</h3>
        <p>Entrenamiento al personal o a la familia en el manejo y cuidado de los equipos, para evitar daños y alargar su vida útil.</p>
        <a class="more" href="{url('contacto/')}">Solicitar →</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><span class="eyebrow">Trabajos recientes</span><h2>Así trabajo con tus equipos</h2>
    <p class="lead">Fotos reales de mantenimientos: CPAP ResMed y Philips, concentradores Inogen, fuentes de luz Olympus, desfibriladores Mindray y más.</p></div>
    <div style="margin-top:28px">{gallery_html(HOME_GALLERY)}</div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="center"><span class="eyebrow">Cómo trabajo</span><h2>Simple y sin sorpresas</h2></div>
    <ol class="steps" style="margin-top:28px">
      <li><h3>Me escribes</h3><p>Por WhatsApp o el formulario, con la marca, el modelo y lo que le pasa al equipo.</p></li>
      <li><h3>Visita y diagnóstico</h3><p>Voy a donde estás, reviso el equipo, te explico qué tiene y te doy el valor antes de hacer cualquier trabajo.</p></li>
      <li><h3>Mantenimiento y entrega</h3><p>Hago el trabajo, pruebo el equipo y te entrego un reporte con recomendaciones de cuidado.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <span class="eyebrow">Sobre mí</span>
      <h2>Sergio Rodríguez, ingeniero biomédico</h2>
      <p>Ingeniero biomédico con experiencia en soporte técnico especializado y mantenimiento de equipos biomédicos. Mi trabajo es garantizar la continuidad operativa, la seguridad y el buen desempeño de la tecnología médica, tanto en hogares con pacientes como en servicios de salud.</p>
      <p>Respondo de forma oportuna ante fallas e incidentes, y capacito a quienes usan los equipos para que los cuiden mejor.</p>
    </div>
    <div class="card">
      <h3>Zonas donde atiendo</h3>
      <p>Estoy en Suba y atiendo el norte de Bogotá y la Sabana.</p>
      {zones_html()}
      <p style="margin-top:14px"><a href="{url('cobertura/')}">Ver zonas de cobertura →</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><span class="eyebrow">Preguntas frecuentes</span><h2>Lo que más me preguntan</h2></div>
    <div style="max-width:780px;margin:28px auto 0">{faq_html(FAQ_HOME)}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">{cta_band()}</div>
</section>
"""
    return page(
        "",
        "Mantenimiento de equipos biomédicos en Bogotá | Ing. Sergio Rodríguez",
        "Ingeniero biomédico a domicilio en Suba, Bogotá. Mantenimiento y reparación de CPAP, BPAP, concentradores de oxígeno, endoscopia, laparoscopia y camas hospitalarias.",
        body,
        current="",
        schemas=[business_schema(), faq_schema(FAQ_HOME)],
    )


def build_service(s):
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    symptoms = "".join(f"<li>{escape(x)}</li>" for x in s["symptoms"])
    includes = "".join(f"<li>{escape(x)}</li>" for x in s["includes"])
    notice = f'<div class="notice">{s["notice"]}</div>' if s["notice"] else ""
    related = "".join(f'<li><a href="{url("servicios/" + o["slug"] + "/")}">{o["short"]}</a></li>' for o in others)
    wa_text = f"Hola Sergio, vi tu página y necesito ayuda con un equipo: {s['short']}."
    crumbs = [("Inicio", ""), ("Servicios", "servicios/"), (s["short"], f"servicios/{s['slug']}/")]
    body = f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div>
    <nav class="breadcrumbs" aria-label="Ruta"><ol><li><a href="{url()}">Inicio</a></li><li><a href="{url('servicios/')}">Servicios</a></li><li aria-current="page">{s['short']}</li></ol></nav>
    <h1>{s['h1']}</h1>
    <p class="lead">{s['intro']}</p>
    <div class="btn-row"><a class="btn btn-wa" href="{wa_link(wa_text)}" target="_blank" rel="noopener">{ICONS['wa']} Escríbeme por WhatsApp</a><a class="btn btn-ghost" href="{url('contacto/')}">Solicitar cotización</a></div>
    </div>
    {hero_img(s)}
  </div>
</section>
<section class="section">
  <div class="container content-grid">
    <article class="prose">
      <h2>¿Tu equipo presenta alguna de estas fallas?</h2>
      <ul class="symptoms">{symptoms}</ul>
      {notice}
      <h2>Qué incluye el servicio</h2>
      <ul class="check-list">{includes}</ul>
      {('<h2>Trabajos realizados</h2>' + gallery_html(s['photos'][1:])) if len(s.get('photos', [])) > 1 else ''}
      <h2>Zonas donde atiendo</h2>
      <p>Estoy ubicado en Suba y atiendo en el norte de Bogotá y la Sabana:</p>
      {zones_html()}
      <h2>Preguntas frecuentes</h2>
      {faq_html(s['faq'])}
    </article>
    <aside class="aside-card">
      <h3>Cotiza tu servicio</h3>
      <p>Envíame la marca, el modelo y la falla. Te doy el valor después del diagnóstico y antes de hacer cualquier trabajo.</p>
      <a class="btn btn-wa" href="{wa_link(wa_text)}" target="_blank" rel="noopener">{ICONS['wa']} WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICONS['phone']} {PHONE_DISPLAY}</a>
      <h3 style="margin-top:24px">Otros servicios</h3>
      <ul style="padding-left:1.1em;margin:0">{related.replace('<a ', '<a style="color:#e2eaf3" ')}</ul>
    </aside>
  </div>
</section>
<section class="section" style="padding-top:0"><div class="container">{cta_band()}</div></section>
"""
    svc_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["h1"],
        "serviceType": "Mantenimiento de " + s["short"],
        "description": s["description"],
        "provider": {"@id": SITE_URL + "/#negocio"},
        "areaServed": [{"@type": "Place", "name": z} for z in AREA_SERVED],
        "url": SITE_URL + url(f"servicios/{s['slug']}/"),
    }
    return page(
        f"servicios/{s['slug']}/",
        s["title"],
        s["description"],
        body,
        current="servicios/",
        schemas=[business_schema(), svc_schema, faq_schema(s["faq"]), breadcrumb_schema(crumbs)],
    )


def build_services_index():
    body = f"""
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Ruta"><ol><li><a href="{url()}">Inicio</a></li><li aria-current="page">Servicios</li></ol></nav>
    <h1>Servicios de mantenimiento de equipos biomédicos</h1>
    <p class="lead">Mantenimiento preventivo, correctivo y predictivo, y suministro de repuestos o alternativas de operación, en Suba y el norte de Bogotá.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid-3">{''.join(service_card(s) for s in SERVICES)}
      <div class="card"><div class="icon">{ICONS['train']}</div><h3>Capacitación</h3><p>Entrenamiento en el manejo y cuidado de los equipos para el personal de tu institución o para la familia del paciente.</p><a class="more" href="{url('contacto/')}">Solicitar →</a></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0"><div class="container">{cta_band()}</div></section>
"""
    crumbs = [("Inicio", ""), ("Servicios", "servicios/")]
    return page("servicios/", "Servicios de mantenimiento biomédico en Bogotá | Ing. Sergio Rodríguez",
                "CPAP, BPAP, concentradores de oxígeno, torres de endoscopia y laparoscopia, endoscopios y mobiliario hospitalario. Mantenimiento en Suba y norte de Bogotá.",
                body, current="servicios/", schemas=[business_schema(), breadcrumb_schema(crumbs)])


def build_coverage():
    suba = ", ".join(ZONES_SUBA)
    rows = "".join(
        f'<li><a href="{url("servicios/" + s["slug"] + "/")}">{s["short"]}</a></li>' for s in SERVICES
    )
    body = f"""
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Ruta"><ol><li><a href="{url()}">Inicio</a></li><li aria-current="page">Cobertura</li></ol></nav>
    <h1>Mantenimiento de equipos biomédicos en Suba y el norte de Bogotá</h1>
    <p class="lead">Estoy ubicado en Suba y trabajo a domicilio. Voy a donde están pacientes en casa, clínicas, IPS y consultorios del norte de Bogotá y de la Sabana.</p>
  </div>
</section>
<section class="section">
  <div class="container content-grid">
    <article class="prose">
      <h2>Zonas de cobertura</h2>
      {zones_html()}
      <h2>Suba</h2>
      <p>Suba es mi base de trabajo, así que es donde puedo responder más rápido. Atiendo barrios como {suba}, entre otros.</p>
      <h2>Usaquén, Engativá, Barrios Unidos y Chapinero</h2>
      <p>Atiendo estas localidades vecinas de Suba, donde se concentran muchas clínicas, consultorios y centros de procedimientos del norte de la ciudad.</p>
      <h2>Chía, Cota y Cajicá</h2>
      <p>También llego a los municipios de la Sabana más cercanos a Suba. Escríbeme y coordinamos la visita.</p>
      <h2>Equipos que atiendo en estas zonas</h2>
      <ul>{rows}</ul>
      <p>¿Estás en otra zona? Escríbeme de todas formas y revisamos si puedo atenderte.</p>
    </article>
    <aside class="aside-card">
      <h3>¿Estás en mi zona?</h3>
      <p>Cuéntame dónde estás, qué equipo tienes y qué le pasa.</p>
      <a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICONS['phone']} {PHONE_DISPLAY}</a>
    </aside>
  </div>
</section>
"""
    crumbs = [("Inicio", ""), ("Cobertura", "cobertura/")]
    return page("cobertura/", "Equipos biomédicos en Suba, Usaquén, Engativá, Chía y Cota",
                "Ingeniero biomédico en Suba. Mantenimiento de equipos biomédicos en Suba, Usaquén, Engativá, Barrios Unidos, Chapinero, Chía, Cota y Cajicá.",
                body, current="cobertura/", schemas=[business_schema(), breadcrumb_schema(crumbs)])


def build_contact():
    options = "".join(f"<option>{s['short']}</option>" for s in SERVICES) + "<option>Otro equipo</option>"
    zones = "".join(f"<option>{z}</option>" for z in AREA_SERVED) + "<option>Otra zona</option>"
    body = f"""
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Ruta"><ol><li><a href="{url()}">Inicio</a></li><li aria-current="page">Contacto</li></ol></nav>
    <h1>Solicita una cotización</h1>
    <p class="lead">La forma más rápida es WhatsApp. Si prefieres, llena el formulario y te contacto.</p>
  </div>
</section>
<section class="section">
  <div class="container content-grid">
    <form id="form-cotizacion" class="form card" data-key="{WEB3FORMS_KEY}" data-wa="{WA_NUMBER}" novalidate>
      <div><label for="nombre">Nombre</label><input id="nombre" name="nombre" required autocomplete="name"></div>
      <div><label>Teléfono o WhatsApp</label><div class="phone-field" data-phone-input data-name="telefono" data-label="Número de celular" data-required></div></div>
      <div class="row">
        <div><label for="tipo">Soy</label><select id="tipo" name="tipo"><option>Paciente o familiar</option><option>Clínica, IPS o consultorio</option><option>Otro</option></select></div>
        <div><label for="zona">Zona</label><select id="zona" name="zona">{zones}</select></div>
      </div>
      <div><label for="equipo">Equipo</label><select id="equipo" name="equipo">{options}</select></div>
      <div><label for="mensaje">¿Qué le pasa al equipo? (marca y modelo si los tienes)</label><textarea id="mensaje" name="mensaje" required></textarea></div>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-primary" type="submit">Enviar solicitud</button>
      <p class="form-status" role="status" aria-live="polite"></p>
      <p class="form-note">Uso tus datos solo para responder tu solicitud.</p>
    </form>
    <aside class="aside-card">
      <h3>Contacto directo</h3>
      <p>{NAME}<br>{ROLE}<br>Suba, Bogotá</p>
      <a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICONS['phone']} {PHONE_DISPLAY}</a>
      <p style="margin-top:16px"><a style="color:#e2eaf3" href="mailto:{EMAIL}">{EMAIL}</a></p>
    </aside>
  </div>
</section>
"""
    crumbs = [("Inicio", ""), ("Contacto", "contacto/")]
    return page("contacto/", "Contacto y cotización | Ing. Sergio Rodríguez, ingeniero biomédico",
                "Solicita una cotización de mantenimiento de equipos biomédicos en Bogotá. WhatsApp 301 449 7065. Atención en Suba y el norte de Bogotá.",
                body, current="contacto/", schemas=[business_schema(), breadcrumb_schema(crumbs)])


def build_404():
    body = f"""
<section class="section"><div class="container center">
  <h1>Esta página no existe</h1>
  <p class="lead">Puede que el enlace haya cambiado. Vuelve al inicio o escríbeme directo.</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="{url()}">Ir al inicio</a><a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['wa']} WhatsApp</a></div>
</div></section>"""
    return page("404.html", "Página no encontrada | Ing. Sergio Rodríguez", "La página que buscas no existe.", body, robots="noindex,follow")


# ---------------------------------------------------------------------------
# Escritura
# ---------------------------------------------------------------------------
def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    pages = [("", build_home())]
    pages.append(("servicios/", build_services_index()))
    for s in SERVICES:
        pages.append((f"servicios/{s['slug']}/", build_service(s)))
    pages.append(("cobertura/", build_coverage()))
    pages.append(("contacto/", build_contact()))

    for p, html in pages:
        write(os.path.join(p, "index.html"), html)
    write("404.html", build_404())

    priority = {"": "1.0", "contacto/": "0.6", "cobertura/": "0.7", "servicios/": "0.8"}
    urls = "".join(
        f"<url><loc>{SITE_URL + url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{priority.get(p, '0.9')}</priority></url>"
        for p, _ in pages
    )
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    write("CNAME", DOMAIN + "\n")
    print(f"Listo: {len(pages) + 1} páginas generadas para {SITE_URL}")


if __name__ == "__main__":
    main()
