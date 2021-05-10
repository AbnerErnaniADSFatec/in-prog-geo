-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/overlay.html
--
-- Recuperar os trechos de rodovia no Estado do Tocantins com o tipo de revestimento “Pavimentado”?

SELECT trechos.codtrechor, trechos.revestimen, trechos.geom
FROM trechos_rodoviarios AS trechos
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Contains(uf.geom, trechos.geom) AND ST_Intersects(uf.geom, trechos.geom)
AND trechos.revestimen = 'Pavimentado';

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_ AS SELECT trechos.gid, trechos.codtrechor, trechos.revestimen, trechos.geom
FROM trechos_rodoviarios AS trechos
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Contains(uf.geom, trechos.geom) AND ST_Intersects(uf.geom, trechos.geom)
AND trechos.revestimen = 'Pavimentado';
