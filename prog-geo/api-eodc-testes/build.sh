pydocstyle eocube/*.py eocube-server/*.py && \
isort eocube eocube/setup.py eocube-server/setup.py --check-only --diff && \
check-manifest eocube-server && \
check-manifest eocube && \
pytest && \
sphinx-build -qnW --color -b doctest help/source help/_build && \
cd help && sphinx-build -b html -d _build/doctrees source build
