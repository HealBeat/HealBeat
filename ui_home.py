import tkinter as tk
from tkinter import messagebox
import os
from game import run_game_with_realtime_input
from visualizer import visualize_sessions
from PIL import Image, ImageTk

MIDI_FOLDER = "midFolder"  # 🎵 미리 지정한 MIDI 폴더


# 🎵 MIDI 선택 UI 함수
def choose_midi_from_folder(root, folder=MIDI_FOLDER):
    win = tk.Toplevel(root)
    win.title("MIDI 파일 선택")
    win.geometry("400x400")
    win.configure(bg="#1e1e1e")

    tk.Label(win, text="MIDI 파일 선택", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

    midi_files = [f for f in os.listdir(folder) if f.lower().endswith((".mid", ".midi"))]

    listbox = tk.Listbox(win, font=("Arial", 14), width=30, height=15)
    listbox.pack(pady=10)

    if not midi_files:
        listbox.insert(tk.END, "폴더에 MIDI 파일이 없습니다.")
    else:
        for f in midi_files:
            listbox.insert(tk.END, f)


    def start_selected():
        selection = listbox.curselection()
        if selection:
            midi_path = os.path.join(folder, midi_files[selection[0]])
            win.destroy()
            root.withdraw()
            run_game_with_realtime_input(midi_path)  # 게임 실행
            root.deiconify()

    tk.Button(
        win,
        text="🎵 선택한 곡 실행",
        font=("Arial", 14, "bold"),
        bg="#444",
        fg="white",
        activebackground="orange",
        command=start_selected,
    ).pack(pady=10)


# 🎮 홈 화면
def home():
    root = tk.Tk()
    root.title("HealBeat Rehab Rhythm Game")
    root.geometry("600x400")
    
    # ✅ 배경 이미지 설정
    bg_image_path = "assets/background.png"  # 원하는 이미지 경로
    if os.path.exists(bg_image_path):
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((800, 600))  # 창 크기에 맞게 조정
        bg_photo = ImageTk.PhotoImage(bg_img)

        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo  # 참조 유지
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    else:
        root.configure(bg="#1e1e1e")  # 이미지 없으면 단색 배경

    title = tk.Label(root, text="HealBeat Rehab Rhythm Game", font=("Arial", 28, "bold"), fg="white", bg="#1e1e1e")
    title.pack(pady=40)

    # MIDI 선택 버튼 → 리스트 창 열기
    midi_btn = tk.Button(
        root,
        text="🎵 Select MIDI and Play",
        font=("Arial", 16),
        width=25,
        height=2,
        command=lambda: choose_midi_from_folder(root),
        bg="#007acc",
        fg="white",
        relief="flat",
    )
    midi_btn.pack(pady=20)

    # 데이터 시각화 버튼
    viz_btn = tk.Button(
        root,
        text="📊 View Data Visualization",
        font=("Arial", 14),
        command=visualize_sessions,
        bg="#444",
        fg="white",
        relief="flat",
        width=25,
        height=2,
    )
    viz_btn.pack(pady=20)
    
    exit = tk.Button(
        root, 
        text="❌ 종료", 
        font=("Arial", 14), 
        command=root.destroy,
        bg="#444",
        fg="white",
        relief="flat",
        width=25,
        height=2,
    )
    exit.pack(pady=20)   

    root.mainloop()
