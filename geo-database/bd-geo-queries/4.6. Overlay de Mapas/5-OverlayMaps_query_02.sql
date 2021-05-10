-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/overlay.html
--
-- Qual o tipo de solo predominante em Ouro Preto?

WITH op_pedologia AS (
	SELECT pedologia.ordem AS ordem,
	COUNT(pedologia.gid) AS ocorrencia
	FROM pedologia
	INNER JOIN municipios AS mun ON mun.nome = 'OURO PRETO'
	WHERE ST_Intersects(mun.geom, pedologia.geom) AND pedologia.ordem IS NOT NULL
	GROUP BY pedologia.ordem
), max_op_pedologia AS (
	SELECT MAX(op_pedologia.ocorrencia) AS maior_ocorrencia FROM op_pedologia
) SELECT ordem, ocorrencia
FROM op_pedologia, max_op_pedologia
WHERE op_pedologia.ocorrencia = max_op_pedologia.maior_ocorrencia;

-- Visualização da pedologia de Ouro Preto

SELECT pedologia.gid AS gid, pedologia.ordem AS ordem, ST_Intersection(pedologia.geom, mun.geom) AS geom
FROM pedologia
INNER JOIN municipios AS mun ON mun.nome = 'OURO PRETO'
WHERE ST_Intersects(mun.geom, pedologia.geom);

-- PostgreSQL and QGIS

CREATE VIEW result_ AS SELECT pedologia.gid AS gid,
pedologia.ordem AS ordem,
ST_Intersection(pedologia.geom, mun.geom) AS geom
FROM pedologia
INNER JOIN municipios AS mun ON mun.nome = 'OURO PRETO'
WHERE ST_Intersects(mun.geom, pedologia.geom);
