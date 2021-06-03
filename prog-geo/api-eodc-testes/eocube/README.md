# API - EO Data Cube Python Package

[![Miniconda](https://img.shields.io/badge/miniconda-3-green)](https://docs.conda.io/en/latest/miniconda.html)
[![Python](https://img.shields.io/badge/python-3.8-green)](https://www.python.org/)

Construir uma biblioteca Python chamada EOCubes que forneça uma abstração denominada DataCube para cubos de dados de observação da Terra. Essa abstração deverá possibilitar o uso das coleções disponíveis no serviço STAC da Plataforma Brazil Data Cube. Utilize as bibliotecas stac.py e Xarray na construção dessa nova bilioteca. Considere criar um ou mais Notebooks que ajudem a apresentar as funcionalidades desse pacote. Utilize os cubos de dados disponíveis no portal do projeto Brazil Data Cube para testar a biblioteca desenvolvida. Forneça exemplos de uso dessa biblioteca, por exemplo, com operações de geração de índices espectrais ou extração de séries temporais. Também considere integrar recursos de visualização e processamento paralelo.

## Criação do Ambiente Virtual MiniConda

Criar um ambiente com o miniconda:

~~~shell
$ conda create --name eocube python==3.8
~~~

Ativar o ambiente:

~~~shell
$ conda activate eocube
~~~

## Instalando as dependências

Instalando a dependência `IPython` para utilizar o ambiente conda no jupyter:

~~~shell
(eocube) $ conda install -c anaconda ipython ipykernel jupyter
~~~

Para instalar as dependências específicas de cada exemplo [EO Cube](./eocube) e o serviço [EO Cube Server](./eocube-server), faremos uma conexão com o ambiente virtual criado anteriormente:

~~~shell
(eocube) $ ipython kernel install --user --name eocube
~~~

## Documentação e Testes

Construção da documentação e execução dos testes unitários para a API e o pacote EOCube `./help/build/index.html`.

~~~shell
(eocube) $ sudo chmod +x ./build.sh && ./build.sh
~~~

## Execução

Execução do pacote no ambiente Jupyter no Python.

~~~shell
(eocube) $ jupyter-notebook
~~~

## Instalação das Dependências

Atualizar o pacote `pip` e o `setuptools` para a instalação:

~~~shell
(eocube) ~/eocube-server $ python -m pip install --upgrade pip setuptools
~~~

Realizar a instalação do pacote `GDAL` para a manipulação de imagens:

~~~shell
(eocube) ~/eocube-server $ conda install GDAL
~~~

Instalar as depências utilizando o arquivo [`setup.py`](./setup.py):

~~~shell
(eocube) ~/eocube-server $ python -m pip install -e .[all]
~~~

## Execução

> **Obs.:** Não esqueça de que a cada atualização do pacote o comando de instalação `.[all]` deve ser executado para atualizar o repositório, o kernel do `jupyter-notebook` deve ser reiniciado também:

~~~python
from eocube import EOCube
~~~
