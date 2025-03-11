#!/bin/bash

if [ "$MODE" == "DEVELOPMENT" ]
then
  poetry install
else
  poetry install --only main
fi
