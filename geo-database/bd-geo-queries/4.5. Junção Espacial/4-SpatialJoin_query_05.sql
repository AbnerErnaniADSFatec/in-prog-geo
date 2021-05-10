-- Consultas realizadas utilizando o QGIS e uma conexão com
-- banco de dados PostgreSQL com as extensão PostGIS.
-- Os dados de consulta podem ser baixados em
-- https://fatecspgov-my.sharepoint.com/:u:/g/personal/abner_anjos_fatec_sp_gov_br/EULYMirmz5JHkYUA1EdF6PsBLfpUC73oHbiftVjwcozICw?e=QmjKAD
--
-- Material do Exercício
-- https://bd-geoespacial.github.io/consultas-espaciais/spatial-join.html
--
-- Quais os municípios vizinhos de Ouro Preto em Minas Gerais?

SELECT m2.nome AS vizinho, m2.geom AS geom
FROM municipios AS m1
INNER JOIN municipios AS m2 ON m2.nome != 'OURO PRETO'
WHERE ST_Touches(m1.geom, m2.geom)
    AND m1.nome = 'OURO PRETO';

-- PostgreSQL and QGIS

CREATE OR REPLACE VIEW result_ AS SELECT m2.nome AS vizinho, m2.geom AS geom
FROM municipios AS m1
INNER JOIN municipios AS m2 ON m2.nome != 'OURO PRETO'
WHERE ST_Touches(m1.geom, m2.geom)
    AND m1.nome = 'OURO PRETO';

CREATE OR REPLACE VIEW result_geom AS SELECT *
FROM municipios AS m1
WHERE m1.nome = 'OURO PRETO';
