from faster_whisper import WhisperModel
import pyaudio
import numpy as np
import wave
import os

# Whisper モデルのロード
model = WhisperModel("large-v3", device="cpu", compute_type="int8")

# PyAudio 設定
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

print("Recording...")

# 音声データをバッファに蓄積
buffer = np.array([], dtype=np.int16)
file_count = 0  # ファイル番号カウンタ

try:
    while True:
        # PyAudio からデータ取得
        data = stream.read(1024, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)

        # バッファにデータを追加
        buffer = np.concatenate((buffer, audio))

        # 5秒分の音声が蓄積されたら処理
        if len(buffer) >= 16000 * 3:  # 5秒分のサンプル数
            # ファイル名を作成
            file_name = f"recording_{file_count}.wav"
            file_count += 1

            # バッファをWAVファイルとして保存
            with wave.open(file_name, 'wb') as wf:
                wf.setnchannels(1)  # モノラル
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(16000)  # サンプリングレート
                wf.writeframes(buffer[:16000 * 5].tobytes())

            print(f"Saved {file_name}")

            # WAVファイルをモデルに渡して文字起こし
            segments, info = model.transcribe(
                file_name,
                beam_size=5,
                vad_filter=True,
                without_timestamps=True,
            )

            # 結果を表示
            print("Transcription:")
            for segment in segments:
                print(segment.text.strip())

            # 処理済みデータをバッファから削除
            buffer = buffer[16000 * 5:]

except KeyboardInterrupt:
    print("Recording stopped.")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # PyAudio終了後に環境変数を無効化
    os.environ["ALSA_DEBUG"] = "0"
