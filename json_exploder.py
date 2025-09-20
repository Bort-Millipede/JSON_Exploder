#! /usr/bin/python3

import sys
import random
import string
import time

def rand_val(max_length,random_type=False):
	ret_val = None
	
	if random_type:
		type_list = [False,1,0.1,"",[],None,{}]
		t = type(random.choice(type_list))
		if t == type(False):
			ret_val = str(bool(random.randint(0,2))).lower()
		elif t == type(1):
			ret_val = str(random.randint(-2147483648,2147483647))
		elif t == type(0.1):
			sci_not = bool(random.randint(0,2))
			if sci_not:
				ret_val = "%e"%(random.uniform(-2147483648,2147483647))
			else:
				ret_val = str(random.uniform(-2147483648,2147483647))
		elif t == type(""):
			ret_val = "\"%s\""%(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,max_length+1)))
		elif t == type([]):
			ret_val = "[]"
		elif t == type(None):
			ret_val = "null"
		elif t == type({}):
			random_dict = {}
			for i in range(max_length*random.randint(1,3)):
				key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,max_length+1))
				val_type = type(random.choice(type_list))
				value = None
				if val_type == type(False):
					value = bool(random.randint(0,2))
				elif val_type == type(1):
					value = random.randint(-2147483648,2147483647)
				elif val_type == type(0.1):
					value = random.uniform(-2147483648,2147483647)
				elif val_type == type(""):
					value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,max_length+1))
				elif val_type == type([]):
					value = []
				elif val_type == type(None):
					value = None
				elif val_type == type({}):
					value = {}
				random_dict[key] = value
			ret_val = str(random_dict)
			ret_val = ret_val.replace(" ","",-1).replace("None","null",-1).replace("False","false",-1).replace("True","true",-1).replace("\'","\"",-1)
	else:
		ret_val = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,max_length+1))
	
	return ret_val

def normal_explode(max_indices,repeat_rand,rand_types):
	out_json = ''
	rand = rand_val(max_indices*random.randint(1,3),rand_types)
	
	i=0
	while i<max_indices:
		i_depth = random.randint(1,max_indices+1)
		index = '%s'%('['*i_depth)
		index += rand
		if not repeat_rand: rand = rand_val(max_indices*random.randint(1,3),rand_types)
		index += '%s,'%(']'*i_depth)
		out_json += index
		i+=1
	
	out_json = out_json.rstrip(',')
	out_json = "[%s]"%(out_json)
	
	return out_json

def pyramid_explode(max_indices,repeat_rand,rand_types):
	out_json = '["RANDHERE"]'
	i=2
	while i<=max_indices:
		j=1
		while j<=i:
			out_json = "%s,"%(out_json)*j
			out_json = out_json.rstrip(',')
			out_json = "[%s]"%(out_json)
			j+=1
		i+=1
	
	while out_json.find("\"RANDHERE\"")!=-1:
		out_json = out_json.replace("\"RANDHERE\"","%s"%(rand_val(max_indices*random.randint(1,3),rand_types)),-1 if repeat_rand else 1)
	
	return out_json

def reverse_pyramid_explode(max_indices,repeat_rand,rand_types):
	out_json = reverse_pyramid_recurse("",max_indices,max_indices)
	out_json = "[%s]"%(out_json)
	
	while out_json.find("\"RANDHERE\"")!=-1:
		out_json = out_json.replace("\"RANDHERE\"","%s"%(rand_val(max_indices*random.randint(1,3),rand_types)),-1 if repeat_rand else 1)
	
	return out_json

def reverse_pyramid_recurse(out_json,max_indices,counter):
	if max_indices==counter:
		out_json = '"RANDHERE",'*counter
		out_json = out_json.rstrip(',')
		out_json = "[%s]"%(out_json)
	if counter>=2:
		out_json = '%s,'%(out_json)*counter
		out_json = out_json.rstrip(',')
		out_json = "[%s]"%(out_json)
		return reverse_pyramid_recurse(out_json,max_indices,counter-1)
	else:
		return out_json

