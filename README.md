# SNLP Fact Checker

Build a corpus-driven fact-checking engine, which returns a confidence
value between -1 (fact is false) and +1 (fact is true) given a fact from
DBpedia

## Appraoch
- Load a custom model we have trained for NER (to train the model we have used the [train_ner.py]) (https://github.com/explosion/spaCy/blob/master/examples/training/train_ner.py) script by Spacy).
- Extract statements from the data file.
- Feed it to the model. The model extracts Subject(SUB) and Objects(OBJ) from the statements.
- Query the extracted Subject from the statement on wikipedia and get the page text.
- Check if Objects appear in the wikipedia text.
- If all Objects appear in text then assign 1 Truth Value else assign -1 Truth Value.
- Write results in results.ttl file.

## Example

```
3333245	Charles Édouard Guillaume's award is Nobel Prize in Literature.
```
- Extracted Entities by Model:
`
[('Charles Édouard Guillaume',SUB), ('Nobel Prize',OBJ), ('Literature',OBJ)]
`
- wikipedia.search("Charles Édouard Guillaume").
- Check if `'Nobel Prize'` and `'Literature'` occur in text.
- If both occur then assign 1 else assign -1.

## Prerequisites
Python 2.7 must be installed on the system and for MacOS a virtual environment is also needed. (To create a virtual environment on Mac follow the tutorial [here](http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-mac-os-x/))

Clone or Download the repo on your system. Go to the project directory and run

```bash
pip install -r requirements.txt
```

## Usage

```python
python preprocess.py -f test.tsv
```
- Result will be written into the result.ttl file.

## Statements which fail

##### True Statements which return False

- Albert Einstein published the Thoery of Relativity.
- Wasim Akram played Cricket in Australia.
- Wright Brothers invented the airplane.
- J.K. Rowling wrote Harry Potter.
- Isaac Newton discovered gravity.

##### False Statements which return True

- Arthur Conan Doyle did not write Sherlock Holmes.
- The capital of Pakistan is Karachi.
- Cristiano Ronaldo was born in England.
- Bill Gates death place is Seattle.
- Barack Obama was born in Washington.


## Contributors
Group Name: 3 Leute
- Azam Zubairi
- Asher Ahsan
- Asjad Sohail
