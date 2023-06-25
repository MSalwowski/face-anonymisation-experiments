#!/bin/bash

DATABASE="sample"
METHOD="p"
STRENGTHS="10"

for STRENGTH in $STRENGTHS
do
    python3 anonymiser.py --database $DATABASE --method $METHOD --strength $STRENGTH
done