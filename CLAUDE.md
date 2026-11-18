# Reglas del proyecto

- El contenido se edita en `tools/build.py` y se regenera con `python3 tools/build.py`. No editar los `index.html` a mano.
- **Campos de teléfono**: siempre con el componente `assets/phone-input.js`
  (`<div class="phone-field" data-phone-input data-name="..." data-label="..." data-required></div>`):
  botón con bandera y flecha a la izquierda, etiqueta pequeña dentro del campo, indicativo (+57) antes del número,
  y desplegable con buscador de países, lista "País (+código)" con bandera y check en el seleccionado.
  Colombia por defecto. Nunca un `<input type="tel">` suelto.
- Banderas locales en `assets/flags/` (flag-icons, MIT). Si se agrega un país, copiar su SVG ahí.
- Las imágenes de `assets/img/` son ilustraciones provisionales; reemplazar por fotos reales de Sergio cuando existan.
