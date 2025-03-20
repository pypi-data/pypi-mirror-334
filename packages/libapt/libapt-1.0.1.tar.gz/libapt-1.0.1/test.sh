#!/bin/bash

clear

echo "=================== Linters ===================="

echo "------------------- Ruff -----------------------"

uv run ruff check --output-format=github .

echo "------------------- darglint--------------------"

uv run darglint --verbosity 2 --docstring-style sphinx libapt

echo "=================== Tests ===================="

if [[ $1 == "all" ]]; then
    uv run coverage run -m pytest -v -s
else
    uv run coverage run -m pytest -v -s -m "not long_running"
fi

uv run coverage report -m
uv run coverage html
