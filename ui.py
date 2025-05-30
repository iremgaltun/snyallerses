import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
from realtime import process_realtime
print("Import başarılı!")


input_path = ""
output_path = ""

python_exe = sys.executable
script_dir = os.path.dirname(os.path.abspath(__file__))

def select_file():
    global input_path, output_path
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        input_path = file_path
        output_path = os.path.splitext(input_path)[0] + "_temiz.wav"
        file_label.config(text=f"Seçilen Dosya: {os.path.basename(file_path)}")

def clean_audio():
    if not input_path:
        messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin!")
        return
    btn_clean.config(state=tk.DISABLED)
    btn_analyze.config(state=tk.DISABLED)
    try:
        filtre_path = os.path.join(script_dir, "filtre.py")
        subprocess.run([python_exe, filtre_path, input_path, output_path], check=True)
        messagebox.showinfo("Başarılı", "Ses temizleme tamamlandı.")

        # Temizleme bittikten sonra analiz yap
        analiz_path = os.path.join(script_dir, "analiz.py")
        subprocess.run([python_exe, analiz_path, input_path, output_path], check=True)
        messagebox.showinfo("Başarılı", "Analiz tamamlandı.")

    except Exception as e:
        messagebox.showerror("Hata", str(e))
    finally:
        btn_clean.config(state=tk.NORMAL)
        btn_analyze.config(state=tk.NORMAL)


def analyze_audio():
    if not input_path or not output_path:
        messagebox.showwarning("Uyarı", "Önce temizleme işlemini yapın!")
        return
    if not os.path.exists(output_path):
        messagebox.showwarning("Uyarı", "Temizlenmiş dosya bulunamadı. Önce temizleme yapın.")
        return
    btn_clean.config(state=tk.DISABLED)
    btn_analyze.config(state=tk.DISABLED)
    try:
        analiz_path = os.path.join(script_dir, "analiz.py")
        subprocess.run([python_exe, analiz_path, input_path, output_path], check=True)
    except Exception as e:
        messagebox.showerror("Hata", str(e))
    finally:
        btn_clean.config(state=tk.NORMAL)
        btn_analyze.config(state=tk.NORMAL)

def run_realtime():
    def task():
        btn_record.config(state=tk.DISABLED)
        try:
            global input_path, output_path
            input_path, output_path = process_realtime(python_exe, script_dir)
            file_label.config(text="Canlı kayıt tamamlandı.")
            messagebox.showinfo("Tamamlandı", "🎙️ Kayıt, Temizleme ve Analiz bitti.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            btn_record.config(state=tk.NORMAL)

    threading.Thread(target=task).start()

# --- Arayüz ---
root = tk.Tk()
root.title("Ses Temizleme ve Analiz Arayüzü")
root.geometry("400x300")

file_label = tk.Label(root, text="Henüz dosya seçilmedi", wraplength=300)
file_label.pack(pady=10)

btn_select = tk.Button(root, text="📁 Dosya Seç", command=select_file)
btn_select.pack(pady=5)

btn_clean = tk.Button(root, text="🧹 Temizle", command=clean_audio)
btn_clean.pack(pady=5)

btn_analyze = tk.Button(root, text="📊 Analiz Et", command=analyze_audio)
btn_analyze.pack(pady=5)

btn_record = tk.Button(root, text="🎙️ Kaydet ve Temizle", command=run_realtime)
btn_record.pack(pady=10)

root.mainloop()
