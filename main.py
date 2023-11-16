import random
import language_tool_python

tool = language_tool_python.LanguageToolPublicAPI('en-US')

data_raw = []
data = {}
all_tokens = []
punctation = ",.<>/?;:\"[]\\{}|`~=_+!@#$%^&*()\n"
depunctated_replacement = "PLEASEREMOVETHISSHIT"

def compileAndAddSequence(string):
    depunctuated = string.lower()
    for char in punctation:
        # char = punctation[i]
        depunctuated = depunctuated.replace(char, depunctated_replacement)
    
    for i in depunctuated.split(depunctated_replacement):
        data_raw.append(i)

def processData():
    for i in data_raw:
        sequence = i.split()
        for token_index in range(len(sequence)):
            token = sequence[token_index]

            if not token in data:
                data[token] = []
                all_tokens.append(token)

            has_next = token_index + 1 < len(sequence)
            if has_next:
                data[token].append({"occurences": 1, "word": sequence[token_index + 1]});
    # print(data)

def randomToken():
    return random.choice(all_tokens)

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
                # print(". ", end="")
                # print("KILLYOURSELFNOWooooooooooooo!!!!!!")
                next_starting_token = randomToken()
                # print("KILLYOURSELFNOW!!!!!!")
                # print(next_starting_token, end=" ")
                return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1)
            next_token = random.choice(next_tokens)
        else:
            # print(". ", end="")
            # print("KILLYOURSELFNOWooooooooooooo!!!!!!")
            next_starting_token = randomToken()
            # print("KILLYOURSELFNOW!!!!!!")
            # print(next_starting_token, end=" ")
            return starting_token + ". " + generateSequence(next_starting_token, remaining_sentences - 1)
        # print(next_token, end=" ")
        return starting_token + " " + generateSequence(next_token, remaining_sentences)
    except Exception as error:
        print(error.args)
        # print(".", end="")
# def processSequence(sequence):
#     re

compileAndAddSequence(open("stuff.txt", "r").read())
processData()

while True:
    print("Input starting token: ", end="")
    tokens_raw = input()
    print("=============================\n")
    # print(tokens_raw, end=" ")
    output = generateSequence(tokens_raw, 5)
    # print(grammar_check.correct(output, tool.check(output)))
    print(tool.correct(output))
    print("\n=============================")

    
