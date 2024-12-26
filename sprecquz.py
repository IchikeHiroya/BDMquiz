import csv
import random
import speech_recognition as sr
import os
import sys

# 標準エラー出力を完全に無効化
sys.stderr = open(os.devnull, 'w')


# 音声認識インスタンスの初期化
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("音声入力を開始します。話してください...")
        try:
            # 標準エラー出力を無効化
            sys.stderr = open(os.devnull, 'w')
            audio = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio, language='ja-JP')
            print(f"認識結果: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("音声を認識できませんでした。もう一度お試しください。")
            return None
        except sr.RequestError as e:
            print("音声認識サービスに接続できません。")
            return None
        except sr.WaitTimeoutError:
            print("音声入力がタイムアウトしました。")
            return None
        finally:
            # 標準エラー出力を元に戻す
            sys.stderr = sys.__stderr__

def load_quizzes(csv_file):
    """CSVファイルからクイズデータを読み込む"""
    quizzes = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quizzes.append({"question": row["question"], "answer": row["answer"]})
    return quizzes

def main():
    # CSVファイルの読み込み
    csv_file = "quizzes.csv"  # クイズデータを格納したCSVファイル名
    quizzes = load_quizzes(csv_file)

    print("\nクイズゲームへようこそ！")

    print("\nゲーム開始！\n")

    while True:
        # クイズをランダムに選択
        quiz = random.choice(quizzes)
        print(f"クイズ: {quiz['question']}")

        # 音声で回答を取得
        print("回答を音声で入力してください。")
        answer = recognize_speech()
        print(f"クイズ: {quiz['question']}")
        if answer is None:
            print("音声入力が認識されなかったため、スキップします。\n")
            continue

        # 正解判定
        if answer.strip() == quiz['answer']:
            print("正解！\n")
        else:
            print(f"不正解。正解は: {quiz['answer']}\n")

        # 次のアクションを確認
        next_action = input("続けますか？ (y: 続ける, r: 結果発表, q: 終了): ")
        if next_action.lower() == 'r':
            print()
        elif next_action.lower() == 'q':
            print("\nゲーム終了！お疲れ様でした！")
            break

if __name__ == "__main__":
    main()
