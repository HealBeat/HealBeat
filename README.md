# 🥁 HealBeat Rhythm Game

HealBeat Rhythm Game은 전자드럼 실시간 입력을 기반으로 하는 리듬 게임입니다.  
노인·자폐 아동·뇌졸증 환자 등 **재활 목적**의 음악치료 보조 도구로 활용할 수 있도록 설계되었습니다.  

---

## ✨ 주요 기능

- 🎵 **MIDI 파일 기반 리듬 노트 생성**  
  지정한 폴더의 MIDI 파일을 선택하여 게임 플레이 가능

- 🥁 **전자드럼 실시간 입력 지원**  
  MIDI 입력 포트에서 드럼 신호를 받아 정해진 타이밍과 비교

- 🔴 **비주얼 피드백**  
  - 예정된 노트: 붉은색 펄스 원  
  - 실시간 사용자 입력: 주황색 원  

- 📊 **데이터 기록 및 시각화**  
  - 반응속도 기록을 CSV로 저장  
  - 세션별 limb 평균 반응속도를 그래프로 확인 가능  

- 🏆 **자동 점수 화면**  
  곡이 끝나면 점수를 자동 계산 후 결과 화면 표시

- ⏸ **게임 도중 메뉴 호출**  
  ESC 키 또는 마우스로 **Resume / Home / Exit** 선택 가능  

---

## ⚙️ 설치 방법
1. 저장소 클론
```bash
git clone https://github.com/username/healbeat-rhythm-game.git
cd healbeat-rhythm-game
```

2. 패키지 설치
```bash
pip install -r requirements.txt
```

3. 실행
```bash
python main.py
```

---

## 📂 파일 구조

```bash
healbeat/
├── main.py              # 실행 진입점
├── game.py              # 게임 로직 (pygame)
├── midi_utils.py        # MIDI 처리 (pretty_midi, mido)
├── data_utils.py        # CSV 기록 및 데이터 시각화
├── ui_home.py           # 홈 화면 UI (tkinter)
├── ui_score.py          # 점수 화면 UI
├── right.ino            # 오른팔, 오른다리 모터 진동
├── left.ino             # 왼팔, 왼다리 모터 진동
├── assets/
│   ├── background.png   # 홈 화면 배경
│   ├── background_2.png # 게임 화면 배경
│   └── ...              # 기타 이미지 리소스
├── midiFolder/               # MIDI 파일 모음 폴더
└── reaction_data.csv    # 반응속도 기록 (자동 생성)






