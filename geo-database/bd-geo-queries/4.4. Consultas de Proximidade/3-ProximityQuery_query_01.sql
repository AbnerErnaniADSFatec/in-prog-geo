-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/proximity-query.html
--
-- Quais os municípios num raio de 2 graus da coordenada (−43.59,−20.32)?

SELECT *
FROM municipios
WHERE ST_DWithin(
	geom,
	ST_GeomFromText('POINT(-43.59 -20.32)', 4674),
	2.0
);

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_geom AS
SELECT 1 AS id,
'geometry query' AS name,
ST_GeomFromText('POINT(-43.59 -20.32)', 4674) AS geom;

CREATE OR REPLACE VIEW result_ AS SELECT *
FROM municipios
WHERE ST_DWithin(
	geom,
	ST_GeomFromText('POINT(-43.59 -20.32)', 4674),
	2.0
);