def usage():
	sys.stderr.write("\nUsage: %s [OPTIONS] max_indices\n"%(sys.argv[0]))
	sys.stderr.write("OPTIONS:\n\t--outfile[=FILENAME]: save output to file. If FILENAME is not specified, a randomized filename will be used\n")
	sys.stderr.write("\t--normal: (Default) Generate a \"normal\" list payload: max_indices number of indices, with each index having a single string value deeply nested within a random-leveled (1-max_indices) list\n")
	sys.stderr.write("\t--pyramid: Generate a \"pyramid list\" payload: max_indices first level, max_indices-1 all subsequent nested levels until top level with single string value\n")
	sys.stderr.write("\t--reverse-pyramid: Generate a \"reverse pyramid list\" payload: 1 index first level, n+1 all subsequent nested levels until top level with max_indices string values\n")
	sys.stderr.write("\t--repeat-random: use same random value for all indices in payload\n")
	sys.stderr.write("\t--fully-random: (Default) use different random value for all indices in payload\n")
	sys.stderr.write("\t--random-types: fill in indices with random type(s)\n")
	sys.stderr.write("\t-f: force \"unsafe\" operations (ex. \"pyramid list\" payload with max_indices>5)\n\t\tNOTE: setting -f option will automatically set --outfile option!\n")
	sys.stderr.write("\t--append=DATA: add DATA (must be valid JSON data: this is not validated) as final index in final nested level.\n")
	sys.stderr.write("\t--append-file=FILENAME: add FILENAME file contents (FILENAME must contain valid JSON data: this is not validated) as final index in final nested level.\n\n")

if __name__ == '__main__':
	if len(sys.argv)<2:
		usage()
		sys.exit(1)
	
	out_filename = None
	normal = True
	pyramid = False
	reverse_pyramid = False
	repeat_rand = False #--repeat-random (True) or --full-random (False)
	rand_types=False
	append = False
	append_data = None
	append_filename = None
	append_file = None
	unsafe = False
	max_indices = -1
	
	i=1
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
		elif arg_split[0] == "--normal":
			normal = True
			pyramid = False
			reverse_pyramid = False
		elif arg_split[0] == "--pyramid":
			pyramid = True
			normal = False
			reverse_pyramid = False
		elif arg_split[0] == "--reverse-pyramid":
			reverse_pyramid = True
			pyramid = False
			normal = False
		elif arg_split[0] == '--repeat-random':
			repeat_rand = True
		elif arg_split[0] == '--fully-random':
			repeat_rand = False
		elif arg_split[0] == "--random-types":
			rand_types = True
		elif arg_split[0] == "-f":
			unsafe = True
			if out_filename == None: out_filename = "exploded_%i.json"%(int(time.time()))
		elif arg_split[0] == "--append":
			append = True
			if len(arg_split)>1:
				append_data = arg_split[1]
				if len(append_data)<1:
					sys.stderr.write("Empty input specified with --append!\n")
					sys.exit(2)
			else:
				sys.stderr.write("No input specified with --append!\n")
				sys.exit(2)
		elif arg_split[0] == "--append-file":
			append = True
			if len(arg_split)>1:
				append_filename = arg_split[1]
			else:
				sys.stderr.write("No input file specified with --append-file!\n")
				sys.exit(3)
		else:
			sys.stderr.write("Invalid option: %s\n\n"%(arg_split[0]))
			sys.exit(4)
		i+=1
	
	try:
		max_indices = int(sys.argv[len(sys.argv)-1])
		if max_indices<1:
			raise ValueError
	except ValueError as ve:
		sys.stderr.write("Invalid maximum indices: %s\n"%(sys.argv[len(sys.argv)-1]))
		usage()
		sys.exit(5)
	
	if append and append_filename!=None:
		try:
			append_file = open(append_filename,'r')
		except:
			sys.stderr.write("File %s could not be opened!\n"%(append_filename))
			sys.exit(6)
	
	if max_indices>5 and (pyramid or reverse_pyramid):
		if not unsafe:
			sys.stderr.write("pyramid or reverse payloads with max_indices>5 can only be generated by specifying -f!\n")
			usage()
			sys.exit(7)
	
	out_json = ''
	if pyramid:
		out_json = pyramid_explode(max_indices,repeat_rand,rand_types)
	elif reverse_pyramid:
		out_json = reverse_pyramid_explode(max_indices,repeat_rand,rand_types)
	else:
		out_json = normal_explode(max_indices,repeat_rand,rand_types)
	
	if append:
		if append_file!=None:
			append_data = append_file.read()
			append_file.close()
		
		i=len(out_json)-1
		last_index = out_json[i]
		while last_index==']':
			i-=1
			last_index = out_json[i]
		i+=1
		out_json = "%s%s%s%s"%(out_json[0:i],'' if last_index=='[' else ',',append_data,out_json[i:])
	
	if out_filename != None:
		outfile = None
		try:
			open(out_filename,'w')
			outfile.write(out_json)
			outfile.close()
			print("Output saved to %s"%(out_filename))
		except:
			sys.stderr.write("Could not write output to %s!\n"%(out_filename))
			sys.exit(8)
	else:
		print(out_json)
	
	sys.exit(0)

