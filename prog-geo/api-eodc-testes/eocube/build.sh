pydocstyle *.py && \
isort eocube setup.py --check-only --diff && \
check-manifest && \
pytest && \
sphinx-build -qnW --color -b doctest help/source help/_build && \
cd help && sphinx-build -b html -d _build/doctrees source build
cp ./build/ ../../../../docs/