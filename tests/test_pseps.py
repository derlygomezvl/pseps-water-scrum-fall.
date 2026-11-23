"""Pruebas del prototipo PSEPS sobre el caso Water-Scrum-Fall.

Ejecutar desde la raíz del repositorio:  python -m unittest discover -s tests -v
"""
import copy
import json
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from pseps import PSEPS, PLENA, PARCIAL, FALLA, RECOMENDABLE, PRECAUCION, NO_RECOMENDABLE  # noqa: E402

CASO = json.loads((RAIZ / "datos" / "water-scrum-fall.json").read_text(encoding="utf-8"))

# Resultado esperado: el de la Tabla 2 del artículo.
ESPERADO = {
    "S1": (PLENA, PLENA, PLENA, RECOMENDABLE),
    "S2": (FALLA, PLENA, FALLA, NO_RECOMENDABLE),
    "S3": (PLENA, PLENA, PLENA, RECOMENDABLE),
    "S4": (FALLA, FALLA, FALLA, NO_RECOMENDABLE),
    "S5": (PLENA, FALLA, FALLA, NO_RECOMENDABLE),
    "S6": (PLENA, PARCIAL, PARCIAL, PRECAUCION),
}


class TablaDelArticulo(unittest.TestCase):
    def setUp(self):
        self.motor = PSEPS(CASO)

    def test_reproduce_la_tabla(self):
        for c_id, (r1, r2, r3, rec) in ESPERADO.items():
            with self.subTest(candidata=c_id):
                e = self.motor.evaluar(c_id)
                self.assertEqual((e.reglas["R1"].nivel, e.reglas["R2"].nivel, e.reglas["R3"].nivel), (r1, r2, r3))
                self.assertEqual(e.recomendacion, rec)

    def test_s6_exige_la_adaptacion(self):
        e = self.motor.evaluar("S6")
        self.assertEqual(e.adaptaciones, ["El Product Owner prioriza y descompone la SRS en el Product Backlog"])

    def test_solo_los_casos_amarillos_tienen_adaptacion(self):
        for c_id in ESPERADO:
            e = self.motor.evaluar(c_id)
            self.assertEqual(bool(e.adaptaciones), e.recomendacion == PRECAUCION, c_id)


class PropiedadesDelPrincipio(unittest.TestCase):
    def test_las_entradas_opcionales_no_cuentan(self):
        # S1 recibe la SRS como opcional; si fuera obligatoria, R1 fallaría.
        caso = copy.deepcopy(CASO)
        caso["candidatas"]["S1"]["pre"].append("SRS")
        e = PSEPS(caso).evaluar("S1")
        self.assertEqual(e.reglas["R1"].nivel, FALLA)

    def test_entregar_mas_esta_permitido(self):
        # S3 entrega además el Acta del sprint y sigue siendo recomendable.
        e = PSEPS(CASO).evaluar("S3")
        self.assertEqual(e.recomendacion, RECOMENDABLE)

    def test_la_equivalencia_tiene_direccion(self):
        motor = PSEPS(CASO)
        self.assertEqual(motor.cobertura("SRS", "Product Backlog")[0], 0.5)
        self.assertEqual(motor.cobertura("Product Backlog", "SRS")[0], 0.0)

    def test_artefacto_desconocido_se_rechaza(self):
        caso = copy.deepcopy(CASO)
        caso["candidatas"]["S1"]["pre"] = ["Algo que no existe"]
        with self.assertRaises(ValueError):
            PSEPS(caso)


if __name__ == "__main__":
    unittest.main()
