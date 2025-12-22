from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import random
import csv
from datetime import datetime

app = Flask(__name__)

# Configuration
# Assuming the audio files are in ../data/complex_mix relative to this script
# You can change this path to match your actual audio directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, '../data/complex_mix')
RESULTS_FILE = os.path.join(BASE_DIR, 'survey_results.csv')
COMMENTS_FILE = os.path.join(BASE_DIR, 'survey_comments.csv')

# Ensure results file exists with headers
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'name', 'audio_file', 'perception_yn', 'perception_difficulty', 'annoyance', 'user_agent'])

# Ensure comments file exists with headers
if not os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'name', 'comment'])

def get_audio_files():
    """Recursively find all audio files in the AUDIO_DIR."""
    audio_files = []
    for root, dirs, files in os.walk(AUDIO_DIR):
        for file in files:
            if file.lower().endswith(('.wav', '.mp3', '.flac')):
                # Store relative path from AUDIO_DIR
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, AUDIO_DIR)
                audio_files.append(rel_path)
    return audio_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/next_audio')
def next_audio():
    files = get_audio_files()
    if not files:
        return jsonify({'error': 'No audio files found'}), 404
    
    # Pick a random file
    # In a real deployment, you might want to track which files 
    # have been rated to prioritize unrated ones.
    selected_file = random.choice(files)
    return jsonify({'audio_file': selected_file})

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@app.route('/api/submit', methods=['POST'])
def submit_survey():
    data = request.json
    
    with open(RESULTS_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            data.get('name'),
            data.get('audio_file'),
            data.get('perception_yn'),
            data.get('perception_difficulty'),
            data.get('annoyance'),
            request.headers.get('User-Agent')
        ])
    
    return jsonify({'status': 'success'})

@app.route('/api/submit_comment', methods=['POST'])
def submit_comment():
    data = request.json
    
    with open(COMMENTS_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            data.get('name'),
            data.get('comment')
        ])
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print(f"Serving audio from: {AUDIO_DIR}")
    print(f"Saving results to: {RESULTS_FILE}")
    print(f"Saving comments to: {COMMENTS_FILE}")
    app.run(host='0.0.0.0', port=5000, debug=True)
