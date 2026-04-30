# Base de conocimiento demo: Motocicletas Grupo Pellas Nicaragua

> Documento ficticio para demostracion de RAG y agentes de IA.  
> La informacion de modelos, precios, planes, sucursales y politicas es inventada para fines de capacitacion. No debe usarse como informacion comercial real.

## 1. Proposito del documento

Este documento contiene informacion simulada sobre una unidad de venta de motocicletas de Grupo Pellas Nicaragua. Su objetivo es servir como base de conocimiento para una demostracion de RAG y agentes de IA.

El bot debe usar este documento para responder preguntas frecuentes sobre:

- modelos de motocicletas disponibles;
- precios de referencia;
- opciones de financiamiento;
- requisitos para compra;
- garantia;
- mantenimiento;
- servicios postventa;
- ubicaciones de atencion;
- promociones ficticias;
- casos que deben escalarse a un asesor humano.

## 2. Reglas para el bot

El bot debe seguir estas reglas al responder:

1. Responder solo con informacion incluida en este documento.
2. Aclarar que los precios son referenciales de demostracion.
3. No aprobar creditos.
4. No confirmar disponibilidad final de inventario.
5. No prometer descuentos fuera de las promociones indicadas.
6. Escalar a un asesor humano cuando el cliente quiera comprar, financiar, reservar o negociar.
7. Pedir datos minimos cuando el cliente solicite seguimiento comercial.

Mensaje sugerido cuando no encuentre informacion:

> No tengo esa informacion en la base de conocimiento de esta demo. Puedo conectarte con un asesor para revisarlo.

## 3. Horario de atencion

El horario ficticio de atencion comercial es:

- Lunes a viernes: 8:00 a.m. a 5:30 p.m.
- Sabados: 8:00 a.m. a 12:30 p.m.
- Domingos: cerrado.

El horario ficticio de taller es:

- Lunes a viernes: 7:30 a.m. a 5:00 p.m.
- Sabados: 8:00 a.m. a 12:00 p.m.
- Domingos: cerrado.

## 4. Sucursales ficticias

### 4.1 Managua Centro

- Direccion ficticia: Avenida Principal, frente a Plaza Central, Managua.
- Servicios: ventas, financiamiento, repuestos, taller, entrega de motos.
- Telefono ficticio: 2255-1001.

### 4.2 Managua Carretera Sur

- Direccion ficticia: Km 8.5 Carretera Sur, Managua.
- Servicios: ventas, financiamiento, taller rapido, accesorios.
- Telefono ficticio: 2255-1002.

### 4.3 Leon

- Direccion ficticia: Entrada principal a Leon, contiguo a centro comercial local.
- Servicios: ventas, taller, repuestos basicos.
- Telefono ficticio: 2311-2001.

### 4.4 Chinandega

- Direccion ficticia: Rotonda comercial norte, Chinandega.
- Servicios: ventas, financiamiento, entrega programada.
- Telefono ficticio: 2341-3001.

### 4.5 Esteli

- Direccion ficticia: Avenida Central, modulo comercial 12, Esteli.
- Servicios: ventas, taller, repuestos.
- Telefono ficticio: 2713-4001.

## 5. Modelos disponibles para demo

### 5.1 Urbano 125

La Urbano 125 es una motocicleta ficticia pensada para traslados diarios en ciudad.

- Cilindraje: 125 cc.
- Tipo: urbana.
- Transmision: mecanica de 5 velocidades.
- Rendimiento estimado: hasta 115 km por galon en condiciones ideales.
- Tanque: 12 litros.
- Frenos: tambor delantero y trasero.
- Encendido: electrico y pedal.
- Colores disponibles: rojo, negro, azul.
- Precio de referencia demo: USD 1,350.

Ideal para:

- estudiantes;
- repartidores independientes;
- traslados diarios;
- primer comprador de motocicleta.

No recomendada para:

- viajes frecuentes de larga distancia;
- carga pesada;
- terrenos muy irregulares.

### 5.2 Trabajo 150 Cargo

La Trabajo 150 Cargo es una motocicleta ficticia enfocada en trabajo diario y carga liviana.

- Cilindraje: 150 cc.
- Tipo: utilitaria.
- Transmision: mecanica de 5 velocidades.
- Rendimiento estimado: hasta 100 km por galon en condiciones ideales.
- Tanque: 13 litros.
- Frenos: disco delantero y tambor trasero.
- Parrilla de carga: incluida.
- Capacidad de carga recomendada: hasta 120 kg incluyendo conductor y carga.
- Colores disponibles: blanco, negro, gris.
- Precio de referencia demo: USD 1,650.

