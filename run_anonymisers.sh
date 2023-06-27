#!/bin/bash

DATABASE="sample"
METHODS="b"
STRENGTHS="0.1 0.2 0.3 0.4 0.5"

for STRENGTH in $STRENGTHS
do
    python3 anonymiser.py --database $DATABASE --method $METHOD --strength $STRENGTH
done