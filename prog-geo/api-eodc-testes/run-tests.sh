pydocstyle eocube/*.py eocube-server/*.py && \
isort eocube eocube/setup.py eocube-server/setup.py --check-only --diff # && \
# check-manifest && \
# sphinx-build -qnW --color -b doctest wtss_plugin/help/source wtss_plugin/help/_build && \
# pytest