Ideal para:

- negocios pequeños;
- mensajeria;
- entregas urbanas;
- vendedores de ruta;
- uso diario intensivo.

### 5.3 Sport 200

La Sport 200 es una motocicleta ficticia para usuarios que buscan mayor potencia y estilo deportivo.

- Cilindraje: 200 cc.
- Tipo: deportiva urbana.
- Transmision: mecanica de 6 velocidades.
- Rendimiento estimado: hasta 82 km por galon en condiciones ideales.
- Tanque: 14 litros.
- Frenos: disco delantero y trasero.
- Suspension: monoshock trasero.
- Tablero: digital.
- Colores disponibles: negro mate, rojo, gris metalico.
- Precio de referencia demo: USD 2,350.

Ideal para:

- usuarios con experiencia;
- recorridos mixtos ciudad-carretera;
- clientes que priorizan diseño y potencia.

No recomendada para:

- primer comprador sin experiencia;
- uso principal de carga.

### 5.4 Scooter City 110

La Scooter City 110 es una motocicleta automatica ficticia para movilidad urbana sencilla.

- Cilindraje: 110 cc.
- Tipo: scooter.
- Transmision: automatica CVT.
- Rendimiento estimado: hasta 120 km por galon en condiciones ideales.
- Tanque: 5.5 litros.
- Frenos: tambor delantero y trasero.
- Espacio bajo asiento: casco pequeño o articulos personales.
- Colores disponibles: blanco, celeste, gris.
- Precio de referencia demo: USD 1,480.

Ideal para:

- trayectos cortos;
- usuarios que prefieren manejo automatico;
- movilidad urbana;
- bajo consumo.

### 5.5 Adventure 250

La Adventure 250 es una motocicleta ficticia para clientes que combinan ciudad, carretera y caminos secundarios.

- Cilindraje: 250 cc.
- Tipo: doble proposito.
- Transmision: mecanica de 6 velocidades.
- Rendimiento estimado: hasta 70 km por galon en condiciones ideales.
- Tanque: 16 litros.
- Frenos: disco delantero y trasero.
- Suspension: recorrido extendido.
- Llantas: mixtas.
- Colores disponibles: verde, negro, naranja.
- Precio de referencia demo: USD 3,200.

Ideal para:

- viajes de fin de semana;
- clientes fuera de Managua;
- caminos secundarios;
- usuarios con experiencia.

No recomendada para:

- personas de baja experiencia que buscan una moto liviana;
- uso exclusivo en ciudad con trafico pesado.

### 5.6 Electrica E-Move

La Electrica E-Move es una motocicleta electrica ficticia para recorridos urbanos cortos.

- Tipo: electrica urbana.
- Autonomia estimada: hasta 70 km por carga.
- Tiempo de carga: 6 a 8 horas en toma convencional.
- Velocidad maxima estimada: 55 km/h.
- Bateria: litio removible.
- Frenos: disco delantero y tambor trasero.
- Colores disponibles: blanco, negro, verde.
- Precio de referencia demo: USD 2,100.

Ideal para:

- uso urbano;
- clientes con trayectos cortos;
- empresas que buscan movilidad de bajo costo operativo;
- clientes interesados en sostenibilidad.

No recomendada para:

- viajes largos;
- zonas sin facilidad de carga;
- uso de alta velocidad en carretera.

## 6. Comparacion rapida de modelos

| Modelo | Uso principal | Precio demo | Tipo de cliente |
|---|---:|---:|---|
| Urbano 125 | Ciudad y traslado diario | USD 1,350 | Primer comprador |
| Trabajo 150 Cargo | Trabajo y entregas | USD 1,650 | Negocios y reparto |
| Sport 200 | Ciudad-carretera y estilo | USD 2,350 | Usuario con experiencia |
| Scooter City 110 | Movilidad automatica urbana | USD 1,480 | Usuario urbano practico |
| Adventure 250 | Caminos mixtos y viajes | USD 3,200 | Usuario aventurero |
| Electrica E-Move | Movilidad urbana electrica | USD 2,100 | Cliente eco-urbano |

## 7. Recomendaciones por necesidad

### Si el cliente busca economia

Recomendar:

- Urbano 125.
- Scooter City 110.

Explicacion:

> Para economia y uso diario en ciudad, la Urbano 125 y la Scooter City 110 son las opciones mas accesibles y de menor consumo en esta demo.

