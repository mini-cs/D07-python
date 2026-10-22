import random
import tkinter as tk
from datetime import datetime

# 동행복권 공 색상: 1-10 노랑, 11-20 파랑, 21-30 빨강, 31-40 회색, 41-45 초록
COLORS = ["#fbc400", "#69c8f2", "#ff7272", "#aaaaaa", "#b0d840"]


def draw():
    return [sorted(random.sample(range(1, 46), 6)) for _ in range(5)]


def show():
    date_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for row, nums in zip(rows, draw()):
        for lbl, n in zip(row, nums):
            lbl.config(text=n, bg=COLORS[(n - 1) // 10])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("로또 번호 생성기")
    date_label = tk.Label(root, text="", font=("맑은 고딕", 12))
    date_label.pack(pady=8)
    rows = []
    for _ in range(5):
        frame = tk.Frame(root)
        frame.pack(pady=3, padx=10)
        row = [tk.Label(frame, text="", width=3, font=("맑은 고딕", 14, "bold"), fg="white") for _ in range(6)]
        for lbl in row:
            lbl.pack(side="left", padx=2)
        rows.append(row)
    tk.Button(root, text="번호 뽑기", font=("맑은 고딕", 12), command=show).pack(pady=10)
    root.mainloop()
