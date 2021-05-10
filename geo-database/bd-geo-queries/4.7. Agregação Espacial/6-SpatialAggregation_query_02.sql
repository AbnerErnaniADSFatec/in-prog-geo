-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-aggregation.html
--
-- Utilizando os dados dos anos de 2017 e 2018 de focos, apresente uma contagem por bioma.

WITH f AS (SELECT DISTINCT focos.id, focos.geom FROM focos WHERE focos.data_obser >= '2017-09-01' AND focos.data_obser < '2017-10-01')
SELECT * from f, biomas WHERE ST_Contains(biomas.geom, f.geom);

-- PostgreSQL and QGIS

SELECT * FROM focos WHERE '2017-09-01' <= data_obser AND data_obser < '2017-10-01';
