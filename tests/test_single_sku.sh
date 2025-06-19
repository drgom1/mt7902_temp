#!/bin/sh
set -e

DIR="$(dirname "$0")"
ROOT="$DIR/.."

OUTPUT="$(perl "$ROOT/src/scripts/single-sku.pl" mt7615 "$DIR/sample.txt")"

echo "$OUTPUT" | grep -q "power-limits {"
