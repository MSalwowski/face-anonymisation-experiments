#!/bin/env bash

DATABASE="FRGC"
METHOD="deepprivacy"
STRENGTHS="1.0"

for STRENGTH in $STRENGTHS
do
  cp -r $DATABASE/anonymised/$METHOD/$STRENGTH $DATABASE
  mv $DATABASE/$STRENGTH $DATABASE/reference
  python3 comparator.py --database $DATABASE
  mkdir -p $DATABASE/results/$METHOD/$STRENGTH
  mv $DATABASE/reference_embeddings $DATABASE/results/$METHOD/$STRENGTH/reference_embeddings
  mv $DATABASE/reference $DATABASE/results/$METHOD/$STRENGTH/reference
  mv $DATABASE/scores $DATABASE/results/$METHOD/$STRENGTH/scores
done