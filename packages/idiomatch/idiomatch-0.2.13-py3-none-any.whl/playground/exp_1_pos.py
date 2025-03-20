from spacy import load

nlp = load("en_core_web_sm")


doc = nlp("This is for him. This is his fault. This is something like that. This is your fault. Apple is great.")

for token in doc:
    print(token.text, token.pos_, token.tag_)

"""
This PRON DT
is AUX VBZ
for ADP IN
him PRON PRP
. PUNCT .
This PRON DT
is AUX VBZ
his PRON PRP$
fault NOUN NN
. PUNCT .
This PRON DT
is AUX VBZ
something PRON NN
like ADP IN
that PRON DT
. PUNCT .
This PRON DT
is AUX VBZ
your PRON PRP$
fault NOUN NN
. PUNCT .
Apple PROPN NNP
is AUX VBZ
great ADJ JJ
. PUNCT .
"""