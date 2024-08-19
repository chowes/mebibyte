#/bin/bash

set -exo pipefail

streamlit_py="${HOME}/.local/share/pipx/venvs/streamlit/bin/python"

python -m unittest mebibyte/test/converter_test.py
python -m unittest mebibyte/test/expression_test.py
python -m unittest mebibyte/test/handler_test.py
python -m unittest mebibyte/test/operand_test.py
python -m unittest mebibyte/test/operator_test.py
python -m unittest service/test/service_test.py
${streamlit_py} -m unittest frontend/test/frontend_test.py