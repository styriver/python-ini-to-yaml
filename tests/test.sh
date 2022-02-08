#!/bin/bash

echo "installing pyyaml"
pip install pyyaml --upgrade
echo "running test"
python ini_to_yml.py --in ./tests/PROD-AUTH --out C:\Users\HpLaptop-Scott\test.yaml
python ini_to_yml.py --in ./tests/PROD-CLOUD --out C:\Users\HpLaptop-Scott\test.yaml

