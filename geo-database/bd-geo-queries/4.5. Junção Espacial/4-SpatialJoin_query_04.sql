-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-join.html
--
-- Quantos focos de incêndio ocorreram nas proximidades da rodovia BR-153 no mês de setembro de 2017?

SELECT COUNT(*) AS total_focos FROM (
	SELECT DISTINCT focos.id
	FROM focos
	INNER JOIN trechos_rodoviarios AS trechos ON trechos.codtrechor = 'BR-153'
    WHERE ST_DWithin(trechos.geom, focos.geom, 1000.0 / 111000.0)
    	AND focos.data_obser >= '2017-09-01' AND focos.data_obser < '2017-10-01'
) AS focos_sel;
