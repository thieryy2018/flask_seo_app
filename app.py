from flask import Flask, render_template, request
import config
import re
import metatitle

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
