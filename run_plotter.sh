#!/bin/bash

DATABASE="FRGC"
METHOD="gn"
STRENGTHS="0.1 0.2 0.3 0.4"

python3 DET_plotter.py --database $DATABASE --method $METHOD --strengths $STRENGTHS --include_bona_fide