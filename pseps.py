#!/usr/bin/env python3
"""
PSEPS — Principio de Sustitución de Elementos de Proceso Software.

Prototipo que evalúa si una actividad candidata H puede reemplazar a una
actividad núcleo B de un proceso híbrido, comparando sus contratos:

  R1 (no exigir más):            ∀p ∈ Pre(H)  ∃q ∈ Pre(B):  q ⊒ p
  R2 (no entregar menos):        ∀q ∈ Post(B) ∃p ∈ Post(H): p ⊒ q
  R3 (conservar la invariante):  Inv(H) ⇒ Inv(B)

q ⊒ p ("q cubre a p") usa la escala de equivalencia del ICF de CHAPLIN:
cobertura ≥ umbral plena  → cobertura plena
cobertura ≥ umbral parcial → cobertura parcial (exige una adaptación A)
en otro caso              → sin cobertura

Recomendación:
  Recomendable                 R1–R3 se cumplen con cobertura plena
  Recomendable con precaución  R1–R3 se cumplen, alguna solo con cobertura parcial (+ A)
  No recomendable              alguna regla es falsa

Uso:
  python pseps.py datos/water-scrum-fall.json            # evalúa y muestra la tabla
  python pseps.py datos/water-scrum-fall.json --detalle  # muestra cada comprobación
  python pseps.py datos/water-scrum-fall.json --salida resultados
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

PLENA, PARCIAL, FALLA = "plena", "parcial", "falla"
RECOMENDABLE = "Recomendable"
PRECAUCION = "Recomendable con precaución"
NO_RECOMENDABLE = "No recomendable"


# ----------------------------------------------------------------- modelo
@dataclass
class Comprobacion:
    """Resultado de comprobar un elemento dentro de una regla."""
    elemento: str
    nivel: str                      # plena | parcial | falla
    detalle: str
    adaptacion: str | None = None


@dataclass
class ResultadoRegla:
    regla: str
    comprobaciones: list[Comprobacion] = field(default_factory=list)

    @property
    def nivel(self) -> str:
        niveles = {c.nivel for c in self.comprobaciones}
        if FALLA in niveles:
            return FALLA
        if PARCIAL in niveles:
            return PARCIAL
        return PLENA

    @property
    def cumple(self) -> bool:
        return self.nivel != FALLA

    @property
    def adaptaciones(self) -> list[str]:
        return [c.adaptacion for c in self.comprobaciones if c.adaptacion]


@dataclass
class Evaluacion:
    id: str
    nucleo: str
    candidata: str
    reglas: dict[str, ResultadoRegla]

    @property
    def recomendacion(self) -> str:
        niveles = [r.nivel for r in self.reglas.values()]
        if FALLA in niveles:
            return NO_RECOMENDABLE
        if PARCIAL in niveles:
            return PRECAUCION
        return RECOMENDABLE

    @property
    def adaptaciones(self) -> list[str]:
        vistas: list[str] = []
        for r in self.reglas.values():
            for a in r.adaptaciones:
                if a not in vistas:
                    vistas.append(a)
        return vistas


# ----------------------------------------------------------------- motor
class PSEPS:
    def __init__(self, caso: dict):
        self.caso = caso
        self.plena = caso["umbrales"]["plena"]
        self.parcial = caso["umbrales"]["parcial"]
        self.artefactos = caso["artefactos"]
        self.eq = {(e["de"], e["a"]): e for e in caso["equivalencias"]}
        self.invariantes = caso["invariantes"]
        self.nucleo = caso["nucleo"]["actividades"]
        self.candidatas = caso["candidatas"]
        self._validar()

    # -- validación de datos
    def _validar(self) -> None:
        conocidos = set(self.artefactos)
        for nombre, act in list(self.nucleo.items()) + list(self.candidatas.items()):
            for lista in ("pre", "post", "opcionales"):
                for a in act.get(lista, []):
                    if a not in conocidos:
                        raise ValueError(f"{nombre}: artefacto desconocido '{a}' en {lista}")
        for c_id, c in self.candidatas.items():
            if c["reemplaza"] not in self.nucleo:
                raise ValueError(f"{c_id}: reemplaza a una actividad núcleo inexistente")

    # -- cobertura dirigida q ⊒ p
    def cobertura(self, q: str, p: str) -> tuple[float, dict | None]:
        if q == p:
            return 1.0, None
        e = self.eq.get((q, p))
        return (e["cobertura"], e) if e else (0.0, None)

    def nivel(self, cob: float) -> str:
        if cob >= self.plena:
            return PLENA
        if cob >= self.parcial:
            return PARCIAL
        return FALLA

    def mejor_cobertura(self, fuentes: list[str], objetivo: str) -> Comprobacion:
        """Busca en `fuentes` el artefacto que mejor cubre a `objetivo`."""
        mejor = (-1.0, None, None)
        for q in fuentes:
            cob, e = self.cobertura(q, objetivo)
            if cob > mejor[0]:
                mejor = (cob, q, e)
        cob, q, e = mejor
        nivel = self.nivel(cob)
        if q is None:
            return Comprobacion(objetivo, FALLA, f"no hay artefactos que cubran {objetivo}")
        if nivel == FALLA:
            falta = f" (falta {e['falta']})" if e and e.get("falta") else ""
            return Comprobacion(objetivo, FALLA, f"ningún artefacto cubre {objetivo}: mejor {q} ⊒ {objetivo} = {cob:g}{falta}")
        if nivel == PARCIAL:
            return Comprobacion(objetivo, PARCIAL,
                                f"{q} ⊒ {objetivo} = {cob:g} (falta {e.get('falta', '?')})",
                                adaptacion=e.get("adaptacion"))
        return Comprobacion(objetivo, PLENA, f"{q} ⊒ {objetivo} = {cob:g}")

    # -- propiedades de la invariante, evaluadas sobre la candidata H
    def propiedad(self, prop: str, h: dict) -> Comprobacion:
        pre, post, roles = h["pre"], h["post"], h.get("roles", [])
        si = lambda ok, txt: Comprobacion(prop, PLENA if ok else FALLA, txt)

        if prop in ("iterativo", "secuencial"):
            return si(h["ciclo"] == prop, f"ciclo {h['ciclo']}")
        if prop == "sin_documento_congelado":
            cong = [a for a in pre if self.artefactos[a]["congelado"]]
            return si(not cong, "ninguna entrada congelada" if not cong else f"entrada congelada: {', '.join(cong)}")
        if prop == "participa_product_owner":
            return si("Product Owner" in roles, "participa el Product Owner" if "Product Owner" in roles else "sin Product Owner")
        if prop == "ejecuta_equipo":
            return si("Equipo" in roles, "la ejecuta el equipo" if "Equipo" in roles else "no la ejecuta el equipo")
        if prop == "aprobado_con_firma":
            sin = [a for a in post if not self.artefactos[a]["firmado"]]
            return si(not sin, "salidas firmadas" if not sin else f"sin firma: {', '.join(sin)}")
        if prop == "trazabilidad":
            sin = [a for a in post if not self.artefactos[a]["trazable"]]
            return si(not sin, "salidas trazables" if not sin else f"sin trazabilidad: {', '.join(sin)}")
        if prop == "entrega_incremento":
            c = self.mejor_cobertura(post, "Incremento")
            return Comprobacion(prop, c.nivel, c.detalle, c.adaptacion)
        if prop == "actualiza_product_backlog":
            c = self.mejor_cobertura(post, "Product Backlog")
            return Comprobacion(prop, c.nivel, c.detalle, c.adaptacion)
        raise ValueError(f"propiedad de invariante desconocida: {prop}")

    # -- reglas
    def r1(self, b: dict, h: dict) -> ResultadoRegla:
        """No exigir más: cada entrada obligatoria de H está cubierta por alguna de B."""
        r = ResultadoRegla("R1")
        for p in h["pre"]:
            r.comprobaciones.append(self.mejor_cobertura(b["pre"], p))
        return r

    def r2(self, b: dict, h: dict) -> ResultadoRegla:
        """No entregar menos: cada salida de B está cubierta por alguna de H."""
        r = ResultadoRegla("R2")
        for q in b["post"]:
            r.comprobaciones.append(self.mejor_cobertura(h["post"], q))
        return r

    def r3(self, b: dict, h: dict) -> ResultadoRegla:
        """Conservar la invariante: H cumple cada propiedad de Inv(B)."""
        r = ResultadoRegla("R3")
        for prop in self.invariantes[b["invariante"]]:
            r.comprobaciones.append(self.propiedad(prop, h))
        return r

    def evaluar(self, c_id: str) -> Evaluacion:
        h = self.candidatas[c_id]
        b = self.nucleo[h["reemplaza"]]
        reglas = {"R1": self.r1(b, h), "R2": self.r2(b, h), "R3": self.r3(b, h)}
        return Evaluacion(c_id, b["nombre"], h["nombre"], reglas)

    def evaluar_todas(self) -> list[Evaluacion]:
        return [self.evaluar(c) for c in self.candidatas]


# ----------------------------------------------------------------- salida
MARCA = {PLENA: "✓", PARCIAL: "✓ (parcial)", FALLA: "✗"}


def tabla(evals: list[Evaluacion]) -> str:
    filas = [("#", "Núcleo B → Candidata H", "R1", "R2", "R3", "Recomendación")]
    for e in evals:
        filas.append((e.id, f"{e.nucleo} → {e.candidata}",
                      *(MARCA[e.reglas[k].nivel] for k in ("R1", "R2", "R3")), e.recomendacion))
    anchos = [max(len(f[i]) for f in filas) for i in range(len(filas[0]))]
    linea = lambda f: "  ".join(c.ljust(w) for c, w in zip(f, anchos))
    out = [linea(filas[0]), "  ".join("-" * w for w in anchos)]
    out += [linea(f) for f in filas[1:]]
    return "\n".join(out)


def detalle(e: Evaluacion) -> str:
    out = [f"{e.id}: {e.nucleo} → {e.candidata}  ⇒  {e.recomendacion}"]
    for k, r in e.reglas.items():
        out.append(f"  {k} [{r.nivel}]")
        for c in r.comprobaciones:
            out.append(f"     {MARCA[c.nivel]:<12} {c.elemento}: {c.detalle}")
    for a in e.adaptaciones:
        out.append(f"  Adaptación A: {a}")
    return "\n".join(out)


def escribir_resultados(evals: list[Evaluacion], carpeta: Path) -> None:
    carpeta.mkdir(parents=True, exist_ok=True)
    with open(carpeta / "evaluacion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nucleo", "candidata", "R1", "R2", "R3", "recomendacion", "adaptacion"])
        for e in evals:
            w.writerow([e.id, e.nucleo, e.candidata, *(e.reglas[k].nivel for k in ("R1", "R2", "R3")),
                        e.recomendacion, " | ".join(e.adaptaciones)])
    with open(carpeta / "comprobaciones.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "regla", "elemento", "nivel", "detalle", "adaptacion"])
        for e in evals:
            for k, r in e.reglas.items():
                for c in r.comprobaciones:
                    w.writerow([e.id, k, c.elemento, c.nivel, c.detalle, c.adaptacion or ""])
    with open(carpeta / "reporte.md", "w", encoding="utf-8") as f:
        f.write("# Resultado del PSEPS\n\n")
        f.write("| # | Núcleo B → Candidata H | R1 | R2 | R3 | Recomendación |\n|---|---|---|---|---|---|\n")
        for e in evals:
            f.write(f"| {e.id} | {e.nucleo} → {e.candidata} | "
                    + " | ".join(MARCA[e.reglas[k].nivel] for k in ("R1", "R2", "R3"))
                    + f" | {e.recomendacion} |\n")
        f.write("\n## Detalle de las comprobaciones\n\n")
        for e in evals:
            f.write("```\n" + detalle(e) + "\n```\n\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Evalúa sustituciones de actividades con el PSEPS.")
    ap.add_argument("caso", type=Path, help="archivo JSON con el proceso núcleo y las candidatas")
    ap.add_argument("--detalle", action="store_true", help="muestra cada comprobación")
    ap.add_argument("--salida", type=Path, help="carpeta donde escribir evaluacion.csv, comprobaciones.csv y reporte.md")
    ap.add_argument("--candidata", help="evalúa solo una candidata (p. ej. S6)")
    args = ap.parse_args(argv)

    motor = PSEPS(json.loads(args.caso.read_text(encoding="utf-8")))
    evals = [motor.evaluar(args.candidata)] if args.candidata else motor.evaluar_todas()

    print(tabla(evals))
    if args.detalle:
        print()
        print("\n\n".join(detalle(e) for e in evals))
    if args.salida:
        escribir_resultados(evals, args.salida)
        print(f"\nResultados escritos en {args.salida}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
