import csv
import random
import speech_recognition as sr
import os
import sys

def recognize_speech():
    """音声を認識し、テキストとして返す"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("音声入力を開始します。話してください...")
        try:
            audio = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio, language='ja-JP')
            print(f"認識結果: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("音声を認識できませんでした。もう一度お試しください。")
            return None
        except sr.RequestError:
            print("音声認識サービスに接続できません。")
            return None
        except sr.WaitTimeoutError:
            print("音声入力がタイムアウトしました。")
            return None

def load_quizzes(csv_file):
    """CSVファイルからクイズデータを読み込む"""
    quizzes = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quizzes.append({"id": row["id"], "question": row["question"], "answer": row["answer"]})
    return quizzes

def main():
    csv_file = "quizzes.csv"  # クイズデータを格納したCSVファイル名
    quizzes = load_quizzes(csv_file)

    print("\nクイズゲームへようこそ！")

    current_question_number = 0
    status = "syutudai"  # 初期状態は問題出題

    while True:
        if status == "syutudai":
            # 状態1: 問題文を提示する状態
            quiz = random.choice(quizzes)
            current_question_number += 1

            print(f"\n第{current_question_number}問")
            print(f"クイズ: {quiz['question']}")

            input("準備ができたらEnterキーを押してください。")
            status = "kaitou"

        elif status == "kaitou":
            # 状態2: 解答待機状態
            print("回答を音声で入力してください。")
            answer = recognize_speech()
            if answer is None:
                print("音声入力が認識されなかったため、スキップします。\n")
                status = "syutudai"
                continue
            user_answer = answer.strip()
            status = "judge"

        elif status == "judge":
            # 状態3: 正誤判定状態
            if user_answer == quiz['answer']:
                print("正解！\n")
            else:
                print(f"不正解。正解は: {quiz['answer']}\n")
            status = "continue_check"

        elif status == "continue_check":
            # 状態4: 続けるかどうかを判定する状態
            print("続けますか？『続ける』『もう一問』『終了』と答えてください。")
            next_action = recognize_speech()

            if next_action is None:
                print("音声が認識されませんでした。続行操作はありません。\n")
                continue

            next_action = next_action.strip()
            if next_action in ["続ける", "もう一問"]:
                status = "syutudai"
            elif next_action == "終了":
                print("\nゲーム終了！お疲れ様でした！")
                break

if __name__ == "__main__":
    main()
