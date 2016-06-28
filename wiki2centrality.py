#!/usr/bin/python
import networkx as nx
import bulkwiki2snap as bw
import optparse


def centrality(edgeList):
    """
    """
    print "centrality start"
    file = open(edgeList, "r")
    graph = nx.read_edgelist(file, comments="#", create_using=nx.DiGraph(), nodetype=int)
    file.close()
    #return nx.closeness_centrality(graph)
    return nx.out_degree_centrality(graph)
	
def colorPercentile(model, centrality):
    """
    """
    print "colorPercentile start"
    NUMCOLORS=6

    # Get ids of nodes in model and sort by decreasing centrality
    a=[(centrality[x[1]], x[1]) for x in model if x[1] != None]
    s=set(a)
    a=sorted(list(s), reverse=True)
    print "sorting done"

    # Assign colors to nodes
    length=len(a)
    # scale=length/NUMCOLORS

    steve = int(length*0.1)

    colors = {}

    for i in range(steve):
        colors[a[i][1]]="darkblue"
    for i in range(steve, steve*2):
        colors[a[i][1]]="blue"
    for i in range(steve*2, steve*3):
        colors[a[i][1]]="royalblue"
    for i in range(steve*3, steve*4):
        colors[a[i][1]]="cyan"
    for i in range(steve*4, steve*5):
        colors[a[i][1]]="aquamarine"
    for i in range(steve*5,length):
        colors[a[i][1]]="white"
    print "colorPercentile done"
    return colors
	
def writeColors(title, model, content, colors):
    print "writeColors start"
    # Write style sheet
    #colorFile = open("centrality_2_"+title.replace(" ", "_")+".html", "w")
    colorFile = open("out_degree_"+title.replace(" ", "_")+".html", "w")

    colorFile.write("<!DOCTYPE html>\n<html>\n<head>\n<style/>\n")
    colorFile.write(".white {\n\tbackground-color: white;\n color: black;\n}\n")
    colorFile.write(".aquamarine {\n\tbackground-color: aquamarine;\ncolor: black;\n}\n")
    colorFile.write(".cyan {\n\tbackground-color: cyan;\ncolor: black;\n}\n")
    colorFile.write(".royalblue {\n\tbackground-color: royalblue;\ncolor: black;\n}\n")
    colorFile.write(".blue {\n\tbackground-color: blue;\ncolor: white;\n}\n")
    colorFile.write(".darkblue {\n\tbackground-color: darkblue;\ncolor: white;}\n")
    colorFile.write("</style>\n</head>\n")

    # Write content
    colorFile.write("<body>\n<p>\n")
    length = len(model)
    for i in range(length-1):
        # Get text
        start = model[i][0]
        end = model[i+1][0]
        line=""
        for current in content[start:end]:
            line+=current + " "

        # Get color
        revid=model[i][1]
        if revid==None:
        	color="white"
        else:
        	color = colors[model[i][1]]
    	colorFile.write("<span class="+ color+ ">"+line+"</span>\n")

    colorFile.write("</p>\n</body>\n</html>")
    colorFile.close()
    print "writeColors done"

def wiki2centrality(title, remove):
	"""
	"""
	model,content=bw.wiki2snap(title, remove)
	centralityDict = centrality("edgelists/" + title.replace(" ", "_") + ".txt")
	colors = colorPercentile(model, centralityDict)
	writeColors(title, model, content, colors)




def parse_args():
    """parse_args parses sys.argv for wiki2centrality."""
    # Help Menu
    parser = optparse.OptionParser(usage='%prog [options] title')
    parser.add_option('-r', '--remove',
                      action='store_false', dest='remove', default=True,
                      help='remove mass deletions')

    (opts, args) = parser.parse_args()

    # Parser Errors
    if len(args) != 1:
        parser.error('incorrect number of arguments')

    wiki2centrality(args[0], remove=opts.remove)


if __name__ == '__main__':
    parse_args()