### Si el cliente busca trabajo o reparto

Recomendar:

- Trabajo 150 Cargo.

Explicacion:

> Para trabajo, entregas o negocio pequeño, la Trabajo 150 Cargo es la opcion mas adecuada porque incluye parrilla de carga y esta pensada para uso diario intensivo.

### Si el cliente busca potencia

Recomendar:

- Sport 200.
- Adventure 250.

Explicacion:

> Para mayor potencia, la Sport 200 funciona mejor en ciudad-carretera, mientras que la Adventure 250 es mas adecuada para caminos mixtos y viajes.

### Si el cliente busca manejo automatico

Recomendar:

- Scooter City 110.

Explicacion:

> Si el cliente prefiere no usar cambios manuales, la Scooter City 110 es la opcion automatica de esta base de conocimiento.

### Si el cliente busca una opcion electrica

Recomendar:

- Electrica E-Move.

Explicacion:

> Para movilidad urbana electrica, la E-Move ofrece una autonomia estimada de hasta 70 km por carga y esta pensada para trayectos cortos.

## 8. Financiamiento ficticio

Grupo Pellas Motos Demo ofrece planes de financiamiento simulados para la capacitacion.

### 8.1 Requisitos generales

Para solicitar financiamiento, el cliente debe presentar:

- cedula de identidad vigente;
- comprobante de ingresos;
- recibo de servicio basico;
- referencias personales;
- prima inicial;
- autorizacion para revision crediticia.

### 8.2 Prima minima de referencia

La prima minima ficticia es:

- 15% para Urbano 125 y Scooter City 110.
- 20% para Trabajo 150 Cargo y Sport 200.
- 25% para Adventure 250 y Electrica E-Move.

### 8.3 Plazos disponibles

Los plazos ficticios disponibles son:

- 12 meses;
- 18 meses;
- 24 meses;
- 36 meses.

### 8.4 Ejemplo de cuotas referenciales

Las cuotas son ejemplos ficticios para demo. No incluyen seguros, gastos administrativos ni variaciones por perfil crediticio.

| Modelo | Precio demo | Prima demo | Plazo | Cuota mensual demo |
|---|---:|---:|---:|---:|
| Urbano 125 | USD 1,350 | USD 203 | 24 meses | USD 58 |
| Trabajo 150 Cargo | USD 1,650 | USD 330 | 24 meses | USD 67 |
| Sport 200 | USD 2,350 | USD 470 | 36 meses | USD 68 |
| Scooter City 110 | USD 1,480 | USD 222 | 24 meses | USD 63 |
| Adventure 250 | USD 3,200 | USD 800 | 36 meses | USD 88 |
| Electrica E-Move | USD 2,100 | USD 525 | 36 meses | USD 58 |

### 8.5 Reglas para preguntas de credito

El bot puede explicar requisitos y ejemplos de cuotas, pero no debe aprobar credito.

Si el cliente pregunta:

```txt
Me aprueban el credito?
```

El bot debe responder:

> No puedo aprobar creditos desde la base de conocimiento. Puedo explicarte los requisitos generales y conectarte con un asesor para revisar tu caso.

Si el cliente pregunta:

```txt
Cuanto me queda la cuota exacta?
```

El bot debe responder:

> Las cuotas de esta demo son referenciales. Para una cuota exacta se requiere revisar prima, plazo, perfil crediticio y condiciones vigentes con un asesor.

## 9. Promociones ficticias

### 9.1 Promo Mes del Trabajo

Promocion ficticia valida para demo:

- Aplica a Trabajo 150 Cargo.
- Incluye casco basico y primer mantenimiento gratis.
- No aplica con otros descuentos.
- Vigencia ficticia: 1 al 31 de mayo de 2026.

### 9.2 Promo Primer Comprador

Promocion ficticia valida para demo:

- Aplica a Urbano 125 y Scooter City 110.
- Incluye matricula con descuento del 50%.
- Requiere financiamiento aprobado o pago de contado.
- Vigencia ficticia: 1 al 30 de junio de 2026.

### 9.3 Promo Electrica Urbana

Promocion ficticia valida para demo:

- Aplica a Electrica E-Move.
- Incluye cargador adicional.
- Incluye revision electrica gratuita a los 60 dias.
- Vigencia ficticia: 15 de abril al 15 de julio de 2026.

## 10. Garantia ficticia

La garantia ficticia de las motocicletas es:

