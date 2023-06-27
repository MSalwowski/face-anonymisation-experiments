#!/bin/env bash

DATABASE="sample"
FULL_METHOD_NAME="blackened"
STRENGTHS="0.1 0.2 0.3 0.4 0.5"

for STRENGTH in $STRENGTHS
do
  cp -r $DATABASE/anonymised/$FULL_METHOD_NAME/$STRENGTH $DATABASE
  mv $DATABASE/$STRENGTH $DATABASE/reference
  python3 comparator.py --database $DATABASE
  mkdir -p $DATABASE/results/$FULL_METHOD_NAME/$STRENGTH
  mv $DATABASE/reference_embeddings $DATABASE/results/$FULL_METHOD_NAME/$STRENGTH/reference_embeddings
  mv $DATABASE/reference $DATABASE/results/$FULL_METHOD_NAME/$STRENGTH/reference
  mv $DATABASE/scores $DATABASE/results/$FULL_METHOD_NAME/$STRENGTH/scores
done