import os
import json

# 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, '../data/complex_mix')
OUTPUT_FILE = os.path.join(BASE_DIR, 'audio_files.json')

def generate_list():
    audio_files = []
    print(f"Scanning {AUDIO_DIR}...")
    
    for root, dirs, files in os.walk(AUDIO_DIR):
        for file in files:
            if file.lower().endswith(('.wav', '.mp3', '.flac')):
                # 웹에서 접근 가능한 상대 경로로 변환
                # survey_app 폴더 기준이 아니라, 나중에 웹에 올라갔을 때의 상대 경로를 고려해야 함
                # 하지만 로컬 파일 시스템 기준으로 일단 상대 경로를 구하고, 
                # 웹에서는 index.html이 survey_app 안에 있다면 ../data/... 로 접근 가능
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, AUDIO_DIR)
                
                # 윈도우의 경우 역슬래시를 슬래시로 변경
                rel_path = rel_path.replace('\\', '/')
                audio_files.append(rel_path)
    
    # 결과 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(audio_files, f, ensure_ascii=False, indent=2)
    
    print(f"Found {len(audio_files)} files.")
    print(f"Saved list to {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_list()
