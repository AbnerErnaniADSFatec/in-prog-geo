"""
API - EO Data Cube.

Python Client Library for Earth Observation Data Cubes.
This abstraction uses STAC.py library provided by BDC Project.

=======================================
begin                : 2021-05-01
git sha              : $Format:%H$
copyright            : (C) 2020 by none
email                : none@inpe.br
=======================================

This program is free software.
You can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
"""

import os

import click
from eocube_server.app import app


# Aplicando a biblioteca click para criar uma interface de linha de comando
@click.command()
@click.option('--run_port', default=5000, help='Port number.')
def run(run_port):
    """Run a Flask server for API.

    ## Parameters

    ### run_port : int, required

        The port number for run the Flask server.

    ## Raise

    ### ValueError

        If the run port number is null.
    """
    # A API será executada no localhost
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        run_port = int(os.environ.get('PORT', str(run_port)))
    except ValueError:
        run_port = 5000
    app.run(host, run_port, debug=True)

# Aplicando o método run
if __name__ == '__main__':
    run()
