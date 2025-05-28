
from flask import Flask, request, redirect
import csv
import random
import os

app = Flask(__name__)

@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/modalites')
def modalites():
    return """
<!DOCTYPE html>
<html lang='fr'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Modalités</title>
  <link href='https://fonts.googleapis.com/css2?family=Varela+Round&display=swap' rel='stylesheet'>
  <style>
    body {
      margin: 0;
      background-color: #FF0000;
      font-family: 'Varela Round', sans-serif;
      color: white;
      padding: 40px;
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
  <img src='/static/schleich_logo.png' alt='Logo Schleich' class='logo'>
  <h1>Modalités de Participation</h1>
  <p>Ce concours est ouvert aux responsables de magasins participants. Une seule participation par personne est autorisée.</p>
  <p>Les données recueillies ne seront utilisées que dans le cadre du concours et seront supprimées après tirage au sort.</p>
  <p>Le tirage au sort aura lieu le XX/XX/2025. Le gagnant sera contacté par email ou téléphone.</p>
</body>
</html>
"""

@app.route('/submit', methods=['POST'])
def submit():
    data = [
        request.form['ville'],
        request.form['nom'],
        request.form['email'],
        request.form['telephone']
    ]
    with open('participants.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
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
    try:
        with open('participants.csv', encoding='utf-8') as f:
            participants = list(csv.reader(f))
    except FileNotFoundError:
        participants = []

    if not participants:
        return """
        <html><body style='background:#FF0000;color:white;text-align:center;padding-top:20%;font-family:sans-serif;'>
        <h1>Aucune participation enregistrée</h1></body></html>
        """

    gagnant = random.choice(participants)
    nom_prenom = gagnant[1]
    ville = gagnant[0]
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Gagnant</title>
      <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
      <style>
        body {{
          margin: 0;
          background-color: #FF0000;
          font-family: 'Varela Round', sans-serif;
          color: white;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          text-align: center;
        }}
        .logo {{
          position: absolute;
          top: 20px;
          right: 20px;
          width: 100px;
        }}
        h1 {{
          font-size: 2em;
        }}
      </style>
    </head>
    <body>
      <img src="/static/schleich_logo.png" alt="Logo Schleich" class="logo">
      <h1>🎉 Le gagnant est :<br>{nom_prenom} ({ville})</h1>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
