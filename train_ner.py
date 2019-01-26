#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data
TRAIN_DATA = [
    ("Alfonso XIII of Spain's birth place is Madrid.", {"entities": [(0, 21, "SUB"), (39, 45, "OBJ")]}),
    ("Herman Melville's death place is Los Angeles.", {"entities": [(0, 15, "SUB"), (33, 44, "OBJ")]}),
    ("Jack Faust (novel) stars Michael Swanwick.", {"entities": [(0, 18, "SUB"), (25, 41, "OBJ")]}),
    ("Philadelphia 76ers is Kyle Korver's squad.", {"entities": [(0, 18, "OBJ"), (22, 33, "SUB")]}),
    ("Portugal is Mário Soares' role.", {"entities": [(0, 8, "OBJ"), (12, 24, "SUB")]}),
    ("Godzilla (1998 film) stars Harry Shearer.", {"entities": [(0, 20, "SUB"), (27, 40, "OBJ")]}),
    ("Pär Lagerkvist's award is Nobel Prize in Physics.", {"entities": [(0, 14, "SUB"), (26, 37, "OBJ"), (41, 48, "OBJ")]}),
    ("Stephen Dunham's team is Alexondra Lee.", {"entities": [(0, 14, "SUB"), (25, 38, "OBJ")]}),
    ("The Right Stuff (film) stars Ed Harris.", {"entities": [(0, 22, "SUB"), (29, 38, "OBJ")]}),
    ("Henry Wadsworth Longfellow's death place is Nashville, Tennessee.", {"entities": [(0, 26, "SUB"), (44, 53, "OBJ"), (55, 64, "OBJ")]}),
    ("Nobel Prize in Literature is Maurice Maeterlinck's honour.", {"entities": [(0, 11, "OBJ"), (15, 25, "OBJ"), (29, 48, "SUB")]}),
    ("Enrique O'Donnell, Conde del Abisbal's death place is Cádiz.", {"entities": [(0, 17, "SUB"), (19, 36, "SUB"), (54, 59, "OBJ")]}),
    ("L. Sprague de Camp's death place is Archer, Florida.", {"entities": [(0, 18, "SUB"), (36, 42, "OBJ"), (44, 51, "OBJ")]}),
    ("Savannah, Georgia is Johnny Mercer's nascence place.", {"entities": [(0, 8, "OBJ"), (10, 17, "OBJ"), (21, 34, "SUB")]}),
    ("H. H. Asquith's office is Belgium.", {"entities": [(0, 13, "SUB"), (26, 33, "OBJ")]}),
    ("Shogo's spouse is Eriko Imai.", {"entities": [(0, 5, "SUB"), (18, 28, "OBJ")]}),
    ("A Hard Day's Night (film) stars Lacey Chabert", {"entities": [(0, 25, "SUB"), (32, 44, "OBJ")]}),

]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir="ner_model/", n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )


    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]