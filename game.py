import pygame
import time
import sys
from collections import defaultdict
from config import drum_positions, NOTE_TO_DRUM, velocity_to_limb, LIMB_TO_VEL
from data_manager import save_reaction_data
from midi_utils import open_midi_in, extract_hits_from_midi
from tkinter import messagebox
import math

def pause_menu():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    paused = True
    font = pygame.font.SysFont("Arial", 40, bold=True)
    options = ["Resume", "Home", "Exit"]
    selected = 0

    # 메뉴 버튼 rect 저장
    option_rects = []

    while paused:
        screen.fill((0, 0, 0))  # 검은 배경 (투명도 적용하려면 surface 사용)

        option_rects = []  # 매 프레임마다 rect 갱신
        for i, opt in enumerate(options):
            color = (255, 200, 0) if i == selected else (255, 255, 255)
            text = font.render(opt, True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 80))
            screen.blit(text, rect)
            option_rects.append((opt, rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Exit"

            # 키보드 입력
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]

            # 마우스 입력
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, (opt, rect) in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selected = i  # 마우스로 hover하면 선택 이동
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 클릭
                    mouse_pos = event.pos
                    for opt, rect in option_rects:
                        if rect.collidepoint(mouse_pos):
                            return opt

# 게임 실행 함수
def run_game_with_realtime_input(midi_path, inport_name=None):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rehab Rhythm Game")
    clock = pygame.time.Clock()

    HIT_WINDOW_SEC = 0.150

    # 배경 이미지
    try:
        background = pygame.image.load("assets/background_2.png")
        background = pygame.transform.scale(background, (800, 600))
    except:
        background = None

    # MIDI 이벤트 추출
    hits = extract_hits_from_midi(midi_path)
    if not hits:
        print("⚠️ MIDI에서 드럼 이벤트를 찾지 못했습니다.")
        return

    # MIDI 입력 포트 열기
    try:
        inport = open_midi_in()
    except RuntimeError as e:
        messagebox.showerror("MIDI 포트 오류", str(e))
        return

    # 반응속도 기록
    limb_reaction_times = defaultdict(list)

    # 펄스 트리거 초기화
    pulse_trigger = {drum: -1 for drum in drum_positions.keys()}
    live_trigger = {drum: -1 for drum in drum_positions.keys()}
    last_note_time = hits[-1][0] if hits else 0

    start_time = time.time()
    running = True
    score = 0
    total_notes = len(hits)

    while running:
        now = time.time() - start_time

        # 이벤트 처리 (종료/ESC/메뉴)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                action = pause_menu()
                if action == "Exit":
                    pygame.quit()
                    sys.exit()
                elif action == "Home":
                    running = False
                elif action == "Resume":
                    pass
                
        # 화면 그리기
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # 펄스 만들기
        for hit in hits:
            scheduled_time, drum, _ = hit
            dt = now - scheduled_time
            if 0 <= dt < 0.5:
                pulse_trigger[drum] = scheduled_time
    
        for drum, pos in drum_positions.items():
            x, y = pos
            if pulse_trigger[drum] < 0:  # 아직 해당 드럼 노트 없음
                radius = 20
            else:
                dt = now - pulse_trigger[drum]  # 경과 시간 계산
                if dt > 0.5:
                    radius = 20
                else:
                    radius = 80 * math.exp(-3 * dt) + 20
            pygame.draw.circle(screen, (255, 100, 100), (x, y), int(radius))
        
        # 실시간 연주 입력 받기
        for msg in inport.iter_pending():
            print(msg)
            now = time.time() - start_time
            if msg.type=='note_on' and msg.velocity>0:
                drum = NOTE_TO_DRUM.get(msg.note)
                if drum:
                    live_trigger[drum] = now
                    for idx, (scheduled_time, scheduled_drum, limb) in enumerate(hits):
                        if scheduled_drum == drum and scheduled_time >= now - 0.5:
                            diff = now - scheduled_time
                            if abs(diff) <= HIT_WINDOW_SEC:
                                score += 1
                            if limb:
                                for l in limb:
                                    limb_reaction_times[l].append(diff)
                            hits.pop(idx)
                            break
        if now > last_note_time + 2:
            running = False
        
        for drum, pos in drum_positions.items():
            x, y = pos
            dt_live = now - live_trigger[drum]
            if 0 <= dt_live < 0.3:
                pygame.draw.circle(screen, (255, 165, 0), (x, y), 15)  
        
        pygame.display.flip()
        clock.tick(60)
        
        

    # 반응속도 저장
    save_reaction_data(limb_reaction_times)

    # 점수 화면
    show_score_screen(screen, score, total_notes)


def show_score_screen(screen, score, total_notes):
    WIDTH, HEIGHT = 800, 600
    
    try:
        background = pygame.image.load("assets/background.png")
        background = pygame.transform.scale(background, (800, 600))
    except:
        background = None

    font = pygame.font.SysFont("arial", 50, bold=True)
    small_font = pygame.font.SysFont("arial", 30)
    acc = (score / total_notes * 100) if total_notes > 0 else 0
    result_text = font.render(f"Score: {score}/{total_notes} ({acc:.1f}%)", True, (255,255,255))
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 엔터 누르면 홈으로
                    running = False

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))

        text = font.render("🎵 Session Complete! 🎵", True, (255, 255, 255))
        screen.blit(text, (150, 200))

        info = small_font.render("Press ENTER to return to Home", True, (200, 200, 200))
        screen.blit(info, (220, 300))

        pygame.display.flip()

