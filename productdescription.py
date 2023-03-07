import os
import openai
import config

openai.api_key = os.environ['OPENAI_API_KEY']

def productDescription(number, brand, keyword):

    response = openai.Completion.create(
    model="text-davinci-003",
        prompt="Write a clear, concise and descriptive SEO 200 word product description by the brand name for {}. The product is called {} and the description should feature the keyword: {}. Do not repeat the brand, product or keyword. Use Google to get ideas for similar product descriptions and the features. I encourage you to use lists such as bullet points. No american phrases.".format(number, brand, keyword),
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    if 'choices' in response:
        if len (response.choices) > 0:
            answer = response.choices[0].text
        
    else:
        answer = ['Error: Nothing was entered.']

    return answer
