import os
import openai
import config

openai.api_key = config.OPENAI_API_KEY

def blogPosts(number, industry, keyword):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Suggest {} engaging and click worthy blog post titles in the industry of {} using the keyword {}.Suggestions should include the keyword, at the beginning if possible.".format(number, industry, keyword),
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
