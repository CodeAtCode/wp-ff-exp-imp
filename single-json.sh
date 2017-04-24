#!/bin/bash
jq -s '.' ./export-json/*.json > ./json-result/export.json
sed -i 's/\[poll id=\\"1\\"\]//g' ./json-result/export.json
