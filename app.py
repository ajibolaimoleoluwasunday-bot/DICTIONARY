from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Word
from config import Config
import requests
import json

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/api/search/<word>', methods=['GET'])
def search_word(word):
    # Check local DB first
    word_entry = Word.query.filter_by(word=word.lower()).first()
    if word_entry:
        return jsonify({
            'word': word_entry.word,
            'definition': word_entry.definition,
            'ipa': word_entry.ipa,
            'synonyms': json.loads(word_entry.synonyms) if word_entry.synonyms else [],
            'antonyms': json.loads(word_entry.antonyms) if word_entry.antonyms else [],
            'examples': json.loads(word_entry.examples) if word_entry.examples else []
        })
    
    # Fetch from API
    api_key = app.config['WORDS_API_KEY']
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        definition = data.get('results', [{}])[0].get('definition', 'No definition found')
        ipa = data.get('pronunciation', {}).get('all', '')
        synonyms = data.get('results', [{}])[0].get('synonyms', [])
        antonyms = data.get('results', [{}])[0].get('antonyms', [])
        examples = data.get('results', [{}])[0].get('examples', [])
        
        # Save to DB
        new_word = Word(
            word=word.lower(),
            definition=definition,
            ipa=ipa,
            synonyms=json.dumps(synonyms),
            antonyms=json.dumps(antonyms),
            examples=json.dumps(examples)
        )
        db.session.add(new_word)
        db.session.commit()
        
        return jsonify({
            'word': word,
            'definition': definition,
            'ipa': ipa,
            'synonyms': synonyms,
            'antonyms': antonyms,
            'examples': examples
        })
    else:
        return jsonify({'error': 'Word not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample data if empty
        if not Word.query.first():
            sample = Word(
                word='love',
                definition='An intense feeling of deep affection.',
                ipa='/lʌv/',
                synonyms=json.dumps(['affection', 'adoration']),
                antonyms=json.dumps(['hate']),
                examples=json.dumps(['I love my family.'])
            )
            db.session.add(sample)
            db.session.commit()
    app.run(debug=True)
