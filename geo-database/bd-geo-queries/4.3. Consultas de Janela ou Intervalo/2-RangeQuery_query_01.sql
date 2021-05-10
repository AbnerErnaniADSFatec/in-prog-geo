-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/window-query.html
--
-- Quais UF possuem geometrias com interação com
-- o retângulo de coordenadas (−54.23,−21.49) e (−43.89,−12.90)?

SELECT *
FROM uf
WHERE ST_Intersects(
	geom,
    ST_MakeEnvelope(-54.23, -21.49, -43.89, -12.90, 4674)
);

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_geom AS
SELECT 1 AS id,
'geometry query' AS name,
ST_MakeEnvelope(-54.23, -21.49, -43.89, -12.90, 4674) AS geom;

CREATE OR REPLACE VIEW result_ AS SELECT *
FROM uf
WHERE ST_Intersects(
	geom,
    ST_MakeEnvelope(-54.23, -21.49, -43.89, -12.90, 4674)
);
