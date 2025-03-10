from flask import Flask, request, render_template_string
from flask_basicauth import BasicAuth
from textblob import TextBlob
import os


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)


@app.route('/')
# @basic_auth.required
def home():
    return render_template_string('''
        <h1>Análise de Sentimento</h1>
        <form action="/sentimento" method="post">
            <label for="frase">Digite uma frase:</label>
            <input type="text" id="frase" name="frase">
            <input type="submit" value="Analisar Sentimento">
        </form>
    ''')


# Rota para calcular a polaridade do texto
@app.route('/sentimento', methods=['POST'])
def sentimento():
    frase = request.form['frase']
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity
    return "Polaridade: {}".format(polaridade)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
