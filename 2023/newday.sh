#!/bin/bash

if [ -z "$1" ]; then
    echo "missing day number"
    exit 1
fi

DAY=$1

DAY_INPUTS="inputs/day$DAY"
DAY_CMD="cmd/day$DAY"

if [ -e $DAY_INPUTS ]; then
    echo "Abort because inputs folder $DAY_INPUTS already exists"
    exit 1
fi
if [ -e $DAY_CMD ]; then
    echo "Abort because cmd folder $DAY_CMD already exists"
    exit 1
fi

mkdir -p "$DAY_INPUTS"
touch "$DAY_INPUTS/input.txt"
touch "$DAY_INPUTS/test.txt"

mkdir -p "$DAY_CMD"
sed 's/XXX/'"$DAY"'/g' templates/main.go.template > "$DAY_CMD/main.go"
