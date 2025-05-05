# JSON Exploder

JSON list payload generator targeting JSON parsers. Generated payloads are intent on causing excessive error conditions and/or consumption of resources when processed by JSON parsers.

## Usage

```
Usage: json_exploder.py [OPTIONS] max_indices
OPTIONS:
	--outfile[=FILENAME]: save output to file. If FILENAME is not specified, a randomized filename will be used
	-r: NOT IMPLEMENTED YET!
	-p: Generate a "pyramid list" payload: max_indices first level, max_indices-1 all subsequent levels until top level with single string value
	-d: NOT IMPLEMENTED YET!
	-f: force "unsafe" operations (ex. "pyramid list" payload with more than max_indices>5)
```

