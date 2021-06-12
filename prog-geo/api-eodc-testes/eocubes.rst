..
    This file is part of Python Client Library for Earth Observation Data Cube.
    Copyright (C) 2021 None.

    Python Client Library for Earth Observation Data Cube is free software;
    You can redistribute it and/or modify it under the terms of the MIT License;
    See LICENSE file for more details.

==========
Instalação
==========

Requisitos necessários `Python version +3 <https://www.python.org/>`_.

Para instalar o pacote python para acessar dados de observação da terra faça o clone do repositório:

.. code-block:: shell

    git clone https://github.com/prog-geo/eocubes

Antes de instalar as dependências atualize para a versão mais recente do gerenciador de pacotes `pip`:

.. code-block:: shell

    pip install --upgrade pip

Na pasta root do repositório `/eocubes` execute o comando abaixo para instalar o pacote
juntamente com as dependências necessárias

.. code-block:: shell

    pip install -e .[all]

.. note::

    Caso houver algum problema na instalação por conta de uma
    dependência é recomendável a criação de um ambiente virtual `conda` ou `pyenv`.

Criação do Ambiente Virtual
---------------------------

A instalação por meio de um ambiente virtual pode ser feita utilizando
a ferramenta `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ ou
o pacote `pypenv <https://pypi.org/project/pyenv/>`_.

Para criar um ambiente virtual com o `miniconda` execute o comando abaixo:

.. code-block:: shell

    conda create --name eocube python==3.8

Ative o ambiente virtual:

.. code-block:: shell

    conda activate eocube

Para criar um ambiente virtual com o `pyenv` execute o comando abaixo:

.. code-block:: shell

    python3 -m venv venv

Ative o ambiente virtual:

.. code-block:: shell

    source venv/bin/activate

.. note::

    Com o ambiente virtual criado é possível executar os comandos de instalação do pacote:

    .. code-block:: shell

        python -m pip install -e .[all]

Instalando as dependências
--------------------------

Instalando a dependência `IPython` para utilizar o ambiente conda no jupyter:

.. code-block:: shell

    (eocube) $ conda install -c anaconda ipython ipykernel jupyter

Para instalar as dependências específicas de cada exemplo [EO Cube](./eocube) e o serviço [EO Cube](./eocube), faremos uma conexão com o ambiente virtual criado anteriormente:

.. code-block:: shell

    (eocube) $ ipython kernel install --user --name eocube

Documentação e Testes
---------------------

Construção da documentação e execução dos testes unitários para a API e o pacote EOCube `./help/build/index.html`.

.. code-block:: shell

    eocube) $ sudo chmod +x ./build.sh && ./build.sh

Execução
--------

Execução do pacote no ambiente Jupyter no Python.

.. code-block:: shell

    (eocube) $ jupyter notebook

Instalação das Dependências
---------------------------

Atualizar o pacote `pip` e o `setuptools` para a instalação:

.. code-block:: shell

    (eocube) ~/eocube $ python -m pip install --upgrade pip setuptools

Realizar a instalação do pacote `GDAL` para a manipulação de imagens:

.. code-block:: shell

    (eocube) ~/eocube $ conda install GDAL

Instalar as depências utilizando o arquivo [`setup.py`](./setup.py):

.. code-block:: shell

    (eocube) ~/eocube $ python -m pip install -e .[all]
    (eocube) ~/home $ python -m pip install git+https://github.com/AbnerErnaniADSFatec/eocubes

Execução
--------

 - **Obs.:** Não esqueça de que a cada atualização do pacote o comando de instalação `.[all]` deve ser executado para atualizar o repositório, o kernel do `jupyter-notebook` deve ser reiniciado também:

.. code-block:: python

    from eocube import EOCube
