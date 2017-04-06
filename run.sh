#!/usr/bin/env bash

# Remove existing analytics files
rm -rf ./log_output/*

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
python ./src/process_log.py
