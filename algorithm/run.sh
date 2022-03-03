#! /bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if [ ! -d env ]; then
  python3 -m venv $SCRIPT_DIR/env && \
  pip3 install -r requirements.txt
fi

. env/bin/activate
uvicorn server:app --host=0.0.0.0 --port=8779
