#!/bin/bash

DATABASE="FRGC"
METHOD="p"
STRENGTHS="10 25"

python3 DET_plotter.py --database $DATABASE --method $METHOD --strengths $STRENGTHS --include_bona_fide