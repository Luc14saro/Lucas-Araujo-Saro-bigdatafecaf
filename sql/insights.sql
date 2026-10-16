-- Consultas auxiliares para extrair os insights citados no README e no PDF.
-- Rode com:  docker exec -i postgres-iot psql -U iot_user -d iot_db < sql/insights.sql

-- Visão geral da base
SELECT COUNT(*) AS total_leituras,
       MIN(noted_date) AS primeira_leitura,
       MAX(noted_date) AS ultima_leitura,
       ROUND(AVG(temperature), 2) AS temp_media,
       MIN(temperature) AS temp_min,
       MAX(temperature) AS temp_max
FROM temperature_readings;

-- Interno x externo
SELECT * FROM avg_temp_por_dispositivo;

-- Horários com mais e menos leituras
SELECT * FROM leituras_por_hora ORDER BY contagem DESC LIMIT 3;
SELECT * FROM leituras_por_hora ORDER BY contagem ASC  LIMIT 3;

-- Dias com maior amplitude térmica
SELECT data, temp_max, temp_min, temp_max - temp_min AS amplitude
FROM temp_max_min_por_dia
ORDER BY amplitude DESC
LIMIT 5;

-- Temperatura média por hora do dia (padrão diário)
SELECT EXTRACT(HOUR FROM noted_date)::int AS hora,
       ROUND(AVG(temperature), 2) AS temp_media
FROM temperature_readings
GROUP BY 1
ORDER BY 1;
