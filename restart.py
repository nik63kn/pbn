import os
import subprocess
import time
import sys


def restart_flask():
    # Найти PID процесса на порту 5000
    try:
        result = subprocess.run(['lsof', '-t', '-i:5000'], capture_output=True, text=True)
        pids = result.stdout.strip().split('\n')

        # Убить процессы
        for pid in pids:
            if pid:
                print(f"Убиваю процесс {pid}...")
                os.system(f"kill -9 {pid}")
                time.sleep(0.5)
    except Exception as e:
        print(f"Ошибка при поиске/убийстве процесса: {e}")

    # Запустить Flask
    print("Запускаю Flask...")
    os.system("python app.py")


if __name__ == "__main__":
    restart_flask()
