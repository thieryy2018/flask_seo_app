from flask import Flask, render_template, request, session
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


def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)

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

# initialize conversation history
history = ""
messages = []

@app.route('/chatbot')
def chat():
    return render_template('chatbot.html', messages=messages)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    global history, messages
    
    message = request.form['message']
    print("User Message:", message)
    messages.append(message)
    
    # generate bot response
    prompt = message + "\n"
    completion = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.3,
    stop= "."

    )

    bot_response = completion.choices[0].text.strip()
    print("Bot Response:", bot_response)
    messages.append(bot_response)

    history += "User: " + message + "\n" + "AI: " + bot_response + "\n"

    
    # render the chat window with the updated conversation history
    return render_template('chatbot.html', messages=messages)

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    global history, messages
    
    # reset conversation history
    history = ""
    messages = []
    # clear messages list
    messages.clear()

    print("History cleared: ", history)
    print("Messages cleared: ", messages)
    
    # redirect to the chat page
    return redirect('/chatbot')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=False)
