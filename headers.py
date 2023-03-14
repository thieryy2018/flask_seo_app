import os
import openai
import config

openai.api_key = os.environ['OPENAI_API_KEY']

def genHeaders(title, keyword):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Using the keyword {}, create a list of search-engine optimised H2 and H3 titles (please state these next to each suggestion) for a blog post titled {} with a brief description underneath each title about what should be included, using semantic keywords and avoiding American spelling, words or phrases.".format(keyword, title),
        temperature=0.7,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    if 'choices' in response:
        if len (response.choices) > 0:
            answer = response.choices[0].text.strip().split("\n")
        
    else:
        answer = ['Error: Nothing was entered.']

    return answer
