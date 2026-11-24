# Sitio web — Ing. Sergio Rodríguez, Ingeniero Biomédico

Sitio estático multipágina con SEO local para Suba y el norte de Bogotá.
Publicado con GitHub Pages en **https://biomedico.alexmonroy.com**.

## Estructura

| Página | URL |
|---|---|
| Inicio | `/` |
| Servicios | `/servicios/` |
| CPAP y BPAP | `/servicios/mantenimiento-cpap-bpap-bogota/` |
| Concentradores de oxígeno | `/servicios/mantenimiento-concentradores-oxigeno-bogota/` |
| Torres de endoscopia y laparoscopia | `/servicios/mantenimiento-torres-endoscopia-laparoscopia-bogota/` |
| Endoscopios rígidos y flexibles | `/servicios/mantenimiento-endoscopios-rigidos-flexibles-bogota/` |
| Mobiliario hospitalario | `/servicios/mantenimiento-mobiliario-hospitalario-bogota/` |
| Cobertura | `/cobertura/` |
| Contacto / cotización | `/contacto/` |

Incluye `sitemap.xml`, `robots.txt`, datos estructurados (ProfessionalService, Service, FAQPage, BreadcrumbList), Open Graph y botón flotante de WhatsApp.

## Cómo editar

Todo el contenido está en `tools/build.py` (textos, servicios, zonas, teléfono, preguntas frecuentes). Después de editar:

```bash
python3 tools/build.py
```

y sube los cambios. No edites los `index.html` a mano: se sobrescriben al generar.

## Puesta en marcha

1. **Hacer el repo público**: Settings → Danger Zone → Change visibility → Public.
2. **Activar GitHub Pages**: Settings → Pages → Source: *Deploy from a branch* → Branch `main`, carpeta `/ (root)`.
3. **DNS del subdominio**: en el proveedor de DNS de `alexmonroy.com`, crear un registro
   `CNAME` con nombre `biomedico` apuntando a `alexwebpuro.github.io`.
4. En Settings → Pages, escribir `biomedico.alexmonroy.com` como Custom domain y, cuando el certificado esté listo, activar **Enforce HTTPS**.

## Formulario (Web3Forms)

Mientras no haya clave, el formulario abre WhatsApp con el mensaje ya escrito.
Para recibirlo por correo: Sergio entra a https://web3forms.com, pone su correo, recibe la *Access Key*
y se pega en `WEB3FORMS_KEY` dentro de `tools/build.py`. Luego se regenera el sitio.

## Después de publicar (lo que más trae clientes)

- **Google Business Profile** de Sergio, como negocio de área de servicio (sin dirección pública), con zonas Suba, Usaquén, Engativá, Chía, Cota, etc. Enlazar a este sitio. Pedir reseñas a cada cliente.
- **Google Search Console**: verificar el dominio y enviar `https://biomedico.alexmonroy.com/sitemap.xml`.
- Opcional: Google Analytics 4 (poner el ID en `GA_ID`).

## Pendiente por confirmar con Sergio

- [ ] Marcas y modelos que maneja (ResMed, Philips, Yuwell, Olympus, Storz, Pentax…) para añadirlos a cada servicio.
- [ ] Si hace calibración e instalación y si entrega certificado.
- [ ] Fotos de mobiliario hospitalario (esa página aún usa ilustración).
- [ ] Revisar que los textos técnicos de cada servicio reflejan lo que él hace.
