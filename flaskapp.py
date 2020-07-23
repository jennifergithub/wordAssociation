from flask import Flask, redirect, url_for
from flask import request
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import random

app = Flask(__name__)
tokenizer = RegexpTokenizer(r'\w+')

@app.route("/word", methods=["GET"])
def findWord():
    word = request.args.get('word')
    while True:
        try:
            synonyms = []
            syns = wordnet.synsets(word)
            random_syns = random.choice(syns)
            defined = random_syns.definition()
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    if l.name().lower() != word.lower() and len(l.name())>1 and len(l.name())<20:
                        synonyms.append(l.name())
            if len(synonyms) == 0:
                stop_words = set(stopwords.words("english"))
                words = tokenizer.tokenize(defined)
                filtered_definition = [w for w in words if not w in stop_words]
                synonyms.append(random.choice(filtered_definition))

            result_list = list(dict.fromkeys(synonyms))
            result = random.choice(result_list)
            final_result = result.replace("_", " ")
            #return(str(final_result))
            myhtml = "<head><link rel='stylesheet' type='text/css' title='regular' href='styles1.css' /><link rel='alternate stylesheet' type='text/css' title='sunset' href='sunset.css'/></head><form action='http://localhost:2000/word' method='get' id='form-altered' style='text-align: center;'><input type='text' name='word' id='word' style='width: 20vw; height: 6vh; padding: 3px; font-size: 2em; margin: 2px;' /><input type='submit' id='submit-form' style='cursor: pointer; padding: 5px; font-size: 1.2em;' /><br><br><label style='font-size: 2em; font-family: Georgia, 'Times New Roman', Times, serif;'>"+str(final_result)+"</label></form>"
            return myhtml
        except:
            myhtml = "<head><link rel='stylesheet' type='text/css' title='regular' href='styles1.css' /><link rel='alternate stylesheet' type='text/css' title='sunset' href='sunset.css'/></head><form action='http://localhost:2000/word' method='get' id='form-altered' style='text-align: center;'><input type='text' name='word' id='word' style='width: 20vw; height: 6vh; padding: 3px; font-size: 2em; margin: 2px;' /><input type='submit' id='submit-form' style='cursor: pointer; padding: 5px; font-size: 1.2em;' /><br><br><label style='font-size: 2em; font-family: Georgia, 'Times New Roman', Times, serif;'>" + str("Try again!")+ "</label></form>"
            return(myhtml)

app.run(debug=True, host="0.0.0.0", port=80)
