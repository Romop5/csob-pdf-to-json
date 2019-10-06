# ČSOB.sk Unofficial PDF to JSON transformer

## Requirements
- pdfminer package (`pip install pdfminer`)

## Usage
```
pdf2txt.py exportFileName.pdf > output
csob2json.py output > csob.json
```
Options:
- `--keep-lines`: keep original transaction lines (usefull for manual semantic parsing)

## Output format

- card transaction fields: *amount*, *place*

## Known limitations
Semantic is correctly parsed only for card payments.

## Why 
Seems like CSOB.sk is no longer providing any other means of export for regular customers than PDF.
