# %% [markdown]
# # Linguistic Features

# %% [markdown]
# Processing raw text intelligently is difficult: most words are rare, and it’s common for words that look completely different to mean almost the same thing. The same words in a different order can mean something completely different. Even splitting text into useful word-like units can be difficult in many languages. While it’s possible to solve some problems starting from only the raw characters, it’s usually better to use linguistic knowledge to add useful information. That’s exactly what spaCy is designed to do: you put in raw text, and get back a Doc object, that comes with a variety of annotations.

# %% [markdown]
# ## Part-of-speech tagging

# %% [markdown]
# After tokenization, spaCy can parse and tag a given Doc. This is where the trained pipeline and its statistical models come in, which enable spaCy to make predictions of which tag or label most likely applies in this context. A trained component includes binary data that is produced by showing a system enough examples for it to make predictions that generalize across the language – for example, a word following “the” in English is most likely a noun.
# 
# Linguistic annotations are available as Token attributes. Like many NLP libraries, spaCy encodes all strings to hash values to reduce memory usage and improve efficiency. So to get the readable string representation of an attribute, we need to add an underscore _ to its name:

# %%
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

# %%
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# %%
# POS Tagging
pos_tagging = pd.DataFrame(data=[], \
  columns=["id", "T_texto","T_lemma_", "T_pos_", "T_tag_", "T_dep_", "T_shape_", "T_is_alpha", "T_is_stop"])
i = 0
for token in doc:
    pos_tagging.loc[i,"id"] = token.i
    pos_tagging.loc[i,"T_texto"] = token.text
    pos_tagging.loc[i,"T_lemma_"] = token.lemma_
    pos_tagging.loc[i,"T_pos_"] = token.pos_
    pos_tagging.loc[i,"T_tag_"] = token.tag_
    pos_tagging.loc[i,"T_dep_"] = token.dep_
    pos_tagging.loc[i,"T_shape_"] = token.shape_
    pos_tagging.loc[i,"T_is_alpha"] = token.is_alpha
    pos_tagging.loc[i,"T_is_stop"] = token.is_stop

    i = i+1

pos_tagging

# %%
from spacy import displacy

displacy.render(doc, style='dep',
                jupyter=True, options={'distance': 120})

# %% [markdown]
# <h3>Portuguese</h3>

# %%
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_lg")

doc = nlp("Apple quer comprar startup do Reino Unido por US$ 1 bilhão")

# %%
# POS Tagging
pos_tagging = pd.DataFrame(data=[], \
  columns=["id", "T_texto","T_lemma_", "T_pos_", "T_tag_", "T_dep_", "T_shape_", "T_is_alpha", "T_is_stop"])
i = 0
for token in doc:
    pos_tagging.loc[i,"id"] = token.i
    pos_tagging.loc[i,"T_texto"] = token.text
    pos_tagging.loc[i,"T_lemma_"] = token.lemma_
    pos_tagging.loc[i,"T_pos_"] = token.pos_
    pos_tagging.loc[i,"T_tag_"] = token.tag_
    pos_tagging.loc[i,"T_dep_"] = token.dep_
    pos_tagging.loc[i,"T_shape_"] = token.shape_
    pos_tagging.loc[i,"T_is_alpha"] = token.is_alpha
    pos_tagging.loc[i,"T_is_stop"] = token.is_stop

    i = i+1

pos_tagging

# %%
from spacy import displacy

displacy.render(doc, style='dep',
                jupyter=True, options={'distance': 120})

# %% [markdown]
# ## Morphology

# %% [markdown]
# Inflectional morphology is the process by which a root form of a word is modified by adding prefixes or suffixes that specify its grammatical function but do not change its part-of-speech. We say that a lemma (root form) is inflected (modified/combined) with one or more morphological features to create a surface form. Here are some examples:

# %%
import spacy

nlp = spacy.load("pt_core_news_lg")
print("Pipeline:", nlp.pipe_names)
print()
doc = nlp("Ela estava lendo o jornal.")
token = doc[0]  # 'I'
print(token.morph)  # 'Case=Nom|Number=Sing|Person=1|PronType=Prs'
print()
print(token.morph.get("PronType"))  # ['Prs']

# %% [markdown]
# Statistical morphology

# %% [markdown]
# spaCy’s statistical Morphologizer component assigns the morphological features and coarse-grained part-of-speech tags as Token.morph and Token.pos.

# %%
import spacy

nlp = spacy.load("pt_core_news_lg")
doc = nlp("Ela estava lendo o jornal.") # English: 'Where are you?'
print(doc[2].morph)  # 'Case=Nom|Number=Sing|Person=2|PronType=Prs'
print(doc[2].pos_) # 'PRON'

# %%
token = doc[2]  # 'I'
print(token.morph)  # 'Case=Nom|Number=Sing|Person=1|PronType=Prs'
print()
print(token.morph.get("VerbForm"))

# %% [markdown]
# ## Lemmatizer

# %%
import spacy

# English pipelines include a rule-based lemmatizer
nlp = spacy.load("en_core_web_sm")

lemmatizer = nlp.get_pipe("lemmatizer")
print("Pipeline:", nlp.pipe_names)
print(lemmatizer.mode) 

# %%
doc = nlp("I was reading the paper.")
print([token.lemma_ for token in doc])

# %% [markdown]
# Portuguese

# %%
import spacy

# English pipelines include a rule-based lemmatizer
nlp = spacy.load("pt_core_news_lg")

lemmatizer = nlp.get_pipe("lemmatizer")


# %%
print("Pipeline:", nlp.pipe_names)

# %%
from spacy.pipeline.edit_tree_lemmatizer import DEFAULT_EDIT_TREE_LEMMATIZER_MODEL


# %%
config = {"model": DEFAULT_EDIT_TREE_LEMMATIZER_MODEL}
nlp.add_pipe("trainable_lemmatizer", config=config, name="lemmatizer")

# %% [markdown]
# ## Dependency Parsing

# %% [markdown]
# spaCy features a fast and accurate syntactic dependency parser, and has a rich API for navigating the tree. The parser also powers the sentence boundary detection, and lets you iterate over base noun phrases, or “chunks”. You can check whether a Doc object has been parsed by calling doc.has_annotation("DEP"), which checks whether the attribute Token.dep has been set returns a boolean value. If the result is False, the default sentence iterator will raise an exception.

# %%
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)


