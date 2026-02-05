import base64
import tempfile
import os
import librosa
import numpy as np

def decode_and_extract(audio_base64: str):
    audio_bytes = base64.b64decode(audio_base64)

    fd, temp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        try:
            y, sr = librosa.load(temp_path, sr=16000)
        except Exception:
            raise ValueError("Invalid audio file")

        # Limit duration
        max_duration = 10
        if len(y) > sr * max_duration:
            y = y[: sr * max_duration]

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        pitch = librosa.yin(y, fmin=50, fmax=300)
        valid_pitch = pitch[pitch > 0]
        pitch_mean = float(np.mean(valid_pitch)) if len(valid_pitch) > 0 else 0.0

        energy = float(np.mean(librosa.feature.rms(y=y)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        return {
            "mfcc_mean": mfcc_mean.tolist(),
            "mfcc_std": mfcc_std.tolist(),
            "pitch": pitch_mean,
            "energy": energy,
            "zcr": zcr
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
