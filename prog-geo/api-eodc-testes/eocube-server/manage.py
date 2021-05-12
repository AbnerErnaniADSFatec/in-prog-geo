"""
4. API - EO Data Cube.
"""

import os
import click
from eocube_server.app import app

@click.command()
@click.option('--run_port', default=5000, help='Port number.')
def run(run_port):
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        run_port = int(os.environ.get('PORT', str(run_port)))
    except ValueError:
        run_port = 5000
    app.run(host, run_port, debug=True)

if __name__ == '__main__':
    run()
