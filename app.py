from flask import Flask, render_template, request, session, jsonify
import config
import re
import metatitle
import metadescription
import productdescription
import hashtags
import blogtitles
import rewriter
import semantic
import headers
from bs4 import BeautifulSoup
import openai
import json
import os
from typing import Union


def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

#Chatbot functions start ------->

def get_api_response(prompt: str) -> Union[str, None]:
    text: str | None = None

    try:
        response: dict = openai.Completion.create (
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']

        )
        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


#def main():
    prompt_list: list[str] = ['You are a potato and will answer as a potato',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a potato!']

    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, prompt_list)
        print(f'Bot: {response}')

# Chatbot functions -----> End

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())

@app.route('/highlighter', methods=["GET", "POST"])
def highlighter():
    if request.method == 'POST':
        # Check if main-text value is missing or empty
        if 'main-text' not in request.form or not request.form['main-text']:
            error_msg = 'Please enter some text in the Main Text field'
            return render_template('highlighter.html', error_msg=error_msg)
       
        keyword_list = request.form['keyword-list']
        # Check if keyword list value is missing or empty
        if not keyword_list:
            error_msg = 'Please enter some keywords in the Keyword List field'
            return render_template('highlighter.html', error_msg=error_msg)

        main_text = request.form['main-text']
        keyword_list = request.form['keyword-list'].split(',')
        url = request.form.get('url', '')

        for keyword in keyword_list:
            regex = rf'\b({keyword})\b'
            main_text = re.sub(regex, f'<span class="highlight"><a href="{url}">{keyword}</a></span>', main_text, flags=re.IGNORECASE)
       
        return render_template('highlighter.html', main_text=main_text, keyword_list=keyword_list, url=url)
   
    return render_template('highlighter.html')


@app.route('/meta-title', methods=["GET", "POST"])
def metaTitle():

    if request.method == 'POST':
        number = request.form['number']
        brand = request.form['brand']
        keyword = request.form['keyword']
       
        openAIAnswer = metatitle.metaTitle(number, brand, keyword)

        prompt = 'Here are {} meta title(s) for your chosen brand, {}, using the keyword {}:'.format(number, brand, keyword)

    return render_template('meta-title.html', **locals())

@app.route('/meta-description', methods=["GET", "POST"])
def metaDescription():

    if request.method == 'POST':
        number = request.form['number']
        brand = request.form['brand']
        keyword = request.form['keyword']
       
        openAIAnswer = metadescription.metaDescription(number, brand, keyword)

        prompt = 'Here are {} meta description ideas for your chosen brand, {}, using the keyword {}:'.format(number, brand, keyword)

    return render_template('meta-description.html', **locals())

@app.route('/product-description', methods=["GET", "POST"])
def productDescription():

    if request.method == 'POST':
        brand = request.form['brand']
        product = request.form['product']
        keyword = request.form['keyword']
       
       
        openAIAnswer = productdescription.productDescription(brand, product, keyword)

        prompt = 'Here is an Ai generated product description using the brand name, {} for a product called {}, using the keyword {}:'.format(brand, product, keyword)

    return render_template('product-description.html', **locals())

@app.route('/hash-tags', methods=["GET", "POST"])
def hashTags():

    if request.method == 'POST':
        number = request.form['number']
        topic = request.form['topic']
       
        openAIAnswer = hashtags.hashTags(number, topic)

        prompt = 'Here are {} hashtags for: {}'.format(number, topic)

    return render_template('hash-tags.html', **locals())

@app.route('/blog-titles', methods=["GET", "POST"])
def blogPosts():

    if request.method == 'POST':
        number = request.form['number']
        industry = request.form['industry']
        keyword = request.form['keyword']
       
        openAIAnswer = blogtitles.blogPosts(number, industry, keyword)

        prompt = 'Here are {} blog post title suggestions for: {}'.format(number, keyword)

    return render_template('blog-titles.html', **locals())

@app.route('/rewriter', methods=["GET", "POST"])
def reWriter():

    if request.method == 'POST':
        text = request.form['text']
       
        openAIAnswer = rewriter.reWriter(text)

        prompt = 'Here is your new and improved content. '.format()

    return render_template('rewriter.html', **locals())

@app.route('/semantic-keywords', methods=["GET", "POST"])
def semanticKeywords():

    if request.method == 'POST':
        number = request.form['number']
        keyword = request.form['keyword']
       
        openAIAnswer = semantic.semanticKeywords(number, keyword)

        prompt = 'Here are {} semantic keywords for the keyword: {}. '.format(number, keyword)

    return render_template('semantic-keywords.html', **locals())

@app.route('/headers', methods=["GET", "POST"])
def genHeaders():

    if request.method == 'POST':
        title = request.form['title']
        keyword = request.form['keyword']
       
        openAIAnswer = semantic.semanticKeywords(title, keyword)

        prompt = 'Suggested Headers: '.format()

    return render_template('headers.html', **locals())

#Chatbot routes:
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form["message"]
    response = get_bot_response(message, prompt_list)
    return jsonify({"response": response})

@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    global prompt_list
    prompt_list = ['You are an SEO expert and will answer as an SEO expert. Your name is Mr Neural Edge - king of data-driven SEO.',
                   '\nHuman: What is SEO?',
                   '\nAI: SEO stands for Search Engine Optimization. It is a process of optimizing a website to rank higher in search engine result pages, which helps attract more targeted visitors to a website. SEO involves creating content and building links that are relevant to the topic of the website in order to increase its visibility in search engine results.']
    return jsonify({"success": True})

#Chatbot flask routes end

if __name__ == '__main__':
    prompt_list = ['You are an SEO expert and will answer as an SEO expert. Your name is Mr Neural Edge - king of data-driven SEO.',
                   '\nHuman: What is SEO?',
                   '\nAI: SEO stands for Search Engine Optimization. It is a process of optimizing a website to rank higher in search engine result pages, which helps attract more targeted visitors to a website. SEO involves creating content and building links that are relevant to the topic of the website in order to increase its visibility in search engine results.']
    app.run(debug=True)

