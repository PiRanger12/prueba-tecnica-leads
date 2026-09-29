# Prueba Técnica: Pipeline e Integración de Leads Comerciales

Bienvenido a la prueba técnica de Atlas Desarrollos.
Esta evaluación mide tus habilidades prácticas en análisis y limpieza de datos, modelado SQL, integración de APIs, diseño de soluciones con IA y flujo de trabajo en Git.

- Tiempo límite: 1:30 hrs (1 hora y 30 minutos).
- Uso de IA: Se permite el uso de herramientas de IA generativa (ChatGPT, Claude, Gemini, Copilot, Cursor, etc.) únicamente como asistente para la implementación de código en Python.
- Regla estricta sobre exclusión de IA: Queda estrictamente prohibido el uso de IA para:
  1. Escribir las consultas SQL en sql/queries.sql (deben resolverse exclusivamente con tu propio razonamiento y conocimiento técnico).
  2. Responder las preguntas conceptuales de API y arquitectura de IA en este README.
  3. Durante la sesión de defensa verbal en vivo.
- Entrega del hilo de IA: Es obligatorio adjuntar el enlace público compartido o la exportación del hilo de conversación continuo utilizado durante la prueba. No debes reiniciar el chat ni crear conversaciones paralelas; se auditará que no hayas consultado los queries SQL ni la teoría, y se evaluará cómo estructuras tus prompts y refinas el contexto en las partes permitidas.
- Evaluación: Al finalizar, defenderás tu solución en una sesión técnica en vivo (10 a 15 minutos).

---

## Estructura del Proyecto

```text
├── data/
│   ├── leads.csv
│   └── desarrollos.csv
├── src/
│   ├── api.py
│   └── procesar_leads.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── README.md
└── requirements.txt
```

---

## Flujo de Trabajo en Git (Estrategia Dev a Sandbox para Múltiples Candidatos)

Dado que la prueba se aplica de forma concurrente a varios candidatos en el mismo repositorio, es indispensable evitar colisiones en las ramas. Cada candidato debe trabajar con un sufijo único compuesto por su nombre y apellido completo (ejemplo: carlos-perez):

1. Crea tu rama sandbox a partir de main con la nomenclatura: sandbox/<nombre-apellido>
2. A partir de tu rama sandbox, crea tu rama de desarrollo: dev/<nombre-apellido>
3. Trabaja y realiza commits incrementales y descriptivos exclusivamente sobre tu rama dev/<nombre-apellido>.
4. Al concluir la prueba, integra tu trabajo realizando el merge de dev/<nombre-apellido> hacia sandbox/<nombre-apellido>.
5. Publica ambas ramas en el repositorio remoto.
6. El entregable oficial a evaluar será tu rama sandbox/<nombre-apellido> conteniendo el merge correspondiente.

---

## Entorno de Pruebas SQL

Para crear las tablas, insertar datos y validar tus consultas puedes utilizar el siguiente cliente de base de datos en línea (no requiere instalación):

https://onecompiler.com/mysql

Copia tu DDL de schema.sql en el editor, ejecuta las sentencias para crear las tablas, inserta algunos registros de prueba basados en data/leads.csv y data/desarrollos.csv, y luego ejecuta tus consultas de queries.sql para verificar que devuelvan los resultados esperados antes de hacer commit.

---

## Retos a Resolver

### 1. Python y Calidad de Datos (20%)
En src/procesar_leads.py:
- Carga data/leads.csv.
- Implementa la limpieza básica de datos:
  - Elimina registros duplicados considerando el campo email.
  - Descarta registros con email vacío.
  - Normaliza la columna estatus a valores únicos canónicos (NUEVO, CONTACTADO, EN_SEGUIMIENTO, CONVERTIDO, PERDIDO).
  - Trata los valores nulos en la columna presupuesto asignando 0 o el valor promedio.
- Exporta el dataset resultante en data/leads_limpios.csv listo para base de datos.
- Genera un resumen en consola que reporte:
  - Total de prospectos limpios.
  - Conteo de prospectos por origen.
  - Conteo de prospectos por estatus normalizado.

### 2. SQL y Modelado de Datos (30%)
Nota: Esta sección es fundamental. Queda estrictamente prohibido el uso de IA para escribir las consultas en queries.sql.

