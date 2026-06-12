#!/usr/bin/env bash
# Fetch the public datasets the ML notebooks use. Data is gitignored (not re-hosted).
# Run from the ml/ directory:  bash download_data.sh
set -euo pipefail
mkdir -p data
cd data

echo "==> ASSISTments 2009-2010 skill-builder (CORRECTED) via Google Drive"
# Cite: https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data/skill-builder-data-2009-2010
# Feng, Heffernan & Koedinger (2009). No formal license (attribution requested).
python -m pip install --quiet --upgrade gdown
python -m gdown "https://drive.google.com/uc?id=1NNXHFRxcArrU0ZJSb9BIL56vmUt5FhlE" \
  --output assistments_2009_corrected.csv

echo "==> Mohler / UNT CS short-answer grading (ACL 2011, GPL)"
curl -sSL --output mohler.zip \
  "http://web.eecs.umich.edu/~mihalcea/downloads/ShortAnswerGrading_v2.0.zip"
unzip -oq mohler.zip   # extracts to ./data/ (so notebooks read data/data/...)

echo "==> done. Files in ml/data/:"
ls -la
echo
echo "Optional (scaling evidence, not required): EdNet-KT1 (CC BY-NC 4.0) —"
echo "  https://github.com/riiid/ednet  (sample ~5,000 students to fit a free GPU)."
