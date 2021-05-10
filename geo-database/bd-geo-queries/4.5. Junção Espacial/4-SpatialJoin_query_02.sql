-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-join.html
--
-- Quantos focos de incêndio na vegetação foram detectados em
-- Unidades de Conservação Estaduais do Estado do Tocantins em 2020?

SELECT uc.nome AS nome, COUNT(*) AS total_focos
FROM focos_2020, unidades_conservacao AS uc
INNER JOIN uf ON uf.nome = 'TOCANTINS'
WHERE ST_Intersects(uf.geom, uc.geom) AND ST_Contains(uc.geom, focos_2020.geom) AND uc.jurisdicao = 'Estadual'
GROUP BY uc.id, uc.nome
ORDER BY total_focos DESC;
