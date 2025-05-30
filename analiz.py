import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft
import os

if len(sys.argv) != 3:
    print("Kullanım: python analiz.py <orijinal.wav> <temizlenmiş.wav>")
    sys.exit(1)

original_path = sys.argv[1]
cleaned_path = sys.argv[2]

# --- 1. Ses dosyalarını oku ---
fs1, data_orig = wavfile.read(original_path)
fs2, data_clean = wavfile.read(cleaned_path)

# --- 2. Mono yap ---
if len(data_orig.shape) == 2:
    data_orig = data_orig[:, 0]
if len(data_clean.shape) == 2:
    data_clean = data_clean[:, 0]

# --- 3. Normalize et ---
data_orig = data_orig / (np.max(np.abs(data_orig)) + 1e-10)
data_clean = data_clean / (np.max(np.abs(data_clean)) + 1e-10)

# --- 4. Uzunluğu eşitle ---
N = min(len(data_orig), len(data_clean))
data_orig = data_orig[:N]
data_clean = data_clean[:N]

# --- 5. FFT ---
freqs = np.fft.fftfreq(N, 1/fs1)
spectrum_orig = np.abs(fft(data_orig))
spectrum_clean = np.abs(fft(data_clean))

# --- 6. Grafikler ---
plt.figure(figsize=(14, 10))

# (a) Orijinal
plt.subplot(3, 1, 1)
plt.plot(freqs[:N//2], spectrum_orig[:N//2])
plt.title("Orijinal (Gürültülü) Ses Frekans Spektrumu")
plt.xlabel("Frekans (Hz)")
plt.ylabel("Genlik")
plt.grid(True)

# (b) Temizlenmiş
plt.subplot(3, 1, 2)
plt.plot(freqs[:N//2], spectrum_clean[:N//2])
plt.title("Temizlenmiş Ses Frekans Spektrumu")
plt.xlabel("Frekans (Hz)")
plt.ylabel("Genlik")
plt.grid(True)

# (c) Karşılaştırmalı
plt.subplot(3, 1, 3)
plt.plot(freqs[:N//2], spectrum_orig[:N//2], label="Orijinal", alpha=0.6)
plt.plot(freqs[:N//2], spectrum_clean[:N//2], label="Temizlenmiş", alpha=0.6)
plt.title("Frekans Spektrumu Karşılaştırması")
plt.xlabel("Frekans (Hz)")
plt.ylabel("Genlik")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