En el directorio sql/:
- schema.sql: Diseña el modelo relacional para las entidades desarrollos y leads. Define tipos de datos adecuados, llaves primarias, llaves foráneas e índices recomendados.
- queries.sql: Escribe con criterio propio las siguientes 4 consultas:
  - Q1: Leads activos (NUEVO, CONTACTADO, EN_SEGUIMIENTO) registrados durante los últimos 30 días.
  - Q2: Cantidad de leads agrupados por origen, ordenados descendentemente.
  - Q3: Detalle mediante JOIN que presente: nombre del prospecto, desarrollo, ciudad y presupuesto.
  - Q4: Resumen por desarrollo: conteo total de prospectos y presupuesto promedio.

### 3. Consumo de API (15%)
En src/procesar_leads.py:
- Completa la función de envío para mandar una muestra de prospectos a POST http://127.0.0.1:8000/api/leads incluyendo el encabezado Authorization: Bearer atlas-token-2026.
- Explica con tu propio criterio (en este README o en comentarios de código; sin IA) cómo mitigarías en producción los siguientes dos escenarios HTTP:
  - HTTP 401 Unauthorized (Token vencido o inválido): 
    Pues lo que yo realizare el la creacion de una variable que contenga el token (headers donde introducto el token en el desarrollo lo use como una variable dentro de procesar_leads para el envio de las pruebas pero lo mas recomendable y lo que uso es la creacion del token en un archivo .env y lo ignoras en el .gitignore para que no se filtre y pueda con llevar a un problema de filtracion de datos, una vez teniendo esta variable en el archivo .env asemos el llamado del mismo dentro de nuestra apliacacion asi cada vez que se recargue la pagina del desarrollador este token se valide) 
  - HTTP 429 Too Many Requests (Límite de peticiones alcanzado):
    aumentando el limite de peticiones que puede hacer un desarrollador por sierto tiempo a vien si se cuenta con varios servidores que cuentan el proyecto podemos hacer que distrubuya las paticiones entre los servidores para no saturar a uno solo

### 4. Arquitectura de IA y Herramientas (15%)
Nota: Redacta tus respuestas con criterio propio. Queda prohibido el uso de IA para esta sección.

El área comercial requiere procesar el campo comentarios de los prospectos para extraer intención de compra y prioridad.

Responde de forma clara y breve:
1. ¿Qué diferencia práctica hay entre enviar una instrucción simple a ChatGPT y configurar un Agente de IA con herramientas (Tools) que interactúe con el CRM o la base de datos?
    la diferencia practica consiste en que el asistente de ia con una instruccion simple para la realizacion de alguna funcion o instrucion, en lo particuar e notado el contexto a randes razgon del agente el limitado por que con esa simple instruccion si no la contextualiza no puede realizar acciones mas completajas como es el caso de algunas funcioens que no conoce las variables que se usan en el desarrollo pueden cambiar de nombre y al la hora de ejecutart se tiene que ajustar a los parametros de dasarrollo. el caso del agente que esta integrado en el CRM este conoce todos los contexto del mismo lo que permite ajustar a los parametros del mismo
2. ¿Cómo conectarías a un agente para que consulte datos en una base de datos SQL garantizando seguridad y evitando riesgos de modificación o borrado accidental de información?
    lo que podemos crear es un user en la base de datos esclusivo en la base de datos para el agente con limitaciones de solo creacion para evitar que pueda evitar filtar informacio o borar informacion y implementar try-catch para validar las acciones les mismo por parte de los desarrolladores. 
---

## Criterios de Evaluación (100 Puntos)

- 30% SQL y modelado relacional (evaluado sin uso de IA).
- 20% Python, limpieza de datos y resumen ejecutivo.
- 15% Consumo de API y conceptos de mitigación HTTP.
- 15% Preguntas conceptuales de IA (sin uso de IA).
- 10% Flujo Git: creación de ramas individualizadas, calidad de commits y merge a sandbox.
- 10% Defensa técnica en vivo y auditoría del hilo de interacción con IA.

---

## Registro del Hilo de IA

Agrega aquí el enlace público o ruta del archivo de tu conversación continua con la IA utilizada durante la prueba:

- Nombre del candidato:
      Jesús Jiménez de Santiago
- Herramienta utilizada (ChatGPT, Claude, Cursor, Copilot, etc.):
      claude
- Enlace compartido al hilo del chat o ruta del archivo exportado: 
      https://claude.ai/share/373fb06b-dd80-48bb-9854-0a064e34af88
