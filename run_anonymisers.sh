#!/bin/bash

METHOD="gb"
DATABASE="FRGC"

for STRENGTH in 2 5 8
do
    python3 anonymiser.py --database $DATABASE --method $METHOD --strength $STRENGTH
done