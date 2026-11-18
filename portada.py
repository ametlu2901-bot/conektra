"""Panel ancho de la portada: entradas → Conektra → tus sistemas, con paquetes que viajan.

Se dibujan dos versiones del mismo flujo: horizontal (computadora) y vertical (celular).
Los nodos son HTML posicionados en porcentaje sobre un lienzo SVG con la misma proporción,
para que los círculos de los paquetes no se deformen.
"""

TEXTOS = {
    "es": dict(titulo="Un cliente nuevo", vivo="En vivo", entradas="Cómo te encuentran", sistemas="Qué pasa después"),
    "en": dict(titulo="A new customer", vivo="Live", entradas="How they find you", sistemas="What happens next"),
}

# índices dentro de T["nodos"]: [Web, CRM, ERP, WhatsApp, Pagos, Sheets]
ENTRADAS = [0, 3, 4]
SALIDAS = [1, 2, 5]
DUR = 2.2          # segundos que tarda un paquete en cada tramo
DESFASE = [0.0, 0.8, 1.6]


def _lienzo(T, I, NUCLEO, ancho, alto, pos_in, pos_out, centro, curva_in, curva_out, clase):
    halo = ('<radialGradient id="g-halo-{c}"><stop offset="0" stop-color="#b9f5cf" stop-opacity=".95"/>'
            '<stop offset=".45" stop-color="#1f6b52" stop-opacity=".45"/><stop offset="1" stop-color="#1f6b52" stop-opacity="0"/></radialGradient>').format(c=clase)
    rutas, paquetes, nodos = [], [], []
    for k, (idx, (x, y)) in enumerate(zip(ENTRADAS, pos_in)):
        rid = f"r-{clase}-in-{k}"
        rutas.append(f'<path class="ruta" id="{rid}" d="{curva_in(x, y)}"/><path class="flujo" d="{curva_in(x, y)}"/>')
        paquetes.append(_paquete(rid, DESFASE[k], clase))
        nodos.append(_nodo(T, I, idx, x, y, ancho, alto, DESFASE[k]))
    for k, (idx, (x, y)) in enumerate(zip(SALIDAS, pos_out)):
        rid = f"r-{clase}-out-{k}"
        rutas.append(f'<path class="ruta" id="{rid}" d="{curva_out(x, y)}"/><path class="flujo" d="{curva_out(x, y)}"/>')
        # sale del núcleo justo cuando llega el paquete de la entrada con el mismo número
        paquetes.append(_paquete(rid, DESFASE[k] + DUR, clase))
        nodos.append(_nodo(T, I, idx, x, y, ancho, alto, DESFASE[k] + 2 * DUR))
    cx, cy = centro
    return f'''<div class="flujo-panel__lienzo flujo-panel__lienzo--{clase}" style="aspect-ratio:{ancho}/{alto}">
          <svg viewBox="0 0 {ancho} {alto}" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><defs>{halo}</defs>{"".join(rutas)}{"".join(paquetes)}</svg>
          <div class="nucleo nucleo--panel" style="left:{cx / ancho * 100:.3f}%;top:{cy / alto * 100:.3f}%"><span class="onda"></span><span class="onda"></span><span class="onda"></span><span class="nucleo__cara">{NUCLEO}<b>Conektra</b></span></div>
          {"".join(nodos)}
        </div>'''


def _paquete(rid, inicio, clase):
    # el ciclo completo dura 3 tramos (entrada, salida y una pausa) para que se lea la secuencia
    # el paquete es invisible mientras espera; se ve solo durante su recorrido
    return (f'<g class="paquete" opacity="0"><circle r="11" fill="url(#g-halo-{clase})"/><circle r="3.6" fill="#fff"/>'
            f'<animateMotion dur="{DUR}s" begin="{inicio}s;{rid}-m.end+{2 * DUR}s" id="{rid}-m"><mpath href="#{rid}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.88;1" dur="{DUR}s" begin="{rid}-m.begin"/></g>')


def _nodo(T, I, idx, x, y, ancho, alto, llegada):
    n, s, ico = T["nodos"][idx]
    return (f'<div class="nodo nodo--panel" style="left:{x / ancho * 100:.3f}%;top:{y / alto * 100:.3f}%;--ciclo:{3 * DUR}s;--llegada:{llegada:.2f}s">'
            f'<i>{I[ico]}</i><span>{n}<small>{s}</small></span></div>')


def panel(T, I, NUCLEO):
    X = TEXTOS[T["lang"]]
    # horizontal 1000x400: entradas a la izquierda, núcleo al centro, sistemas a la derecha
    ancho = _lienzo(
        T, I, NUCLEO, 1000, 400,
        pos_in=[(150, 85), (150, 200), (150, 315)], pos_out=[(850, 85), (850, 200), (850, 315)], centro=(500, 200),
        curva_in=lambda x, y: f"M{x + 70} {y} C {x + 210} {y}, 330 200, 430 200",
        curva_out=lambda x, y: f"M570 200 C 670 200, {x - 210} {y}, {x - 70} {y}",
        clase="ancho")
    # vertical 380x620: entradas arriba, núcleo al medio, sistemas abajo
    alto = _lienzo(
        T, I, NUCLEO, 380, 620,
        pos_in=[(68, 70), (190, 70), (312, 70)], pos_out=[(68, 550), (190, 550), (312, 550)], centro=(190, 310),
        curva_in=lambda x, y: f"M{x} {y + 34} C {x} {y + 140}, 190 170, 190 250",
        curva_out=lambda x, y: f"M190 370 C 190 450, {x} {y - 140}, {x} {y - 34}",
        clase="alto")
    aviso0 = T["avisos"][0]
    return f'''<div class="flujo-panel aparece" style="--a:1s" aria-hidden="true">
        <div class="flujo-panel__brillo"></div>
        <div class="flujo-panel__barra"><span class="flujo-panel__puntos"><i></i><i></i><i></i></span><b>{X["titulo"]}</b><span class="flujo-panel__vivo"><i></i>{X["vivo"]}</span></div>
        <div class="flujo-panel__cuerpo">
          <div class="flujo-panel__columnas"><span>{X["entradas"]}</span><span>{X["sistemas"]}</span></div>
          {ancho}
          {alto}
        </div>
        <div class="flujo-panel__pie"><span class="aviso" id="aviso"><span class="aviso__ico">{I["rayo"]}</span><span><b id="aviso-titulo">{aviso0[0]}</b> <span id="aviso-texto">{aviso0[1]}</span></span></span></div>
      </div>'''
