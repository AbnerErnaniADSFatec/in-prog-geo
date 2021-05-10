-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/overlay.html
--
-- Quais os tipos de solo do Estado do Tocantins?

SELECT pedologia.gid AS gid, pedologia.ordem AS ordem, ST_Intersection(pedologia.geom, uf.geom) AS geom
FROM pedologia
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Intersects(uf.geom, pedologia.geom);

-- PostgreSQL and QGIS

CREATE VIEW result_ AS SELECT pedologia.gid AS gid,
pedologia.ordem AS ordem,
ST_Intersection(pedologia.geom, uf.geom) AS geom
FROM pedologia
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Intersects(uf.geom, pedologia.geom);
