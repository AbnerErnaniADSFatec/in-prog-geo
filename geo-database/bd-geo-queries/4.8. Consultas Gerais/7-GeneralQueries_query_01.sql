-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/general-queries.html
--
-- Qual a porcentagem de cada bioma em relação à extensão do Brasil?

WITH area_biomas AS (
	SELECT biomas.bioma, ST_Area(biomas.geom) AS area FROM biomas
), total AS (
	SELECT SUM(biomas.area) AS area_total
	FROM (
		SELECT ST_Area(biomas.geom) AS area FROM biomas
	) AS biomas
) SELECT area_biomas.bioma,
ROUND(CAST(float8 (area_biomas.area/total.area_total) * 100 as numeric), 2) || '%' AS porcentagem
FROM area_biomas, total;

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_ AS WITH area_biomas AS (
	SELECT biomas.bioma, ST_Area(biomas.geom) AS area, biomas.geom FROM biomas
), total AS (
	SELECT SUM(biomas.area) AS area_total
	FROM (
		SELECT ST_Area(biomas.geom) AS area FROM biomas
	) AS biomas
) SELECT area_biomas.bioma,
ROUND(CAST(float8 (area_biomas.area/total.area_total) * 100 as numeric), 2) || '%' AS porcentagem,
area_biomas.geom
FROM area_biomas, total;
