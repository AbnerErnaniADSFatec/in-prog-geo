-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-join.html
--
-- Quais as áreas de terras indígenas no Estado do Tocantins?

SELECT ti.*
FROM terras_indigenas AS ti
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Intersects(uf.geom, ti.geom);

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_ AS SELECT ti.*
FROM terras_indigenas AS ti
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Intersects(uf.geom, ti.geom);
