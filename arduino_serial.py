#----------------------------
# UNO 포트 열기(없으면 None)
#----------------------------
def open_serial(port: str, baud: int = 250000):
    """UNO 포트 열기(없으면 None)"""
    if not port: return None
    try:
        ser = serial.Serial(port, baudrate=baud, timeout=1, write_timeout=0)
        time.sleep(2.0)  # UNO는 포트 오픈 시 리셋
        ser.reset_input_buffer(); ser.reset_output_buffer()
        return ser
    except Exception:
        return None

# === 모터 전송 헬퍼 ===
def send_limbs_serial(ser, limbs):
    """사지 리스트를 UNO가 이해하는 vel로 전송: {"vel":NN}\n"""
    if not ser or not ser.is_open or not limbs:
        return
    for l in limbs:
        vel = LIMB_TO_VEL.get(l)     # "Left Arm" 등 정확 문자열 → 40/30/20/10
        if vel is None:
            continue
        ser.write((json.dumps({"vel": vel}) + "\n").encode("utf-8"))

def all_off_serial(ser):
    """모든 모터 OFF"""
    if ser and ser.is_open:
        try:
            ser.write(b'{"cmd":"all_off"}\n'); time.sleep(0.02)
            ser.write(b'{"cmd":"all_off"}\n')
        except Exception:
            pass
        
