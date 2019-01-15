factURI = "<http://swc2017.aksw.org/task2/dataset/"
propURI = "<http://swc2017.aksw.org/hasTruthValue>"
valueType = "^^<http://www.w3.org/2001/XMLSchema#double> ."

def write_as_turtle(factID, truth_value):
    elements = []
    for (f, t) in zip(factID, truth_value):
        elements.append(factURI + unicode(f, 'latin-1') + "> " + propURI + " \"" + unicode(t, 'latin-1') + "\" " + valueType)
    with open('result.ttl', 'w') as file:
        for item in elements:
            file.write("%s\n" % item)