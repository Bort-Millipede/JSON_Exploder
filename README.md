# JSON Exploder

JSON list payload generator targeting JSON parsers. Generated payloads are intent on causing excessive consumption of resources and/or error conditions when processed by JSON parsers.

Because JSON lists are not explicitly typed and can also contain lists themselves, processing complicated but syntactically-correct JSON lists can easily cause excessive resource consumption and/or error conditions when the parse does not perform type checking on inputted data. This payload generator can be helpful in identifying such conditions.

## Payload Types

Payload names are proprietary and are described below.

### "Normal"

A single-leveled list with each index having randomized values deeply nested within random-leveled lists. 

**Advantages:**  
* Can easily generate large (but still reasonably sized) payloads (unlike some "Pyramid" and "Reverse Pyramid" payloads).

**Disadvantages:**  
* Payloads with higher indices are more likely to hit parser recursion limits.

#### Example (8 indices with random types)

```
[[[[[null]]]],[[["CLWPG194"]]],[[[[[[[[null]]]]]]]],[[[[[[[]]]]]]],[["V4A4TP8OKQQMRFC9VXNBZ7AA"]],[[[[[[[[2109687633]]]]]]]],[[[[[null]]]]],[[{"9ZSXVDWVCU02C5CS":{},"F9SWPU175AUDI19O":null,"DBOG6XPW8I83XRLK":1584158619.0433578,"W5GJIER3JW0H8F0D":1188323547.8822546,"N4DXZ82DOL04NH34":[],"YU61VCT9VT6YE6DC":true,"BRO6HB4ACZRPG8DF":null,"CW1V74SSO02YMPH9":-1486346002.6097202,"4NTA11C5PHGSR7T3":true,"SWO5G1ZC0IKVHW8A":null,"PSTTUPQWR43LQM95":-1534543860,"LROERCVPFMXWTY7V":true,"VCP1QBZJQL69ZTZQ":246273338.62975693,"5HL2PYE49X21UZ5O":true,"5XX3FJXBORFEN3Q0":"E37JIF9KXZYQ7K6U","3OCKWEJOJIFJ2JZR":{}}]]]
```

### "Pyramid"

A nested list with the maximum indices at the first level and one less index on all subsequent nested levels, until top level containing a single randomized value.

**Advantages:**  
* Large payloads with less likelihood of hitting parser recursion limits (unliked "Normal" payloads).

**Disadvantages:**  
* Payload sizes increase VERY rapidly when increasing maximum index count (eventually requiring use of of `-f` "force" option).

#### Example (3 maximum indices with random types)

```
[[[[[[1.976877e+09]],[[true]]]],[[[[619690826]],[[-1268831296]]]]],[[[[[{"FR3":-1446771320.2394552,"X37":"XJ8","40K":-360574116,"RJY":985123112,"C86":{},"YQI":-237983977}]],[[null]]]],[[[[8.055141e+08]],[[{"U5HBZ3":[],"TA46J6":null,"2HG19K":-551053362,"BC6ATG":-650413624,"V3JIFG":"XN9CBQ","8C0COJ":[]}]]]]],[[[[[1310240640]],[[-1.976122e+08]]]],[[[[true]],[[{"BEG":-618411258,"A47":null,"T9Z":"612","9GP":-2053896626,"CG7":{},"L2I":[],"IWS":null,"E9Y":true,"FRZ":null}]]]]]]
```

### "Reverse Pyramid"

A nested listed with 1 index on the first level, and a +1 increased index count on all subsequent levels until the top level containing randomized values.

**Advantages:**  
* Large payloads with less likelihood of hitting parser recursion limits (unlike "Normal" payloads).
* Payload sizes do not increase as rapidly as "Pyramid" payloads.

**Disadvantages:**  
* Less data contained in payloads overall, and therefore less likely to result in as high of resource consumption as "Pyramid" payloads.

#### Example (3 maximum indices with random types)

```
[[[[-1186149350.272589,true,1789381446.2750611],[null,-118564234.73484683,{"PD6H7H5HS":{},"GMOXOZ7M9":{},"XA4P5UHSB":-2041862220,"4MBJ1122G":-1043222248.5063696,"R062EIVX3":-2064106393,"X162SSD3L":[],"WN9C2SWZE":[],"7EISY4VEV":false,"05VH268SA":{},"5UJKSAY3N":{},"66O5VG2LP":[],"0UXBKTZ5T":748095847.6585484,"0LMX13Q4I":false,"KER1RMK68":{},"HIRPSJ3Y4":false,"LXCRBPZ90":true,"SB9VY7SLG":false,"X65YRY957":[]}],[null,"302S68VRH",null]],[[true,"M5R","X69"],[{"PV2":false,"F33":null,"EOC":{},"UWO":[],"O5U":null,"S38":null,"P0L":[],"QOD":[],"NAY":[]},[],null],[true,true,true]]]]
```

## Usage

```
Usage: json_exploder.py [OPTIONS] max_indices
OPTIONS:
	--outfile[=FILENAME]: save output to file. If FILENAME is not specified, a randomized filename will be used
	--normal: (Default) Generate a "normal" list payload: max_indices number of indices, with each index having a single randomized value deeply nested within a random-leveled (1-max_indices) list
	--pyramid: Generate a "pyramid" list payload: max_indices first level, max_indices-1 all subsequent nested levels until top level with single randomized value
	--reverse-pyramid: Generate a "reverse pyramid" list payload: 1 index first level, n+1 all subsequent nested levels until top level with max_indices randomized values
	--repeat-random: use same random value for all indices in payload
	--fully-random: (Default) use different random value for all indices in payload
	--random-types: fill in indices with random type(s)
	-f: force "unsafe" operations (ex. "pyramid list" payload with max_indices>5)
		NOTE: setting -f option will automatically set --outfile option!
	--append=DATA: add DATA (must be valid JSON data: this is not validated!) as final index in final nested level.
	--append-file=FILENAME: add FILENAME file contents (FILENAME must contain valid JSON data: this is not validated!) as final index in final nested level.
```

### Options 

TODO

