# PSEPS: Principio de Sustitución de Elementos de Proceso Software

Prototipo y datos del artículo **«Contratos de proceso para evaluar la sustitución de actividades en procesos híbridos»** (Ingeniería de Procesos de Software, Universidad del Cauca, 2026).

**Autores:** Derly Tatiana Gómez Cuarán, Alejandro Otálora Tejada, Hennerson Estid Cobo Caicedo, Liz Yurany Castiblanco Sierra, Yeimy D. Joaquín Joaquín, Juan Felipe Ramírez Salazar.

## Qué hace

En un proceso híbrido se parte de un **proceso núcleo** y se reemplazan actividades por otras del otro enfoque (ágil o tradicional). El prototipo decide si una **actividad candidata H** puede reemplazar a una **actividad núcleo B** comparando sus contratos con tres reglas:

| Regla | Condición | Significado |
| --- | --- | --- |
| R1 · no exigir más | ∀p ∈ Pre(H) ∃q ∈ Pre(B): q ⊒ p | H no pide nada que B no recibía |
| R2 · no entregar menos | ∀q ∈ Post(B) ∃p ∈ Post(H): p ⊒ q | H entrega todo lo que entregaba B |
| R3 · conservar la invariante | Inv(H) ⇒ Inv(B) | H respeta el ciclo de vida y los principios de B |

`q ⊒ p` («q cubre a p») usa la escala de equivalencia del ICF del modelo CHAPLIN: cobertura ≥ 0.75 es **plena**, 0.5 es **parcial** (exige una adaptación A) y menos de 0.5 es **ninguna**. La equivalencia tiene dirección: una SRS cubre un Product Backlog con 0.5, pero un Product Backlog cubre una SRS con 0.

Cada regla es verdadera o falsa. La **recomendación** es:

- **Recomendable**: R1–R3 se cumplen con cobertura plena.
- **Recomendable con precaución**: R1–R3 se cumplen, pero alguna depende de una cobertura parcial; la adaptación A queda como obligación explícita.
- **No recomendable**: alguna regla es falsa.

## Uso

Requiere Python 3.8 o superior. No usa librerías externas.

```bash
# Tabla de resultados
python pseps.py datos/water-scrum-fall.json

# Cada comprobación, regla por regla
python pseps.py datos/water-scrum-fall.json --detalle

# Una sola candidata (el ejemplo de verificación del artículo)
python pseps.py datos/water-scrum-fall.json --candidata S6 --detalle

# Escribir resultados/evaluacion.csv, resultados/comprobaciones.csv y resultados/reporte.md
python pseps.py datos/water-scrum-fall.json --salida resultados

# Pruebas: comprueban que el prototipo reproduce la Tabla 2 del artículo
python -m unittest discover -s tests -v
```

Salida:

```
#   Núcleo B → Candidata H                                     R1  R2           R3           Recomendación
S1  Planificar Sprint → Planificar Sprint (Híbrida)            ✓   ✓            ✓            Recomendable
S2  Desarrollar Incremento → Desarrollar Incremento (Híbrida)  ✗   ✓            ✗            No recomendable
S3  Revisar Sprint → Revisar Sprint con Gate Formal            ✓   ✓            ✓            Recomendable
S4  Revisar Sprint → Pruebas de Aceptación Formal              ✗   ✗            ✗            No recomendable
S5  Elicitar Requisitos → Escribir Historias de Usuario        ✓   ✗            ✗            No recomendable
S6  Revisar Sprint → Revisión Formal de Requisitos             ✓   ✓ (parcial)  ✓ (parcial)  Recomendable con precaución
```

## Estructura

| Ruta | Contenido |
| --- | --- |
| `pseps.py` | Prototipo: modelo de contrato, cobertura dirigida, reglas R1–R3 y recomendación |
| `datos/water-scrum-fall.json` | Caso de validación: proceso núcleo Water-Scrum-Fall, 6 candidatas, artefactos, equivalencias e invariantes |
| `resultados/` | Salida del prototipo sobre el caso (`evaluacion.csv`, `comprobaciones.csv`, `reporte.md`) |
| `tests/test_pseps.py` | Pruebas: reproducción de la Tabla 2 y propiedades del principio |
| `figuras/` | Figura 1 del artículo (`.svg`, `.png`) y el script que la genera |

## Formato de los datos

El archivo JSON describe un caso completo:

- **`umbrales`**: cobertura mínima para considerarla plena (0.75) o parcial (0.5).
- **`artefactos`**: cada artefacto con sus atributos `firmado`, `trazable` y `congelado` (aprobado y no modificable).
- **`equivalencias`**: cobertura dirigida `de → a`, con lo que `falta`, la `adaptacion` que lo resuelve (si aplica) y su `justificacion`. Un artefacto siempre se cubre a sí mismo con 1.0; lo que no aparece cubre con 0.
- **`invariantes`**: conjuntos de propiedades. El contrato **tradicional** exige `secuencial`, `aprobado_con_firma` y `trazabilidad`. Los contratos **ágiles** traducen el Manifiesto Ágil y los pilares de Scrum: `iterativo`, `sin_documento_congelado` (respuesta al cambio), `participa_product_owner` (colaboración con el cliente), `ejecuta_equipo` (individuos e interacciones), `entrega_incremento` (software funcionando) y `actualiza_product_backlog` (inspección y adaptación).
- **`nucleo`**: actividades del proceso núcleo con `pre`, `post`, `ciclo`, `roles` y la `invariante` que deben conservar.
- **`candidatas`**: actividades de reemplazo con la actividad núcleo que `reemplaza`, `pre`, `opcionales` (no cuentan en el contrato), `post`, `ciclo` y `roles`.

Para evaluar una sustitución nueva, agreguen una entrada en `candidatas` (y en `artefactos` o `equivalencias` si hace falta) y vuelvan a ejecutar el prototipo.

## Alcance y limitaciones

- El contrato registra si un artefacto existe, no su calidad ni su estado.
- Las equivalencias se declaran a mano con la escala del ICF.
- El caso es un ejemplo ilustrativo construido sobre un proceso de la literatura; no incluye datos de práctica.
- Pre y Post corresponden a los *Mandatory Inputs* y *Outputs* de SPEM/EPF; la invariante y las equivalencias son campos que se agregan.
