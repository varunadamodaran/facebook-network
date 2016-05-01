# Your functions go here!









####################################
## DO NOT EDIT BELOW THIS POINT!! ##
## #################################

# Run the method specified by the command-line
if __name__ == '__main__':
	import sys
	cmd = None
	datafile = None
	INVALID_MSG = """
Invalid arguments. Commands available: 
	load <filename> 
	analyze <filename>
	plot <filename>
"""[1:-1] #bad command message

	try: #catch invalid argument lengths
		cmd = sys.argv[1]
		datafile = sys.argv[2]
	except:
		print(INVALID_MSG)
	else:
		if cmd == 'load':
			G = load_graph(datafile)
			print("loaded graph with", len(G), "nodes and", G.size(), "edges")
		elif cmd == 'analyze':
			G = load_graph(datafile)
			analyze_graph(G)
		elif cmd == 'plot':
			G = load_graph(datafile)
			plot_graph(G)
		else:
			print(INVALID_MSG)
