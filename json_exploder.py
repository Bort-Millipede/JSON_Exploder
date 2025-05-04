"""
Possible options
* Random output types
* output to file ->DONE
* "pyramid": fill first level with max indices, and recurse with minus 1 indices for each new level until down to 1
* "reverse pyramid": fill first level with 1 index, and recurse with plus 1 indices for each new level until up to max indices
"""

import sys
import random
import string
import time

def rand_val(max_length):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,random.randint(1,max_length+1)))

def normal_explode(max_indices):
	out_json = ''
	i=0
	while i<max_indices:
		i_depth = random.randint(1,max_indices+1)
		index = '%s"'%('['*i_depth)
		index += rand_val(max_indices)
		index += '"%s,'%(']'*i_depth)
		out_json += index
		i+=1
	
	out_json = out_json.rstrip(',')
	out_json = "[%s]"%(out_json)
	
	return out_json

def pyramid_explode(max_indices):
	out_json = 'NOT IMPLEMENTED YET!'
	return out_json

def reverse_pyramid_explode(max_indices):
	out_json = 'NOT IMPLEMENTED YET!'
	return out_json

def usage():
	sys.stderr.write("Usage: %s [OPTIONS] max_indices\n"%(sys.argv[0]))
	sys.stderr.write("OPTIONS:\n\t--outfile[=FILENAME]: save output to file. If FILENAME is not specified, a randomized filename will be used\n")
	sys.stderr.write("\t-r: NOT IMPLEMENTED YET!\n\t-p: NOT IMPLEMENTED YET!\n\t-d: NOT IMPLEMENTED YET!\n")

if __name__ == '__main__':
	if len(sys.argv)<2:
		usage()
		sys.exit(1)
	
	out_filename = None
	rand_types=False
	pyramid = False
	reverse_pyramid = False
	max_indices = -1
	
	i=0
	while i<len(sys.argv)-1:
		arg_split = sys.argv[i].split('=',1)
		if arg_split[0] == "--outfile":
			if len(arg_split)>1:
				if len(arg_split[1])>0:
					out_filename = arg_split[1]
				else:
					out_filename = "exploded_%i.json"%(int(time.time()))
			else:
				out_filename = "exploded_%i.json"%(int(time.time()))
		elif arg_split[0] == "-r":
			rand_types = True
		elif arg_split[0] == "-p":
			pyramid = True
		elif arg_split[0] == "-d":
			reverse_pyramid = True
		
		i+=1
	
	try:
		max_indices = int(sys.argv[len(sys.argv)-1])
	except ValueError as ve:
		sys.stderr.write("Invalid maximum indices: %s\n"%(sys.argv[len(sys.argv)-1]))
		usage()
		sys.exit(2)
	
	if pyramid==True and reverse_pyramid==True:
		sys.stderr.write("Invalid options: can only specify -p or -d, not both\n")
		usage()
		sys.exit(3)
	
	out_json = ''
	if pyramid:
		out_json = pyramid_explode(max_indices)
	elif reverse_pyramid:
		out_json = reverse_pyramid_explode(max_indices)
	else:
		out_json = normal_explode(max_indices)
	
	if out_filename != None:
		outfile = open(out_filename,'w')
		outfile.write(out_json)
		outfile.close()
		print("Output saved to %s"%(out_filename))
	else:
		print(out_json)
	
	sys.exit(0)

