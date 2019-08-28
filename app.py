import os
from flask import Flask, request, render_template
from lime_explainer import explainer, tokenizer, METHODS

app = Flask(__name__)
SECRET_KEY = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def explain():
    if request.method == 'POST':
        text = tokenizer(request.form['entry'])
        method = request.form['classifier']
        n_samples = request.form['n_samples']
        if any(not v for v in [text, n_samples]):
            raise ValueError("Please do not leave text fields blank.")

        exp = explainer(method,
                        path_to_file=METHODS[method]['file'],
                        text=text,
                        num_samples=int(n_samples))
        exp = exp.as_html()

        return render_template('result.html', exp=exp)
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True)
