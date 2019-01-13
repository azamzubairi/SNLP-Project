import csv
import StringIO
import spacy




nlp = spacy.load('xx_ent_wiki_sm')


with open("/Users/azamzubairi/Downloads/train.tsv") as file:
    results = file.read()
    data = list(csv.DictReader(StringIO.StringIO(results), delimiter='\t'))

for entities in data:

    fact_id = entities['FactID']
    fact_statement = entities['Fact_Statement']

    text = unicode(fact_statement, 'latin-1')
    doc = nlp(text)
    ents = [(e.text, e.label_) for e in doc.ents]
    print(ents)














