
from flask import Flask, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/modalites')
def modalites():
    with open('modalites.html', 'r', encoding='utf-8') as f:
        return f.read()

import requests

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'ville': request.form['ville'],
        'nom': request.form['nom'],
        'fonction': request.form['fonction'],
        'email': request.form['email'],
        'telephone': request.form['telephone']
    }

    # URL de ton Google Apps Script :
    webhook_url = "https://script.google.com/macros/s/AKfycbwGyzuJMJki7nUfJUpRyPO31LPmyx9b8pbd_LQCStGI0cpegTPXVrlMerV2rW_Thv7Zuw/exec"

    try:
        requests.post(webhook_url, data=data)
    except Exception as e:
        print("Erreur lors de l’envoi vers Google Sheets :", e)

    return redirect('/merci')


@app.route('/merci')
def merci():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Merci !</title>
      <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
      <style>
        body {
          margin: 0;
          background-color: #FF0000;
          font-family: 'Varela Round', sans-serif;
          color: white;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          text-align: center;
        }
        .logo {
          position: absolute;
          top: 20px;
          right: 20px;
          width: 100px;
        }
        h1 {
          font-size: 2em;
        }
      </style>
    </head>
    <body>
      <img src="/static/schleich_logo.png" alt="Logo Schleich" class="logo">
      <h1>Merci pour votre participation 🦍</h1>
    </body>
    </html>
    """

@app.route('/tirage')
def tirage():
    import random
    with open('participants.csv', encoding='utf-8') as f:
        participants = list(csv.reader(f))
    if not participants:
        return "<h1>Aucune participation enregistrée</h1>"
    gagnant = random.choice(participants)
    return f"<h1>Le gagnant est : {gagnant[1]} de {gagnant[0]} !</h1>"

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
