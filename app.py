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

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.register_error_handler(404, page_not_found)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
