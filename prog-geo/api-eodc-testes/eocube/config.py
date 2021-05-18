"""
4. API - EO Data Cube.
"""

import os

# Save files base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# EO Cube Services
EOCUBE_URL = "http://localhost:5000/eocube"

# Brazil data cube services
STAC_URL = "https://brazildatacube.dpi.inpe.br/stac/"

# Access token for users
ACCESS_TOKEN = ""