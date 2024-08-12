#/bin/bash

set -exo pipefail

python -m unittest mebibyte/test/converter_test.py
python -m unittest mebibyte/test/expression_test.py
python -m unittest mebibyte/test/handler_test.py
python -m unittest mebibyte/test/operand_test.py
python -m unittest mebibyte/test/operator_test.py