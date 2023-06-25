#!/bin/bash

DATABASE="FRGC"
METHOD="gn"
STRENGTHS="0.1 0.2 0.3 0.4"

for STRENGTH in $STRENGTHS
do
    python3 anonymiser.py --database $DATABASE --method $METHOD --strength $STRENGTH
done