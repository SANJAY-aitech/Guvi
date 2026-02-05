import base64
import tempfile
import os
import librosa
import numpy as np

def decode_and_extract(audio_base64: str):
    audio_bytes = base64.b64decode(audio_base64)

    # Create temp file path (Windows-safe)
    fd, temp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)  # IMPORTANT: close immediately

    try:
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        # Load audio safely
        y, sr = librosa.load(temp_path, sr=16000)

        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # Pitch
        pitch = librosa.yin(y, fmin=50, fmax=300)
        pitch_mean = float(np.mean(pitch[pitch > 0]))

        # Energy
        energy = float(np.mean(librosa.feature.rms(y=y)))

        # ZCR
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        return {
            "mfcc_mean": mfcc_mean.tolist(),
            "mfcc_std": mfcc_std.tolist(),
            "pitch": pitch_mean,
            "energy": energy,
            "zcr": zcr
        }

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
