# API - EO Data Cube Server

[![Miniconda](https://img.shields.io/badge/miniconda-3-green)](https://docs.conda.io/en/latest/miniconda.html)
[![Python](https://img.shields.io/badge/python-3.8-green)](https://www.python.org/)

Construir uma biblioteca Python chamada EOCubes que forneça uma abstração denominada DataCube para cubos de dados de observação da Terra. Essa abstração deverá possibilitar o uso das coleções disponíveis no serviço STAC da Plataforma Brazil Data Cube. Utilize as bibliotecas stac.py e Xarray na construção dessa nova bilioteca. Considere criar um ou mais Notebooks que ajudem a apresentar as funcionalidades desse pacote. Utilize os cubos de dados disponíveis no portal do projeto Brazil Data Cube para testar a biblioteca desenvolvida. Forneça exemplos de uso dessa biblioteca, por exemplo, com operações de geração de índices espectrais ou extração de séries temporais. Também considere integrar recursos de visualização e processamento paralelo.

## Instalação das Dependências

Atualizar o pacote `pip` e o `setuptools` para a instalação:

~~~shell
(eocube) ~/eocube-server $ python -m pip install --upgrade pip setuptools
~~~

Instalar as depências utilizando o arquivo [`setup.py`](./setup.py):

~~~shell
(eocube) ~/eocube-server $ python -m pip install -e .[all]
~~~

## Execução

Executar utilizando o arquivo [`manage.py`](./manage.py) com a interface de linha de comando [`Click`](https://click.palletsprojects.com/en/8.0.x/):

~~~shell
(eocube) ~/eocube-server $ python manage.py --run_port=5000
~~~
