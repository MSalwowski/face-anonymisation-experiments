#!/bin/bash

DATABASE="FRGC"
METHOD="dp"
STRENGTHS="1.0"

python3 DET_plotter.py --database $DATABASE --method $METHOD --strengths $STRENGTHS --include_bona_fide