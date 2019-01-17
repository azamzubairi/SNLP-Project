import csv
import StringIO
import spacy
import WikipediaExtractor
import write_to_file

nlp = spacy.load('xx_ent_wiki_sm')

with open("train.tsv") as file:
    results = file.read()
    data = list(csv.DictReader(StringIO.StringIO(results), delimiter='\t'))

for entities in data:

    fact_id = entities['FactID']
    fact_statement = entities['Fact_Statement']

    text = unicode(fact_statement, 'latin-1')
    doc = nlp(text)
    ents = [e.text for e in doc.ents]

    if e.label_ == "PER" or e.label_ == "ORG":
        dic = WikipediaExtractor.get_term_dict(e.text, ents)
        truth_value = WikipediaExtractor.check_existence(dic)
        write_to_file.write_to_file(fact_id, truth_value)
        print truth_value
