#!/bin/bash

cp dicli.py /usr/bin/_dicli.py
cat <<EOF >> /usr/bin/dicli
python3 /usr/bin/_dicli.py
EOF
chmod +x /usr/bin/dicli
