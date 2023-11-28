import random
import language_tool_python
import os
import requests
import base64
from flask import Flask, request, send_file

app = Flask(__name__)

tool = language_tool_python.LanguageToolPublicAPI('en-US')

ic_punctation = ".;:?!"
remove_char = "@#$%^&*()<>{}[],/\\\"=_+"
depunctated_replacement = "DUDEPLEASEREMOVE"

margin = 2;

training_file = "training.txt"
document_data = {}


def compileAndAddSequence(string):
    data_raw = []
    depunctuated = string.lower()
    for char in ic_punctation:
        # char = punctation[i]
        depunctuated = depunctuated.replace(char, depunctated_replacement)
    
    for char in remove_char:
        # char = punctation[i]
        depunctuated = depunctuated.replace(char, "")
    
    for i in depunctuated.split(depunctated_replacement):
        data_raw.append(i)

    return data_raw

def processData(document_name):
    if document_name in document_data:
        return

    data_raw = ""
    try:
        data_raw = compileAndAddSequence(open(document_name, "r", encoding="utf8").read())
    except:
        print("bruh kys")
        return

    data = {}
    sentence_starters = []

    for i in data_raw:
        sequence = i.split()
        for token_index in range(len(sequence)):
            token = sequence[token_index]

            if not token in data:
                data[token] = []

            has_next = token_index + 1 < len(sequence)
            if has_next:
                next = sequence[token_index + 1]
                next_index = -1
                for i in range(len(data[token])):
                    if data[token][i]["word"] == next:
                        next_index = i
                if next_index == -1:
                    data[token].append({"occurences": 1, "word": next})
                else:
                    data[token][next_index]["occurences"] += 1
        if len(sequence) > 0:
            sentence_starters.append(sequence[0])


    document_data[document_name] = {"data": data, "sentence_starters": sentence_starters}
    print(f"Successfully processed ${document_name}")

def randomToken(document_name):
    return random.choice(document_data[document_name]["sentence_starters"])

def generateSequence(starting_token, remaining_sentences, document_name):
    processData(document_name)

    if remaining_sentences == 0:
        return ""

    # print(starting_token)

    next_token = ""
    data = document_data[document_name]["data"]
    try:
        if starting_token in data:
            max_occurences = 1

            next_possible_tokens = data[starting_token]
            next_tokens = []
            for i in next_possible_tokens:
                max_occurences = max(max_occurences, i["occurences"])

            for i in next_possible_tokens:
                if i["occurences"] >= max_occurences - margin:
                    next_tokens.append(i["word"])
            
            if len(next_tokens) == 0:
                next_starting_token = randomToken(document_name)
                return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1, document_name)
            next_token = random.choice(next_tokens)
        else:
            next_starting_token = randomToken(document_name)
            return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1, document_name)
        # print(next_token, end=" ")
        return starting_token + " " + generateSequence(next_token, remaining_sentences, document_name)
    except Exception as error:
        print(error.args)
        return ""

def publicFile(filename):
    return os.path.join("public", filename)




@app.route("/<path>")
def balls(path):
    return send_file(publicFile(path))

@app.route("/")
def index():
    return send_file(publicFile("index.html"))

@app.route("/preview/<content>")
def preview(content):
    print("iuowerghiuergipuhebgwbiobihogrihuerwuebopufdgtvr8yobtrhju")
    decoded_content = base64.b64decode(content).decode()
    return f"<style>@import url('https://fonts.googleapis.com/css2?family=Inconsolata:wght@400;700&family=Roboto:ital,wght@0,300;0,700;1,300;1,700&display=swap'); body {'{ padding: 30px; line-height: 2em; font-family: \'Inconsolata\'; }'} </style><h2>Preview</h2>------------------------<br><br>&nbsp;&nbsp;&nbsp;&nbsp;{decoded_content}";

@app.route("/generate/<starting_tokens>/<int:sentences>/<document_name>", methods=["POST"])
def generate(starting_tokens, sentences, document_name):

    print(starting_tokens)
    tokens_raw = starting_tokens.lower()
    tokens = tokens_raw.split();
    # print(tokens_raw, end=" ")
    output = ""
    for i in range(len(tokens) - 1):
        output += tokens[i] + " "
    output += generateSequence(tokens[len(tokens) - 1], sentences, document_name)
    output = tool.correct(output)
    # print(grammar_check.correct(output, tool.check(output)))
    print(output)
    return output
    
if __name__ == '__main__':
#    app.run(debug = True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)