factURI = "<http://swc2017.aksw.org/task2/dataset/"
propURI = "<http://swc2017.aksw.org/hasTruthValue>"
valueType = "^^<http://www.w3.org/2001/XMLSchema#double> ."

def write_to_file(factID, truth_value):
    line = factURI + str(factID) + "> " + propURI + " \"" + str(truth_value) + "\" " + valueType
    with open('result.ttl', 'a') as file:
        file.write(line+'\n')