- 12 meses o 12,000 km para motos de combustion.
- 18 meses o 15,000 km para Electrica E-Move.
- La garantia cubre defectos de fabricacion.
- La garantia no cubre desgaste normal, accidentes, modificaciones no autorizadas o falta de mantenimiento.

Para conservar la garantia, el cliente debe:

- realizar mantenimientos en taller autorizado;
- respetar los kilometrajes de servicio;
- usar repuestos recomendados;
- conservar comprobantes de mantenimiento.

## 11. Mantenimiento

### 11.1 Primer mantenimiento

El primer mantenimiento debe realizarse a los:

- 500 km o 30 dias, lo que ocurra primero.

Incluye:

- revision general;
- ajuste de cadena;
- revision de frenos;
- revision de luces;
- cambio de aceite para modelos de combustion;
- inspeccion de bateria para Electrica E-Move.

### 11.2 Mantenimientos posteriores

Los mantenimientos posteriores se recomiendan cada:

- 2,000 km para Urbano 125, Trabajo 150 Cargo, Sport 200 y Scooter City 110.
- 2,500 km para Adventure 250.
- 3,000 km para Electrica E-Move.

### 11.3 Costos de mantenimiento ficticios

| Modelo | Primer mantenimiento | Mantenimiento regular |
|---|---:|---:|
| Urbano 125 | USD 25 | USD 35 |
| Trabajo 150 Cargo | USD 30 | USD 40 |
| Sport 200 | USD 40 | USD 55 |
| Scooter City 110 | USD 25 | USD 35 |
| Adventure 250 | USD 55 | USD 75 |
| Electrica E-Move | USD 35 | USD 45 |

## 12. Repuestos y accesorios

Los repuestos ficticios disponibles incluyen:

- aceite;
- filtros;
- bujias;
- pastillas de freno;
- llantas;
- cadenas;
- baterias;
- espejos;
- focos;
- cables;
- cargador para Electrica E-Move.

Los accesorios ficticios disponibles incluyen:

- cascos;
- guantes;
- chaquetas;
- baules;
- parrillas;
- impermeables;
- candados;
- soportes para celular.

## 13. Proceso de compra

### 13.1 Compra de contado

Pasos:

1. Cliente elige modelo.
2. Asesor confirma disponibilidad.
3. Cliente presenta cedula.
4. Cliente realiza pago.
5. Se prepara factura y documentos.
6. Se programa entrega.

### 13.2 Compra financiada

Pasos:

1. Cliente elige modelo.
2. Cliente presenta documentos.
3. Se realiza analisis crediticio.
4. Se confirma prima, plazo y cuota.
5. Cliente firma contrato.
6. Se programa entrega.

### 13.3 Reserva

La reserva ficticia requiere:

- nombre completo;
- telefono;
- modelo de interes;
- sucursal preferida;
- monto de reserva de USD 50.

La reserva ficticia dura 5 dias habiles. Si el cliente no completa la compra, la reserva puede liberarse.

El bot no debe confirmar reservas. Debe escalar a asesor humano.

## 14. Datos que debe pedir el bot para escalar a ventas

Si el cliente quiere comprar, financiar o reservar, el bot debe pedir:

- nombre completo;
- numero de telefono;
- ciudad;
- modelo de interes;
- si desea contado o financiamiento;
- sucursal preferida;
- mejor horario para contacto.

Mensaje sugerido:

> Para conectarte con un asesor, por favor comparteme tu nombre, telefono, ciudad, modelo de interes y si buscas pago de contado o financiamiento.

## 15. Preguntas frecuentes

### 15.1 Cual es la moto mas economica?

La moto mas economica de esta demo es la Urbano 125, con precio de referencia de USD 1,350.

### 15.2 Cual moto recomiendan para reparto?

Para reparto se recomienda la Trabajo 150 Cargo, porque esta pensada para uso diario intensivo e incluye parrilla de carga.

### 15.3 Tienen moto automatica?

Si. La Scooter City 110 es la opcion automatica de esta base de conocimiento.

### 15.4 Tienen moto electrica?

Si. La Electrica E-Move es la opcion electrica ficticia, con autonomia estimada de hasta 70 km por carga.

### 15.5 Puedo comprar con financiamiento?

Si, en esta demo existen planes de financiamiento con prima minima desde 15%, dependiendo del modelo. La aprobacion final debe revisarla un asesor.

### 15.6 Cual es la garantia?

La garantia ficticia es de 12 meses o 12,000 km para motos de combustion, y 18 meses o 15,000 km para la Electrica E-Move.

### 15.7 Cual moto sirve para caminos malos?

