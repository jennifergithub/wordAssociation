from flask import Flask
from flask import request
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import random

app = Flask(__name__)

@app.route("/word", methods=["GET"])
def findWord():
    tokenizer = RegexpTokenizer(r'\w+')
    word = request.args.get('word')
    while True:
        try:
            synonyms = []
            syns = wordnet.synsets(word)
            random_syns = random.choice(syns)
            defined = random_syns.definition()
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    if l.name() != word:
                        synonyms.append(l.name())
            if len(synonyms) == 0:
                stop_words = set(stopwords.words("english"))
                words = tokenizer.tokenize(defined)
                filtered_definition = [w for w in words if not w in stop_words]
                synonyms.append(random.choice(filtered_definition))

            result_list = list(dict.fromkeys(synonyms))
            result = random.choice(result_list)
            final_result = result.replace("_", " ")
            return(str(final_result))
        except Exception as e:
            return(str(e))

app.run(host="0.0.0.0", port=4000)
