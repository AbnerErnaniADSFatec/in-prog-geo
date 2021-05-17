# Sample Assessment App

[![Docker](https://img.shields.io/badge/Docker-latest-green)](https://www.docker.com/)
[![Docker SITS](https://img.shields.io/badge/BDC_Sits_RStudio-1.4.1103-green)](https://hub.docker.com/r/brazildatacube/sits-rstudio)
[![Shiny for R](https://img.shields.io/badge/Shiny-latest-green)](https://shiny.rstudio.com/)

Esta interface web será apresentada como uma plataforma onde os usuários poderão fazer o upload dos dados com base em diferentes formatos de arquivos ou utilizando serviços para postagem de mapas como o Geoserver.

A partir do momento da obtenção dos arquivos,a plataforma fará a leitura dos dados de acordo com formato  de  entrada.

Será  utilizado  como  base  os  serviços  em  R  do  projeto BDC que  permitem  a avaliaçãoe o tratamentodas amostras utilizando a metodologia do algoritmo SOM -Self-Organizing Map.

A  plataforma será  desenvolvida  utilizando frameworks e  ferramentas  próprias  para este  tipo  de processamento como o Jupyter Notebooke extensões que permitirãoa manipulação de dados geográficos, logo procurando a melhor integração e proveito dessas tecnologias.

## Dependências

### Shiny

`Shiny` é um pacote da plataforma `RStudio` que permite a criação de páginas _web_ interativas. É possível executar _scripts_ em linguagem `R` para o processamento e análise de dados. Este pacote foi feito para a geração de páginas sem a necessidade de conhecimentos em `HTML` e `CSS`.

### SITS

O pacote [`SITS - Satellite Image Time Series`](https://github.com/e-sensing/sits) Analysis for Earth Observation Data Cubes fornece um conjunto de ferramentas para a análise, visualização e classificação de séries temporais provenientes de imagens de satélite.

A principal funcionalidade do pacote `sits` é o suporte para a classificação de mudanças de uso e cobertura da terra em imagens de satélite.

Fluxo de Trabalho do `sits`:

 - Criação de um cubo de dados utilizando coleções de imagens provenientes de serviços em nuvem ou locais;
 - Extração das séries temporais;
 - Análise e avaliação de amostras;
 - Treinamento de algoritmos de aprendizagem de máquina;
 - Classificação de um cubo de dados utilzando o modelo de aprendizagem de máquina;
 - Pós processamento das imagens;
 - Avaliação da acurácia gerada pelo modelo utilizando boas práticas;

## Ambiente de desenvolvimento em R

O comando abaixo irá criar um container docker para o `RStudio` com as dependências do pacote `SITS` em ambiente de testes, onde após a execução todos o container será excluído:

~~~dos
docker run --rm -it --name sample-assessment \
    -v ${PWD}/:/home/sits/sample-assessment \
    -p 8787:8787 \
    brazildatacube/sits-rstudio:1.4.1103
~~~

O comando abaixo também criará um container com as dependências do `sits`, porém o container será executado em segundo plano:

~~~dos
docker  run -d --name sample-assessment \
    -v ${PWD}/:/home/sits/sample-assessment \
    -p 8787:8787 \
    brazildatacube/sits-rstudio:1.4.1103
~~~

Para executar comandos como super usuário neste container é necessário executar o seguinte comando:

~~~dos
docker exec -it sample-assessment bash
~~~

Instalar as dependências necessárias para a avaliação de amostras utilizando o `sits`:

~~~dos
sample-assessment # cp -u -R /home/sits/sample-assessment/data/sits-bundle/* /usr/local/lib/R/site-library/
~~~

Para excluir as dependências do container docker:

~~~dos
sudo chmod +x ./delete-all.sh && ./delete-all.sh
~~~
