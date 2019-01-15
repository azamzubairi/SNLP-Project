factURI = "<http://swc2017.aksw.org/task2/dataset/"
propURI = "<http://swc2017.aksw.org/hasTruthValue>"
valueType = "^^<http://www.w3.org/2001/XMLSchema#double> ."

with open("train.tsv") as f:
    lines = f.read().splitlines()[1:]
    f.close()

result = []

for x in lines:
    if len(x) > 0:
        lisht = x.split()
        result.append(factURI + unicode(lisht[0], 'latin-1') + "> " + propURI + " \"" + unicode(lisht[-1], 'latin-1') + "\"" + " " + valueType)

with open('result.ttl', 'w') as file:
    for item in result:
        file.write("%s\n" % item)