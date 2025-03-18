from flask import Flask, request, render_template
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
    return render_template('home.html')


# Rota para calcular a polaridade do texto
@app.route('/sentimento', methods=['POST'])
def sentimento():
    frase = request.form['frase']
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity

    # Renderize o template de resultado passando a frase e a polaridade
    return render_template('sentimento.html', frase=frase,
                           polaridade=polaridade)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
