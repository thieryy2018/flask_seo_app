import os
import openai
import config

openai.api_key = os.environ['OPENAI_API_KEY']

def metaTitle(number, brand, keyword):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Create {} clear, concise and descriptive meta title(s) for the brand {} using the keyword {}. The response should use the brand first, be more than 50 text characters in length, but less than 70 text characters in length. Its important not to repeat words, especially the brand or keyword entered. Use Google to get ideas for similar meta titles.".format(number, brand, keyword),
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
