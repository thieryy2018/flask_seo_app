import os
import openai
import config

openai.api_key = config.OPENAI_API_KEY

def reWriter(text):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Improve this piece of content: {} Keep the number of words about the same. Make it concise and engaging.".format(text),
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    if 'choices' in response:
        if len (response.choices) > 0:
            answer = response.choices[0].text.strip().split("\n")
        
    else:
        answer = ['Error: Nothing was entered.']

    return answer
