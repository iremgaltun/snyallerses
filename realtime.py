# realtime.py

import sounddevice as sd
import wave
import tempfile
import subprocess
import os
import sys
import time

def record_to_wav(duration=8, fs=44100, save_dir="recordings"):
    print("🎙️ Kayıt başlıyor...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    timestamp = int(time.time() * 1000)
    filename = f"kayit_{timestamp}.wav"
    tmp_input = os.path.join(save_dir, filename)

    with wave.open(tmp_input, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())

    print(f"✅ Kayıt tamamlandı: {tmp_input}")
    return tmp_input

def process_realtime(python_exe, script_dir):  # BU FONKSİYON BURADA OLMALI
    input_wav = record_to_wav()
    output_wav = input_wav.replace(".wav", "_temiz.wav")

    filtre_path = os.path.join(script_dir, "filtre.py")
    analiz_path = os.path.join(script_dir, "analiz.py")

    subprocess.run([python_exe, filtre_path, input_wav, output_wav], check=True)
    subprocess.run([python_exe, analiz_path, input_wav, output_wav], check=True)

    print("✅ Temizleme ve analiz işlemi tamamlandı.")
    return input_wav, output_wav

print("✅ realtime.py yüklendi. GUI üzerinden çağrılmaya hazır.")
