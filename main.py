from flask import Flask, render_template, request, redirect, url_for
import urllib3
from bs4 import BeautifulSoup

app = Flask(__name__)

# extract data
def no_script_no_style(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'html.parser')

    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    return soup


# render page
@app.route('/', methods=['GET', "POST"])
def index():
    # POST
    if request.method == 'POST':
        url = request.form['nsns-url']
        return redirect(url_for('index', url=url))

    # GET
    url = request.args.get('url')
    if url is None or len(url)==0:
        return render_template('index.html', url=None, content=None)
    else:
        soup = no_script_no_style(url)
        return render_template('index.html', url=url, content=soup)


if __name__ == "__main__":
    app.run(debug=True)