-- ============================================================
-- Views SQL do pipeline de temperatura IoT
-- Tabela de origem: temperature_readings (criada por src/ingest.py)
-- Executado automaticamente por src/ingest.py ao final da carga.
-- ============================================================

-- View 1: temperatura média por dispositivo (e por local: interno/externo)
-- Propósito: comparar o comportamento térmico de cada sensor e
-- evidenciar a diferença entre medições internas (In) e externas (Out).
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    location,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    COUNT(*)                            AS total_leituras
FROM temperature_readings
GROUP BY device_id, location;

-- View 2: quantidade de leituras por hora do dia (0 a 23)
-- Propósito: entender em quais horários os dispositivos mais enviam
-- dados (carga do sistema, lacunas de coleta, padrões de uso).
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date)::int AS hora,
    COUNT(*)                           AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_date)
ORDER BY hora;

-- View 3: temperaturas máxima e mínima por dia
-- Propósito: acompanhar a amplitude térmica diária e identificar
-- dias com picos ou quedas anormais (possíveis alertas).
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    noted_date::date          AS data,
    MAX(temperature)          AS temp_max,
    MIN(temperature)          AS temp_min
FROM temperature_readings
GROUP BY noted_date::date
ORDER BY data;
