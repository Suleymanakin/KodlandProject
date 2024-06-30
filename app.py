from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

# Oturum süresini 5 dakika olarak ayarla
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Oturum yönetimini başlat
Session(app)

def calculate_score(answers):
    # Doğru cevapları tanımla
    correct_answers = {
        'q1': 'Süleyman',
        'q2': 'Siyah',
        'q3': 'Porsuk'
    }
    score = 0
    # Kullanıcı cevaplarını kontrol et ve puanı hesapla
    for q, a in correct_answers.items():
        if answers.get(q) == a:
            score += 1
    return score

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Form verilerini al
        answers = {
            'q1': request.form.get('q1'),
            'q2': request.form.get('q2'),
            'q3': request.form.get('q3')
        }
        score = calculate_score(answers)
        
        # Oturumda en yüksek puanı güncelle
        if 'highest_score' not in session or score > session['highest_score']:
            session['highest_score'] = score
        
        # Oturumu kalıcı hale getir
        session.permanent = True
        
        return render_template('results.html', score=score, highest_score=session['highest_score'])
    
    # Ana sayfada en yüksek puanı getir
    highest_score = session.get('highest_score', 0)
    return render_template('index.html', highest_score=highest_score)

if __name__ == '__main__':
    # Uygulamayı çalıştır
    app.run(debug=True)
