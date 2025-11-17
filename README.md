# 🥁 HealBeat Rhythm Game

(English)


HealBeat Rhythm Game is a rhythm game based on real-time electronic drum input.
It is designed to serve as an auxiliary tool for music therapy with **rehabilitation purposes** for seniors, children with autism, stroke patients, and others.


(한국어)


HealBeat Rhythm Game은 전자드럼 실시간 입력을 기반으로 하는 리듬 게임입니다.  
노인·자폐 아동·뇌졸증 환자 등 **재활 목적**의 음악치료 보조 도구로 활용할 수 있도록 설계되었습니다.  

---

## 🎶 Research Background | 프로젝트 배경

(English)


Music and rhythm games are widely recognized as effective tools in **rehabilitation and therapy**.  
In particular:

- **Motor Skills Training**:  
  Drumming requires precise timing and coordination, which can help improve motor functions in elderly users and individuals with autism spectrum disorder (ASD).

- **Cognitive Engagement**:  
  Matching beats with visual and auditory cues encourages attention, memory, and reaction speed.

- **Emotional Motivation**:  
  Interactive rhythm-based feedback provides motivation and enjoyment, increasing adherence to therapy routines.

By combining **real-time MIDI drumming input** with **visual & heptic feedback and data tracking**, this project bridges **music therapy** and **game-based rehabilitation**, creating a playful yet structured environment for training.


(한국어)


음악과 리듬 게임은 재활 및 치료에서 효과적인 도구로 잘 알려져 있습니다.

-  **운동 능력 훈련**: 드럼 연주는 정확한 타이밍과 협응을 요구하여, 신체 능력 향상에 도움을 줍니다.

- **인지적 참여**: 시각·청각 신호에 맞춰 박자를 맞추는 과정은 집중력, 기억력, 반응 속도 개선에 기여합니다.

- **정서적 동기 부여**: 리듬 기반 상호작용은 즐거움과 동기를 제공해 지속적인 참여를 유도합니다.

본 프로젝트는 **실시간 MIDI 드럼 입력**과 **시각적, 촉각적 피드백 및 데이터 기록**을 결합하여,
음악치료와 게임 기반 재활을 연결하는 구조화된 재미있는 훈련 환경을 제공합니다.

---

## 🎶 Flow Chart | 흐름도


---

## Setup | 개발 환경

(English)


- **Hardware**
  
MCU: Arduino Uno

Actuator: Vibration Motor Module

External Instrument: Samik loogo Electronic Drum Pad


- **Software**
  
Language: Python , Arduino IDE

Library: pretty_midi, pygame, mido, pandas, matplotlib, Pillow, tkinter

Environment: Windows

---

## ✨ Features | 주요 기능

(English)


- 🎵 **Realtime MIDI Drum Input**  
  Detects timing of drum hits
  
- 🥁 **Feedback**
  Drum kit pulses in sync with scheduled notes.
  Vibration sensor with scheduled notes.

- 📊 **Session Visualization**
  Average reaction errors per limb are plotted over multiple attempts.

- 🏆 **Score Screen**
  Evaluates accuracy based on hit timing.

(한국어)

- 🎵 **MIDI 파일 기반 리듬 노트 생성**  
  지정한 폴더의 MIDI 파일을 선택하여 게임 플레이 가능

- 🥁 **전자드럼 실시간 입력 지원**  
  MIDI 입력 포트에서 드럼 신호를 받아 정해진 타이밍과 비교

- 🔴 **피드백**  
  - 예정된 노트: 붉은색 펄스 원, 진동센서서  
  - 실시간 사용자 입력: 주황색 원  

- 📊 **데이터 기록 및 시각화**  
  - 반응속도 기록을 CSV로 저장  
  - 세션별 limb 평균 반응속도를 그래프로 확인 가능  

- 🏆 **자동 점수 화면**  
  곡이 끝나면 점수를 자동 계산 후 결과 화면 표시

- ⏸ **게임 도중 메뉴 호출**  
  ESC 키 또는 마우스로 **Resume / Home / Exit** 선택 가능  

---

## ⚙️ Installation | 설치 방법
1. Clone the repository 저장소 클론
```bash
git clone https://github.com/username/healbeat-rhythm-game.git
cd healbeat-rhythm-game
```

2. Install Packages 패키지 설치
```bash
pip install -r requirements.txt
```

3. Run 실행
```bash
python main.py
```

---

## 📂 Project Structure | 파일 구조

```bash
healbeat/
├── main.py              # 실행 진입점. Entry point (home screen & navigation)
├── game.py              # 게임 로직. Core rhythm game Logic (pygame) 
├── midi_utils.py        # MIDI 처리.  (pretty_midi, mido)
├── data_utils.py        # CSV 기록 및 데이터 시각화. Data saving & visualization.
├── ui_home.py           # 홈 화면 UI. Home screen UI.
├── ui_score.py          # 점수 화면 UI. Score screen UI.
├── motor.ino            # 모터 진동 피드백. Heptic feedback for limbs.
├── requirement.txt      # 패키지 설치 리스트. Dependencies
├── assets/
│   ├── background.png   # 홈 화면 배경. Home screen background.
│   ├── background_2.png # 게임 화면 배경. Main screen background.
│   └── ...              # 기타 이미지 리소스. Other image resources.
├── midiFolder/               # MIDI 파일 모음 폴더. MIDI files folder
└── reaction_data.csv    # 반응속도 기록 (자동 생성). Records of reaction speed.
