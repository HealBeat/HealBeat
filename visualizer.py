import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import messagebox
from data_manager import CSV_FILE

def visualize_sessions():
    if not os.path.isfile(CSV_FILE):
        messagebox.showinfo("데이터 없음", "아직 기록된 반응속도 데이터가 없습니다.")
        return
    
    df = pd.read_csv(CSV_FILE)
    avg_df = df.groupby(["Session","Limb"])["ReactionTime"].mean().reset_index()
    
    plt.figure(figsize=(10,6))  
    for limb, group in avg_df.groupby("Limb"):
        plt.plot(group["Session"], group["ReactionTime"], linestyle="--", marker="o", label=limb)
    
    plt.title("Limb Reaction Time per Session")
    plt.xlabel("Session Index")
    plt.ylabel("Reaction Time (s)")
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.show()
