import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, istft, medfilt
import os

if len(sys.argv) != 3:
    print("Kullanım: python temizle.py <girdidosya.wav> <çıktıdosya.wav>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

# --- 1. Ses dosyasını oku ---
fs, data = wavfile.read(input_path)

# Stereo ise mono yap
if len(data.shape) == 2:
    data = data[:, 0]

# Normalize et
data = data / (np.max(np.abs(data)) + 1e-10)

# Gürültü örneği (ilk 5 saniye + rastgele bölge)
noise_sample = np.concatenate([
    data[0:int(5 * fs)],
    data[int(0 * fs):int(8 * fs)]
])

# --- 2. STFT ---
nperseg = 2048
f, t, Zxx = stft(data, fs=fs, nperseg=nperseg)
_, _, Zxx_noise = stft(noise_sample, fs=fs, nperseg=nperseg)

# --- 3. Wiener filtresi ---
noise_power = np.mean(np.abs(Zxx_noise)**2, axis=1, keepdims=True)
signal_power = np.abs(Zxx)**2
gain = np.maximum(signal_power - noise_power, 0) / (signal_power + 1e-5)
clean_Zxx = Zxx * gain

# --- 4. Ters STFT ---
_, clean_signal = istft(clean_Zxx, fs=fs, nperseg=nperseg)
clean_signal = clean_signal / (np.max(np.abs(clean_signal)) + 1e-10)
clean_signal = (clean_signal * 32767).astype(np.int16)
clean_signal = medfilt(clean_signal, kernel_size=3)

# --- 5. Kaydet ---
wavfile.write(output_path, fs, clean_signal)
print("✅ Temizleme tamamlandı:", os.path.basename(output_path))
