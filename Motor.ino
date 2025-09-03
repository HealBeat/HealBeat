// UNO 1대: 4모터 제어 (Left Hand, Right Hand, Left Leg, Right Leg)
// Pins: 3=Left Hand, 4=Right Hand, 5=Left Leg, 6=Right Leg
// 입력 형식: {"inst":"Snare","vel":NN}\n  ← vel 정확값(30/60/120/90)로 라우팅
// 끝낼 때: {"cmd":"all_off"}\n

#include <ctype.h>  // isspace, isdigit

// ===== Pin mapping =====
const int PIN_LEFT_HAND  = 3;
const int PIN_RIGHT_HAND = 4;
const int PIN_LEFT_LEG   = 5;
const int PIN_RIGHT_LEG  = 6;

// 인덱스: 0=LH, 1=RH, 2=LL, 3=RL
int pins[4] = { PIN_LEFT_HAND, PIN_RIGHT_HAND, PIN_LEFT_LEG, PIN_RIGHT_LEG };

// 펄스 길이(ms)
uint32_t VIB_MS = 250;
uint32_t off_deadline_ms[4] = {0,0,0,0};

// ---- Serial.write 헬퍼 ----
inline void logLine(const String& s){ Serial.write(s.c_str()); Serial.write('\n'); }

// ---- I/O 헬퍼 ----
inline void outOn (int idx){ digitalWrite(pins[idx], HIGH); }
inline void outOff(int idx){ digitalWrite(pins[idx], LOW ); }

// 모터 ON + 자동 OFF 예약
void firePulse(int idx){
  outOn(idx);
  off_deadline_ms[idx] = millis() + VIB_MS;
  logLine(String("TRIGGER idx=") + idx + " pin=" + pins[idx]);
}

// 모두 끄기
void allOff(){
  for (int i=0;i<4;i++){ outOff(i); off_deadline_ms[i] = 0; }
  Serial.write("ALL OFF\n");
}

// === velocity 정확 매핑 ===
// 30 → Left Hand(0), 60 → Right Hand(1), 120 → Left Leg(2), 90 → Right Leg(3)
int indexFromVelocityExact(int vel){
  switch (vel){
    case 40:  return 0; // 왼손
    case 30:  return 1; // 오른손
    case 20: return 2; // 왼발
    case 10:  return 3; // 오른발
    default:  return -1;
  }
}

// JSON에서 "vel"만 추출: {"inst":"...","vel":NN}
bool parseVelOnly(const char* line, int& velOut){
  String s(line); s.trim();
  String low = s; low.toLowerCase();
  velOut = -1;

  int p = low.indexOf("\"vel\"");
  if (p < 0) return false;
  int c = s.indexOf(':', p);
  if (c < 0) return false;

  int i = c + 1;
  while (i < (int)s.length() && isspace((unsigned char)s[i])) i++;
  int j = i;
  while (j < (int)s.length() && isdigit((unsigned char)s[j])) j++;
  if (j > i){ velOut = s.substring(i, j).toInt(); return true; }
  return false;
}

void setup(){
  Serial.begin(250000);                // 파이썬과 보율 맞추기
  for (int i=0;i<4;i++){ pinMode(pins[i], OUTPUT); outOff(i); }
  Serial.write("READY (UNO-4MOTORS)\n");
}

void loop(){
  static char buf[256];

  // 1) 한 줄 수신(개행까지)
  if (Serial.available()){
    size_t n = Serial.readBytesUntil('\n', buf, sizeof(buf)-1);
    buf[n] = 0;

    logLine(String("LINE: ") + buf);

    // all_off 명령 처리
    String low = String(buf); low.toLowerCase();
    if (low.indexOf("all_off") >= 0){ allOff(); return; }

    // 2) vel 파싱 → 정확 매핑
    int vel = -1;
    if (parseVelOnly(buf, vel)){
      int idx = indexFromVelocityExact(vel);
      if (idx >= 0){
        firePulse(idx);
      } else {
        logLine(String("IGNORED vel=") + vel); // 지정 외 값은 무시
      }
    } else {
      Serial.write("parse FAIL\n");
    }
  }

  // 3) 자동 OFF (논블로킹)
  uint32_t now = millis();
  for (int i=0;i<4;i++){
    if (off_deadline_ms[i] && (int32_t)(now - off_deadline_ms[i]) >= 0){
      outOff(i);
      off_deadline_ms[i] = 0;
    }
  }
}
