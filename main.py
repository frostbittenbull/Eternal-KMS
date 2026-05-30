import ctypes
import sys
import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import font as tkfont
import tkinter as tk
import time

def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

ctk.set_appearance_mode("dark")

class AnimatedButton(ctk.CTkButton):
    pass

class WindowsActivator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Eternal KMS")
        self.geometry("520x460")
        self.resizable(False, False)
        self.configure(fg_color="#0d0d0f")

        self.tsforge_exe = resource_path("TSforge.exe")
        self._activated = False

        self._build_ui()
        self._center_window()
        self._animate_intro()

        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#13131a", corner_radius=0, height=24)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        self.stripe = ctk.CTkFrame(header, fg_color="#2e2e2e", corner_radius=0, width=3, height=24)
        self.stripe.place(x=0, y=0)

        self.title_label = ctk.CTkLabel(
            header,
            text="ETERNAL  KMS",
            font=("Courier New", 11, "bold"),
            text_color="#e8e8ff",
        )
        self.title_label.place(x=14, rely=0.5, anchor="w")

        self.status_dot = ctk.CTkLabel(
            header,
            text="●",
            font=("Courier New", 9),
            text_color="#2e2e2e",
        )
        self.status_dot.place(relx=1.0, x=-12, rely=0.5, anchor="e")

        console_frame = ctk.CTkFrame(self, fg_color="#0d0d0f", corner_radius=0)
        console_frame.pack(fill="both", expand=True, padx=12, pady=(8, 4))

        self.console_box = ctk.CTkTextbox(
            console_frame,
            fg_color="#0a0a0c",
            text_color="#7cfc98",
            font=("Courier New", 11),
            corner_radius=6,
            border_width=1,
            border_color="#1e1e1e",
            scrollbar_button_color="#1e1e1e",
            scrollbar_button_hover_color="#2e2e2e",
            wrap="word",
        )
        self.console_box.pack(fill="both", expand=True)
        self.console_box.configure(state="disabled")

        bottom = ctk.CTkFrame(self, fg_color="#0d0d0f", corner_radius=0)
        bottom.pack(fill="x", side="bottom", padx=12, pady=(0, 10))

        self.activate_btn = ctk.CTkButton(
            bottom,
            text="⚡  Активировать Windows на 4085 лет",
            font=("Courier New", 11, "bold"),
            fg_color="#2e2e2e",
            hover_color="#3d3d3d",
            text_color="#ffffff",
            corner_radius=6,
            height=28,
            border_width=0,
            command=self._start_activation,
        )
        self.activate_btn.pack(fill="x", pady=(0, 4))

        self.office_btn = ctk.CTkButton(
            bottom,
            text="⚡  Активировать Office на 4085 лет",
            font=("Courier New", 11, "bold"),
            fg_color="#2e2e2e",
            hover_color="#3d3d3d",
            text_color="#ffffff",
            corner_radius=6,
            height=28,
            border_width=0,
            command=self._start_office_activation,
        )
        self.office_btn.pack(fill="x", pady=(0, 4))

        self.all_btn = ctk.CTkButton(
            bottom,
            text="⚡  Активировать всё сразу на 4085 лет",
            font=("Courier New", 11, "bold"),
            fg_color="#1e2a1e",
            hover_color="#2a3d2a",
            text_color="#a3e6a3",
            corner_radius=6,
            height=28,
            border_width=0,
            command=self._start_all_activation,
        )
        self.all_btn.pack(fill="x")

    def _animate_intro(self):
        lines = [
            "  Инициализация…",
        ]
        for i, line in enumerate(lines):
            self.after(i * 60, lambda l=line: self.log(l, color="#5b5ef4" if "ETERNAL" in l else None))
        self.after(len(lines) * 60 + 100, lambda: self.run_command("systeminfo"))

    def log(self, text, color=None):
        self.console_box.configure(state="normal")
        self.console_box.insert("end", text + "\n")
        self.console_box.see("end")
        self.console_box.configure(state="disabled")

    def _set_status(self, state: str = "idle"):
        colors = {
            "idle":    ("#2e2e2e", "#2e2e2e", "#3d3d3d"),
            "working": ("#f87171", "#7f2020", "#a03030"),
            "done":    ("#4ade80", "#1a5c2a", "#2a7c3a"),
        }
        dot_color, btn_color, hover_color = colors.get(state, colors["idle"])
        self.status_dot.configure(text_color=dot_color)
        self.stripe.configure(fg_color=dot_color)
        self.activate_btn.configure(fg_color=btn_color, hover_color=hover_color)

    def _disable_all_buttons(self):
        self.activate_btn.configure(state="disabled")
        self.office_btn.configure(state="disabled")
        self.all_btn.configure(state="disabled")

    def _enable_all_buttons(self):
        self.activate_btn.configure(state="normal")
        self.office_btn.configure(state="normal")
        self.all_btn.configure(state="normal")

    def run_command(self, cmd_string, flag=None):
        def target():
            try:
                process = subprocess.Popen(
                    cmd_string,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="cp866",
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                for line in process.stdout:
                    self.after(0, self.log, line.strip())
                process.wait()

                if flag in ("kms4k", "kms4o", "kms4all"):
                    self.after(0, self.log, "\n  Проверка статуса…")
                    self.run_command("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /xpr")
                    self.after(0, self._enable_all_buttons)
                    self.after(0, lambda: self._set_status("done"))
                    self.after(0, self.log, "  ✓ Готово.\n")

            except Exception as e:
                self.after(0, self.log, f"  Ошибка! {e}")

        threading.Thread(target=target, daemon=True).start()

    def _start_activation(self):
        self._disable_all_buttons()
        self._set_status("working")
        self.log("\n  Запуск TSforge (Windows)…\n")
        cmd = f'"{self.tsforge_exe}" /kms4k'
        self.run_command(cmd, flag="kms4k")

    def _start_office_activation(self):
        self._disable_all_buttons()
        self._set_status("working")
        self.log("\n  Запуск TSforge (Office)…\n")
        cmd = f'"{self.tsforge_exe}" /kms4o'
        self.run_command(cmd, flag="kms4o")

    def _start_all_activation(self):
        self._disable_all_buttons()
        self._set_status("working")
        self.log("\n  Запуск TSforge (всё)…\n")
        cmd = f'"{self.tsforge_exe}" /kms4all'
        self.run_command(cmd, flag="kms4all")

if __name__ == "__main__":
    app = WindowsActivator()
    app.mainloop()