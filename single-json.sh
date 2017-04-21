#!/bin/bash
jq -s '.' ./export-json/*.json > ./json-result/export.json
