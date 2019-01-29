import csv
import StringIO
import spacy
import WikipediaExtractor
import write_to_file
import sys
import os

if(os.path.isfile('result.ttl')):
    os.unlink('result.ttl')


if sys.platform == 'win32':
    print("Using ner_model_windows....")
    nlp = spacy.load('ner_model_windows')
else:
    print("Using ner_model....")
    nlp = spacy.load('ner_model')

if (sys.argv[1] == '-f'):
    with open(sys.argv[2]) as file:
        results = file.read()
        data = list(csv.DictReader(StringIO.StringIO(results), delimiter='\t'))

for entities in data:

    fact_id = entities['FactID']
    fact_statement = entities['Fact_Statement']

    text = unicode(fact_statement, 'latin-1')
    doc = nlp(text)
    count = 1
    for entity in doc.ents:
        if entity.label_ == "SUB":
            ents = [e.text for e in doc.ents]
            print "Processing Statement "+str(count)
            dic = WikipediaExtractor.get_term_dict(entity.text, ents)
            truth_value = WikipediaExtractor.check_existence(dic)
            write_to_file.write_to_file(fact_id, truth_value)
            print "Statement "+str(count)+" assigned Truth Value: "+str(truth_value)
            count = count + 1


print "Total Statements processed: "+str(count)
print "Results written to result.ttl file"