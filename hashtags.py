import os
import openai
import config

openai.api_key = os.environ['OPENAI_API_KEY']

def hashTags(number, topic):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Find {} current, popular and trending social media hashtags for {}".format(number, topic),
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
