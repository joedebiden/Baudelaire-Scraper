from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/getapi')
def get_api():
    return render_template('api.html')

@app.route('/scraper')
def scrape():
    return render_template('/scraper.html')



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)