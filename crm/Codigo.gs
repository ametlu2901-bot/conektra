/**
 * Enlaza Studio — CRM de prospectos en Google Sheets
 *
 * Instalación (una sola vez):
 *  1. Hoja de cálculo nueva → Extensiones → Apps Script → pega este archivo.
 *  2. Ejecuta la función «configurar» y acepta los permisos.
 *  3. Implementar → Nueva implementación → Aplicación web.
 *     Ejecutar como: Yo. Acceso: Cualquiera.
 *  4. Copia la URL /exec y ponla en CONFIG["crm"] de build.py; luego python build.py.
 * Para cambios posteriores: Administrar implementaciones → editar → Nueva versión (la URL no cambia).
 */

const HOJA_PROSPECTOS = 'Prospectos';
const HOJA_RESUMEN = 'Resumen';
const COLUMNAS = ['Fecha', 'Nombre', 'Empresa', 'Contacto', 'Necesita', 'Presupuesto', 'Mensaje', 'Idioma', 'Estado', 'Valor (USD)', 'Próximo paso', 'Notas'];
const ESTADOS = ['Nuevo', 'Contactado', 'Propuesta enviada', 'Negociación', 'Ganado', 'Perdido'];
const NECESIDADES = ['Página web', 'CRM', 'Integraciones', 'ERP', 'Otro', 'Website', 'Integrations', 'Other'];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.web) return respuesta({ ok: true }); // trampa para robots
  const nombre = limpiar(p.nombre, 80), contacto = limpiar(p.contacto, 120);
  if (!nombre || !contacto) return respuesta({ ok: false, error: 'faltan datos' });
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_PROSPECTOS).appendRow([
      new Date(), nombre, limpiar(p.empresa, 100), contacto, limpiar(p.necesita, 120),
      limpiar(p.presupuesto, 40), limpiar(p.mensaje, 1500), limpiar(p.idioma, 5), 'Nuevo', '', '', '',
    ]);
  } finally {
    lock.releaseLock();
  }
  return respuesta({ ok: true });
}

function doGet() {
  return respuesta({ ok: true, servicio: 'Enlaza Studio CRM' });
}

function respuesta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// recorta, quita caracteres de control y evita que el texto se ejecute como fórmula
function limpiar(valor, max) {
  let t = String(valor || '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim().slice(0, max);
  if (/^[=+\-@]/.test(t)) t = "'" + t;
  return t;
}

function configurar() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  libro.setSpreadsheetTimeZone('America/Panama');

  const hoja = libro.getSheetByName(HOJA_PROSPECTOS) || libro.insertSheet(HOJA_PROSPECTOS, 0);
  hoja.getRange(1, 1, 1, COLUMNAS.length).setValues([COLUMNAS]).setFontWeight('bold').setBackground('#0b1220').setFontColor('#ffffff');
  hoja.setFrozenRows(1);
  hoja.getRange('A:A').setNumberFormat('dd/MM/yyyy HH:mm');
  hoja.getRange('J:J').setNumberFormat('"$"#,##0');
  hoja.getRange('I2:I').setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(ESTADOS, true).setAllowInvalid(false).build());
  const colores = { 'Nuevo': '#fff4c2', 'Contactado': '#dbe8ff', 'Propuesta enviada': '#e7dcff', 'Negociación': '#d2f1ff', 'Ganado': '#c9f2d0', 'Perdido': '#f5d0d0' };
  const rango = hoja.getRange('I2:I');
  hoja.setConditionalFormatRules(Object.keys(colores).map(e =>
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(e).setBackground(colores[e]).setRanges([rango]).build()));
  [140, 160, 160, 190, 190, 130, 360, 70, 140, 110, 200, 260].forEach((w, i) => hoja.setColumnWidth(i + 1, w));

  const sum = libro.getSheetByName(HOJA_RESUMEN) || libro.insertSheet(HOJA_RESUMEN, 1);
  sum.clear();
  const P = `'${HOJA_PROSPECTOS}'`;
  const filas = [
    ['Prospectos por etapa', ''],
    ...ESTADOS.map(e => [e, `=COUNTIF(${P}!I:I,"${e}")`]),
    ['Total de prospectos', `=COUNTA(${P}!B2:B)`],
    ['Prospectos este mes', `=COUNTIFS(${P}!A2:A,">="&EOMONTH(TODAY(),-1)+1)`],
    ['Ganado (USD)', `=SUMIF(${P}!I:I,"Ganado",${P}!J:J)`],
    ['En negociación (USD)', `=SUMIF(${P}!I:I,"Negociación",${P}!J:J)+SUMIF(${P}!I:I,"Propuesta enviada",${P}!J:J)`],
    ['Tasa de cierre', `=IFERROR(COUNTIF(${P}!I:I,"Ganado")/COUNTA(${P}!B2:B),0)`],
  ];
  filas.forEach((f, i) => {
    sum.getRange(i + 1, 1).setValue(f[0]);
    if (f[1]) sum.getRange(i + 1, 2).setFormula(f[1]);
  });
  sum.getRange(1, 1, 1, 2).setFontWeight('bold').setBackground('#0b1220').setFontColor('#ffffff');
  sum.getRange(ESTADOS.length + 4, 2, 2, 1).setNumberFormat('"$"#,##0');
  sum.getRange(ESTADOS.length + 6, 2).setNumberFormat('0%');
  sum.setColumnWidth(1, 240);
  sum.setColumnWidth(2, 140);

  const sobra = libro.getSheetByName('Hoja 1') || libro.getSheetByName('Sheet1');
  if (sobra && libro.getSheets().length > 2) libro.deleteSheet(sobra);
}
