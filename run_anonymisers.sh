#!/bin/bash

DATABASE="FRGC"
METHOD="p"
STRENGTHS="50 40 30 20"

for STRENGTH in $STRENGTHS
do
    python3 anonymiser.py --database $DATABASE --method $METHOD --strength $STRENGTH
done