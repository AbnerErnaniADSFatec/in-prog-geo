-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-join.html
--
-- Quantos focos de incêndio na vegetação foram detectados mensalmente
-- em Unidades de Conservação Estaduais do Estado do Tocantins ao longo de 2017?

SELECT Extract(month from focos.data_obser) AS mes,
uc.nome AS nome,
COUNT(*) AS total_focos
FROM focos
INNER JOIN uf ON uf.nome = 'TOCANTINS'
INNER JOIN unidades_conservacao AS uc ON uc.jurisdicao = 'Estadual'
WHERE ST_Intersects(uf.geom, uc.geom) AND ST_Contains(uc.geom, focos.geom) AND Extract(year from focos.data_obser) = 2017
GROUP BY mes, uc.id, uc.nome
ORDER BY mes ASC, total_focos DESC, nome ASC;
