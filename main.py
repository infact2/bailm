import random
import language_tool_python
import os
import requests
from flask import Flask, request, send_file

app = Flask(__name__)

tool = language_tool_python.LanguageToolPublicAPI('en-US')

data_raw = []
data = {}
sentence_starters = []
ic_punctation = ".;:?!"
remove_char = "@#$%^&*()<>{}[],/\\\"=_+"
depunctated_replacement = "DUDEPLEASEREMOVE"

training_file = "training.txt"


def compileAndAddSequence(string):
    depunctuated = string.lower()
    for char in ic_punctation:
        # char = punctation[i]
        depunctuated = depunctuated.replace(char, depunctated_replacement)
    
    for char in remove_char:
        # char = punctation[i]
        depunctuated = depunctuated.replace(char, "")
    
    for i in depunctuated.split(depunctated_replacement):
        data_raw.append(i)

def processData():
    for i in data_raw:
        sequence = i.split()
        for token_index in range(len(sequence)):
            token = sequence[token_index]

            if not token in data:
                data[token] = []

            has_next = token_index + 1 < len(sequence)
            if has_next:
                data[token].append({"occurences": 1, "word": sequence[token_index + 1]});
        if len(sequence) > 0:
            sentence_starters.append(sequence[0])

def randomToken():
    return random.choice(sentence_starters)

def generateSequence(starting_token, remaining_sentences):
    if remaining_sentences == 0:
        return ""

    # print(starting_token)

    next_token = ""
    try:
        if starting_token in data:
            max_occurences = 1

            next_possible_tokens = data[starting_token]
            next_tokens = []
            for i in next_possible_tokens:
                max_occurences = max(max_occurences, i["occurences"])

            for i in next_possible_tokens:
                if i["occurences"] == max_occurences:
                    next_tokens.append(i["word"])
            
            if len(next_tokens) == 0:
                next_starting_token = randomToken()
                return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1)
            next_token = random.choice(next_tokens)
        else:
            next_starting_token = randomToken()
            return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1)
        # print(next_token, end=" ")
        return starting_token + " " + generateSequence(next_token, remaining_sentences)
    except Exception as error:
        print(error.args)
        return ""

def publicFile(filename):
    return os.path.join("public", filename)

# LOAD TRAINING DATA

compileAndAddSequence(open(training_file, "r", encoding="utf8").read())
processData()

@app.route("/<path>")
def balls(path):
    return send_file(publicFile(path))

@app.route("/")
def index():
    return send_file(publicFile("index.html"))

@app.route("/generate/<starting_tokens>", methods=["POST"])
def generate(starting_tokens):
    print(starting_tokens)
    tokens_raw = starting_tokens.lower()
    tokens = tokens_raw.split();
    # print(tokens_raw, end=" ")
    output = ""
    for i in range(len(tokens) - 1):
        output += tokens[i] + " "
    output += generateSequence(tokens[len(tokens) - 1], 3)
    output = tool.correct(output)
    # print(grammar_check.correct(output, tool.check(output)))
    print(output)
    return output
    
if __name__ == '__main__':
   app.run(debug = True)