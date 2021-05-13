-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/overlay.html
--
-- Quantos KM de rodovia existem no Estado do Tocantins com o tipo de revestimento “Pavimentado”?

WITH trechos_length AS (
	SELECT trechos.gid, trechos.codtrechor, trechos.revestimen, ST_Length(trechos.geom) as length_
	FROM trechos_rodoviarios AS trechos
	INNER JOIN uf ON uf.nome = 'TOCANTINS'
	WHERE ST_Contains(uf.geom, trechos.geom) AND ST_Intersects(uf.geom, trechos.geom)
	AND trechos.revestimen = 'Pavimentado'
) SELECT 111*SUM(length_) || ' km' AS Km_trechos_tocantins FROM trechos_length;

-- Utilizando conversões

WITH trechos_length AS (
	SELECT trechos.gid, trechos.codtrechor, trechos.revestimen,
	ST_Length_Spheroid(trechos.geom, 'SPHEROID["WGS 84",6378137,298.257223563]')/1000 as length_
	FROM trechos_rodoviarios AS trechos
	INNER JOIN uf ON uf.nome = 'TOCANTINS'
	WHERE ST_Contains(uf.geom, trechos.geom) AND ST_Intersects(uf.geom, trechos.geom)
	AND trechos.revestimen = 'Pavimentado'
) SELECT SUM(length_) || ' km' AS Km_trechos_tocantins FROM trechos_length;
