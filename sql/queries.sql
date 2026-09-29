-- =============================================================
-- SECCIÓN 2.2: Consultas SQL
-- REGLA ESTRICTA: Las consultas deben ser escritas con criterio
-- y conocimiento propio. Queda prohibido el uso de IA en esta sección.
-- =============================================================

-- Consulta 1 (Filtro básico de fecha y estado):
-- Obtén todos los leads activos (NUEVO, CONTACTADO, EN_SEGUIMIENTO) registrados en los últimos 30 días.
select * from leads where estatus in ('NUEVO','CONTACTADO','EN_SEGUIMIENTO') and fecha_registro >= DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Consulta 2 (Agregación y ordenamiento):
-- Obtén la cantidad de leads agrupados por origen, ordenados de mayor a menor.
select 
    origen, count(*) as cantidad_leads 
from leads 
group by origen 
order by cantidad_leads desc;


-- Consulta 3 (JOIN relacional):
-- Obtén el nombre del prospecto, nombre del desarrollo, ciudad y presupuesto.
select 
    l.nombre as nombre_prospecto,
    d.nombre as nombre_desarrollo,
    d.ciudad,
    l.presupuesto
from leads l
join desarrollos d on l.desarrollo_id = d.id;

-- Consulta 4 (Métricas de Negocio):
-- Obtén por desarrollo: total de prospectos y presupuesto promedio.
select 
    d.nombre as nombre_desarrollo,
    count(l.id) as total_prospectos,
    avg(l.presupuesto) as promedio_presupuesto
from leads l
join desarrollos d on l.desarrollo_id = d.id