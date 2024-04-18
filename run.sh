#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export QT_QPA_PLATFORM=xcb

source $SCRIPT_DIR/venv/bin/activate
python $SCRIPT_DIR/main.py