La Adventure 250 es la opcion mas adecuada para caminos mixtos y secundarios. No se debe presentar como moto para condiciones extremas, sino para uso mixto.

### 15.8 La cuota mensual es exacta?

No. Las cuotas de este documento son referenciales para demo. La cuota exacta depende de prima, plazo, perfil crediticio y condiciones vigentes.

### 15.9 Puedo reservar una moto?

Si existe un proceso ficticio de reserva, pero el bot no debe confirmar reservas. Debe conectar al cliente con un asesor.

### 15.10 Donde estan ubicados?

Las sucursales ficticias de esta demo estan en Managua Centro, Managua Carretera Sur, Leon, Chinandega y Esteli.

## 16. Casos que deben escalarse

El bot debe escalar a un asesor humano cuando el cliente:

- quiere comprar;
- quiere financiar;
- quiere reservar;
- pide descuento especial;
- pide disponibilidad exacta;
- pregunta por aprobacion crediticia;
- reporta problema mecanico;
- quiere garantia;
- pide hablar con una persona;
- presenta queja;
- pregunta por informacion no incluida en este documento.

## 17. Respuestas ejemplo para el bot

### 17.1 Cliente pregunta por modelo economico

Pregunta:

```txt
Estoy buscando una moto barata para ir al trabajo, cual me recomiendan?
```

Respuesta esperada:

> Para uso diario y economia, la opcion mas accesible de esta demo es la Urbano 125, con precio referencial de USD 1,350. Tambien podria interesarte la Scooter City 110 si prefieres manejo automatico. Los precios son de demostracion y deben confirmarse con un asesor.

### 17.2 Cliente pregunta por reparto

Pregunta:

```txt
Necesito una moto para entregas, cual sirve?
```

Respuesta esperada:

> Para entregas o trabajo diario, la opcion recomendada es la Trabajo 150 Cargo. Tiene motor de 150 cc, parrilla de carga incluida y esta pensada para uso utilitario. Su precio demo es USD 1,650.

### 17.3 Cliente pregunta por credito

Pregunta:

```txt
Me pueden aprobar una moto con prima baja?
```

Respuesta esperada:

> Puedo explicarte los requisitos generales, pero no puedo aprobar creditos. En esta demo, la prima minima empieza desde 15% para algunos modelos. Para revisar tu caso, puedo conectarte con un asesor.

### 17.4 Cliente pregunta por disponibilidad exacta

Pregunta:

```txt
Tienen la Sport 200 negra lista para entrega hoy?
```

Respuesta esperada:

> No puedo confirmar disponibilidad exacta desde esta base de conocimiento. La Sport 200 aparece en esta demo con colores negro mate, rojo y gris metalico, pero la disponibilidad final debe confirmarla un asesor.

### 17.5 Cliente pregunta por mantenimiento

Pregunta:

```txt
Cuando tengo que hacer el primer mantenimiento?
```

Respuesta esperada:

> El primer mantenimiento debe realizarse a los 500 km o 30 dias, lo que ocurra primero. Incluye revision general, ajuste de cadena, revision de frenos, revision de luces y cambio de aceite para modelos de combustion.

## 18. Informacion no incluida

Este documento no contiene:

- inventario real;
- aprobacion crediticia real;
- politicas comerciales reales;
- precios comerciales vigentes;
- tasas de interes reales;
- informacion legal;
- datos reales de clientes;
- disponibilidad por sucursal en tiempo real.

Si el cliente pregunta por cualquiera de estos puntos, el bot debe escalar.

## 19. Mensaje final para clientes interesados

Mensaje recomendado:

> Gracias por tu interes. Esta informacion pertenece a una demo de capacitacion. Si deseas avanzar con compra, financiamiento o reserva, puedo conectarte con un asesor para confirmar precio, disponibilidad y condiciones.

## 20. Nota para la presentacion

Este documento es util para demostrar la diferencia entre:

```txt
Pregunta sobre conocimiento documental
-> RAG puede responder.

Pregunta sobre estado real, disponibilidad o credito
-> se necesita tool, API o asesor humano.
```

Ejemplos para la demo:

1. "Cual es la moto mas economica?"
2. "Que moto sirve para reparto?"
3. "Que incluye la garantia?"
4. "Puedo reservar una Sport 200 negra para hoy?"
5. "Me aprueban el credito si gano 600 dolares?"

Las primeras tres preguntas pueden responderse con RAG. Las ultimas dos deben escalarse porque requieren informacion o decisiones fuera de la base documental.
