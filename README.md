# JSON Exploder

JSON list payload generator targeting JSON parsers. Generated payloads are intent on causing excessive consumption of resources and/or error conditions when processed by JSON parsers.

## Payload Types

Payload names are proprietary and are described below

### "Normal"

TODO

### "Pyramid"

TODO

### "Reverse Pyramid"

TODO

## Usage

```
Usage: json_exploder.py [OPTIONS] max_indices
OPTIONS:
	--outfile[=FILENAME]: save output to file. If FILENAME is not specified, a randomized filename will be used
	--normal: (Default) Generate a "normal" list payload: max_indices number of indices, with each index having a single string value deeply nested within a random-leveled (1-max_indices) list
	--pyramid: Generate a "pyramid list" payload: max_indices first level, max_indices-1 all subsequent nested levels until top level with single string value
	--reverse-pyramid: Generate a "reverse pyramid list" payload: 1 index first level, n+1 all subsequent nested levels until top level with max_indices string values
	--repeat-random: use same random value for all indices in payload
	--fully-random: (Default) use different random value for all indices in payload
	--random-types: fill in indices with random type(s)
	-f: force "unsafe" operations (ex. "pyramid list" payload with max_indices>5)
		NOTE: setting -f option will automatically set --outfile option!
	--append=DATA: add DATA (must be valid JSON data: this is not validated) as final index in final nested level.
	--append-file=FILENAME: add FILENAME file contents (FILENAME must contain valid JSON data: this is not validated) as final index in final nested level.
```

