-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-aggregation.html
--
-- Gerar o mapa de Regiões do Brasil a partir do mapa de Unidades Federativas.

SELECT uf.regiao, ST_Union(uf.geom)
FROM uf GROUP BY uf.regiao;

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_ AS SELECT uf.regiao, ST_Union(uf.geom)
FROM uf GROUP BY uf.regiao;
