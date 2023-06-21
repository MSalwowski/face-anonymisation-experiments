#!/bin/env bash

DATABASE="sample"
METHOD="blurred"

for STRENGTH in 2.0 5.0 8.0
do
  cp -r $DATABASE/anonymised/$METHOD/$STRENGTH $DATABASE
  mv $DATABASE/$STRENGTH $DATABASE/reference
  python3 comparator.py --database $DATABASE
  mkdir -p $DATABASE/results/$METHOD/$STRENGTH
  mv $DATABASE/reference_embeddings $DATABASE/results/$METHOD/$STRENGTH/reference_embeddings
  mv $DATABASE/reference $DATABASE/results/$METHOD/$STRENGTH/reference
  mv $DATABASE/scores $DATABASE/results/$METHOD/$STRENGTH/scores
done