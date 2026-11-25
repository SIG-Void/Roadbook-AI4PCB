#!/bin/sh
# Replay a published model submission to exercise the Harbor pipeline.
set -eu
mkdir -p /app/output
cp /solution/sample/mini_encabulator.kicad_pcb /app/output/mini_encabulator.kicad_pcb
