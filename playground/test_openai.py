import openai
from pprint import pprint

import sys
import os

#  https://www.geeksforgeeks.org/python-import-from-parent-directory/
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from lib.utils import load_config, setup_log
from lib.chat import MyBotWrapper
from lib.parser import *

# config = load_config()

# openai.api_key = config['api_key']
# Set the OPENAI_API_KEY environment variable to your key

model = 'gpt-3.5-turbo-0301'
model = 'gpt-3.5-turbo'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def test_hello():
    prompt = "Hello"
    response = get_completion(prompt, model=model)
    print(f"prompt: {prompt}\nresponse: {response}")

    
def test_summarize():
    text = f"""
    You should express what you want a model to do by \ 
    providing instructions that are as clear and \ 
    specific as you can possibly make them. \ 
    This will guide the model towards the desired output, \ 
    and reduce the chances of receiving irrelevant \ 
    or incorrect responses. Don't confuse writing a \ 
    clear prompt with writing a short prompt. \ 
    In many cases, longer prompts provide more clarity \ 
    and context for the model, which can lead to \ 
    more detailed and relevant outputs.
    """
    prompt = f"""
    Summarize the text delimited by triple backticks \ 
    into a single sentence.
    ```{text}```
    """
    response = get_completion(prompt, model=model)
    print(response)
    

def test_sentence_generation():
    parser = SentGenParser()
    bot = MyBotWrapper(parser=parser, model=model, temperature=0.9)
    # inputs={"word": "account", "tag": "VBZ"}
    # inputs={"word": "constitute", "tag": "VBD"}
    # inputs={"word": "account", "tag": "NN"}
    inputs={"word": "approaches", "tag": "VBZ"}
    res = bot.run(inputs=inputs)



def test_derivatives():
    parser = DerivativeParser()
    bot = MyBotWrapper(parser=parser, model=model, temperature=0.1)
    # inputs={"word": "account", "tag": "NN"}
    # res = bot.run(inputs=inputs)
    # inputs={"word": "account", "tag": "VBZ"}
    inputs={"word": "account"}
    res = bot.run(inputs=inputs)


def test_rational():
    parser = RationalParser()
    bot = MyBotWrapper(parser=parser, model=model, temperature=0)
    inputs={
        "words": ["constitute", "distribute", "export", "issue", "occur", "good"], 
        "sentence": "The actions of the defendant _____ a breach of contract.",
        }
    # inputs={
    #     "words": ["account", "bank", "export", "issue", "occur", "good"], 
    #     "sentence": "I have an ____ with the bank.",
    #     }
    r = bot.run(inputs=inputs)
    pprint(r.get('result'))

def test_rational_more():
    word = "function"
    word = "constitute"
    word = "occur"
    word = "consist"
    sentence = f"The results ____ a strong correlation between the two variables in the study."
    sentence = f"The data ____ a significant correlation between exercise and mental health in this study."
    prompt = f"""Is this sentence semantically correct, if the word {word} is fit into the sentence: {sentence}"""
    prompt = f"""Is the syntax of the sentence correct, if the word {word} is fit into the sentence: {sentence}"""
    
#     prompt = """For each of the following words separated by a comma, \
# when the word is fit into the blank in the masked sentence, \
# if the syntactic structure of the sentence is correct yield true for ""syntax"", \
# if the semantic meaning of the sentence is correct yield true for "semantics".
# Words: ```benefit, proceed, approach, section, research, consist, issue, derive```
# Masked sentence: ```The data ____ a significant correlation between exercise and mental health in this study.```
# ---
# Answer in the following JSON structure:
# {
#   "word 1": {"syntax": true, "semantics": true},
#   "word 2": {"syntax": true, "semantics": false}
# }
# """
    r = get_completion(prompt)
    print(prompt)
    print('-'*20)
    print(r)
    
def test_compare_grammar_syntax():
    
    def test_with(pov = 'syntax'):
        # words = 'benefit, proceed, approach, section, research, consist, issue, derive'
        # sent = 'The data ____ a significant correlation between exercise and mental health in this study.'
        words = 'account, bank, apple'
        sent = 'I have an ____ with the bank.'
        prompt = f"""For each of the following words separated by a comma, \
when the word is fit into the blank in the masked sentence, \
if the {pov} of the sentence is correct yield true for "{pov}", \
if the semantic meaning of the sentence is correct yield true for "semantics".
Words: ```{words}```
Masked sentence: ```{sent}```
---
Answer in the following JSON structure:
{{
  "word 1": {{"{pov}": true, "semantics": true}},
  "word 2": {{"{pov}": true, "semantics": false}}
}}
"""    
        print(prompt)
        r = get_completion(prompt)
        print('-'*10)
        print(r)
        print('-'*20)
    
    test_with('syntax')
    test_with('grammar')

if __name__ == '__main__':
    setup_log()
    test_hello()
    # test_summarize()
    # test_sentence_generation()
    # test_derivatives()
    # test_rational()
    # test_rational_more()
    # test_compare_grammar_syntax()
    