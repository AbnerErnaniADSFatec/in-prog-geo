-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/point-query.html
--
-- Qual UF encontra-se na localização de longitude −44.29 e latitude −18.61?

SELECT *
FROM uf
WHERE ST_Contains(
    geom,
    ST_GeomFromText( 'POINT(-44.29 -18.61)', 4674 )
);

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_geom AS
SELECT 1 AS id,
'geometry query' AS name,
ST_GeomFromText('POINT(-44.29 -18.61)', 4674) AS geom;

CREATE OR REPLACE VIEW result_ AS SELECT *
FROM uf
WHERE ST_Contains(
    geom,
    ST_GeomFromText('POINT(-44.29 -18.61)', 4674)
);
