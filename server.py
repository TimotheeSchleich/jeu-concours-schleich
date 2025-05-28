
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
    return "<h1>Merci pour votre participation ! 🦍</h1>"

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
