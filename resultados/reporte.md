# Resultado del PSEPS

| # | Núcleo B → Candidata H | R1 | R2 | R3 | Recomendación |
|---|---|---|---|---|---|
| S1 | Planificar Sprint → Planificar Sprint (Híbrida) | ✓ | ✓ | ✓ | Recomendable |
| S2 | Desarrollar Incremento → Desarrollar Incremento (Híbrida) | ✗ | ✓ | ✗ | No recomendable |
| S3 | Revisar Sprint → Revisar Sprint con Gate Formal | ✓ | ✓ | ✓ | Recomendable |
| S4 | Revisar Sprint → Pruebas de Aceptación Formal | ✗ | ✗ | ✗ | No recomendable |
| S5 | Elicitar Requisitos → Escribir Historias de Usuario | ✓ | ✗ | ✗ | No recomendable |
| S6 | Revisar Sprint → Revisión Formal de Requisitos | ✓ | ✓ (parcial) | ✓ (parcial) | Recomendable con precaución |

## Detalle de las comprobaciones

```
S1: Planificar Sprint → Planificar Sprint (Híbrida)  ⇒  Recomendable
  R1 [plena]
     ✓            Product Backlog: Product Backlog ⊒ Product Backlog = 1
  R2 [plena]
     ✓            Sprint Backlog: Sprint Backlog ⊒ Sprint Backlog = 1
  R3 [plena]
     ✓            iterativo: ciclo iterativo
     ✓            sin_documento_congelado: ninguna entrada congelada
     ✓            participa_product_owner: participa el Product Owner
     ✓            ejecuta_equipo: la ejecuta el equipo
```

```
S2: Desarrollar Incremento → Desarrollar Incremento (Híbrida)  ⇒  No recomendable
  R1 [falla]
     ✓            Sprint Backlog: Sprint Backlog ⊒ Sprint Backlog = 1
     ✗            Documento de Diseño: ningún artefacto cubre Documento de Diseño: mejor Sprint Backlog ⊒ Documento de Diseño = 0 (falta decisiones de diseño aprobadas)
  R2 [plena]
     ✓            Incremento: Incremento ⊒ Incremento = 1
  R3 [falla]
     ✓            iterativo: ciclo iterativo
     ✗            sin_documento_congelado: entrada congelada: Documento de Diseño
     ✓            ejecuta_equipo: la ejecuta el equipo
     ✓            entrega_incremento: Incremento ⊒ Incremento = 1
```

```
S3: Revisar Sprint → Revisar Sprint con Gate Formal  ⇒  Recomendable
  R1 [plena]
     ✓            Incremento: Incremento ⊒ Incremento = 1
  R2 [plena]
     ✓            Product Backlog: Product Backlog ⊒ Product Backlog = 1
  R3 [plena]
     ✓            iterativo: ciclo iterativo
     ✓            sin_documento_congelado: ninguna entrada congelada
     ✓            participa_product_owner: participa el Product Owner
     ✓            ejecuta_equipo: la ejecuta el equipo
     ✓            actualiza_product_backlog: Product Backlog ⊒ Product Backlog = 1
```

```
S4: Revisar Sprint → Pruebas de Aceptación Formal  ⇒  No recomendable
  R1 [falla]
     ✗            Documento de Diseño: ningún artefacto cubre Documento de Diseño: mejor Incremento ⊒ Documento de Diseño = 0 (falta especificación de diseño)
  R2 [falla]
     ✗            Product Backlog: ningún artefacto cubre Product Backlog: mejor Acta ⊒ Product Backlog = 0 (falta requisitos priorizados)
  R3 [falla]
     ✗            iterativo: ciclo secuencial
     ✗            sin_documento_congelado: entrada congelada: Documento de Diseño
     ✗            participa_product_owner: sin Product Owner
     ✗            ejecuta_equipo: no la ejecuta el equipo
     ✗            actualiza_product_backlog: ningún artefacto cubre Product Backlog: mejor Acta ⊒ Product Backlog = 0 (falta requisitos priorizados)
```

```
S5: Elicitar Requisitos → Escribir Historias de Usuario  ⇒  No recomendable
  R1 [plena]
     ✓            Visión: Visión ⊒ Visión = 1
  R2 [falla]
     ✗            SRS: ningún artefacto cubre SRS: mejor Product Backlog ⊒ SRS = 0 (falta trazabilidad y firmas)
  R3 [falla]
     ✗            secuencial: ciclo iterativo
     ✗            aprobado_con_firma: sin firma: Product Backlog
     ✗            trazabilidad: sin trazabilidad: Product Backlog
```

```
S6: Revisar Sprint → Revisión Formal de Requisitos  ⇒  Recomendable con precaución
  R1 [plena]
     ✓            Incremento: Incremento ⊒ Incremento = 1
  R2 [parcial]
     ✓ (parcial)  Product Backlog: SRS ⊒ Product Backlog = 0.5 (falta prioridad y descomposición)
  R3 [parcial]
     ✓            iterativo: ciclo iterativo
     ✓            sin_documento_congelado: ninguna entrada congelada
     ✓            participa_product_owner: participa el Product Owner
     ✓            ejecuta_equipo: la ejecuta el equipo
     ✓ (parcial)  actualiza_product_backlog: SRS ⊒ Product Backlog = 0.5 (falta prioridad y descomposición)
  Adaptación A: El Product Owner prioriza y descompone la SRS en el Product Backlog
```

