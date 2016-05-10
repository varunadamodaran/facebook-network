# Your functions go here!
import networkx as nx
import re
import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
#plotly.offline.init_notebook_mode()
from plotly.offline import plot
import plotly.plotly as py
import plotly.offline as pyoff
from plotly.graph_objs import *
from operator import itemgetter

def load_graph(EdgeFile):
  G = nx.Graph()
  node1 = 0
  node2 = 0
  with open(EdgeFile, "r") as EdgeData:
    for x in EdgeData:
      node1 = re.compile('^[\d]*[^\s]').findall(x)
      node2 = re.compile('[\d]*$').findall(x)
      G.add_edge(node1[0],node2[0])
  return G

def analyze_graph(GraphObject):
  G = networkx.Graph()
  G = GraphObject
  components = networkx.number_connected_components(G)
  Diameter_list = []
  Avg_path_list = []
  cent_dict = []
  cent_tuple = ()
  cent_list = []
  print('### Analyzing Graph ###')
  print('Number of Nodes:', len(G))
  print('Number of Edges:', G.size())
  print('Number of connected components:', components)
  for graph in networkx.connected_component_subgraphs(G):
    Diameter_list.append(networkx.diameter(graph))
    Avg_path_list.append(networkx.average_shortest_path_length(graph))
  print('Graph diameter:', max(Diameter_list))
  print('Average shortest path length:', max(Avg_path_list))
  print('Clustering coefficient:',networkx.average_clustering(G))
  cent_dict = networkx.degree_centrality(G)
  for key,value in cent_dict.items():
    cent_tuple = (key,value)
    cent_list.append(cent_tuple)
  cent_list = sorted(cent_list,key=itemgetter(1),reverse=True)
  cent_list = cent_list[:10]
  print('Nodes with highest degree centrality:')
  for item in cent_list:
    print(item[0],'(centrality:',item[1],')')

def scatter_nodes(G,pos, labels=None, color='BLUE',size = 20, opacity=1):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    L=len(pos)
    trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[]))
    cent_dict = nx.degree_centrality(G)
    for k in pos.keys():
        trace['x'].append(pos[k][0])
        trace['y'].append(pos[k][1])
        trace['marker']['size'].append(cent_dict[k]*100)
 
    attrib=dict(name='', text=labels , hoverinfo = 'text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib
    if color is not None:
        trace['marker']['color']=color
    return trace     

def scatter_edges(G, pos, line_color='rgb(211,211,211)', line_width=1):
    trace = Scatter(x=[], y=[], mode='lines')
    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
        trace['hoverinfo']='none'
        trace['line']['width']=line_width
        if line_color is not None: # when it is None a default Plotly color is used
            trace['line']['color']=line_color
    return trace

def make_annotations(pos, text, font_size=14, font_color='rgb(25,25,25)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = Annotations()
    for k in pos.keys():
        annotations.append(
            Annotation(
                text=text[int(k)], 
                x=pos[k][0], y=pos[k][1],
                xref='x1', yref='y1',
                font=dict(color= font_color, size=font_size),
                showarrow=False)
        )
    return annotations  

def plot_graph(GraphObject):
  G = nx.Graph()
  G = GraphObject
  color = None
  size = 20
  pos=nx.fruchterman_reingold_layout(G,iterations = 100)   
  # labels are  set as the nodes indices and their degrees 
  labels = []
  hoverinfo = G.degree()
  for key in hoverinfo.keys():
      labels.append(str(key)+" (degree "+str(hoverinfo[key])+")")
  trace1=scatter_edges(G, pos)
  trace2=scatter_nodes(G,pos, labels=labels)
  width=500
  height=500
  axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
  layout=Layout(title= 'Social Network Graph',  
    font= Font(),
    showlegend=False,
    autosize=False,
    width=width,
    height=height,
    xaxis=XAxis(axis),
    yaxis=YAxis(axis),
    margin=Margin(
        l=40,
        r=40,
        b=85,
        t=100,
        pad=0,
       
    ),
    hovermode='closest',
    plot_bgcolor='WHITE', #set background color            
    )
  data=Data([trace1, trace2])
  fig = Figure(data=data, layout=layout)
  py.sign_in('empet', '')
  pyoff.plot({'data':data,'layout':layout})


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
