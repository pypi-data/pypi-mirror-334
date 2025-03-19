from watchdog.events import FileSystemEventHandler
import subprocess
import time
import sys


class RestartHandler(FileSystemEventHandler):
    """Отслеживает изменения в файлах и перезапускает сервер."""
    
    def __init__(self):
        self.server_process = None
        self.restart_delay = 1  # Задержка перед перезапуском
        self.restart()

    def restart(self):
        """Перезапускает сервер."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

        print("\n[INFO] Запускаем сервер...")
        self.server_process = subprocess.Popen([sys.executable, "server.py"])

    def on_modified(self, event):
        """Перезапуск сервера при изменении Python-файлов."""
        if event.src_path.endswith(".py"):
            print(f"[INFO] Файл изменен: {event.src_path}")
            print("[INFO] Перезапускаем сервер через 1 секунду...\n")
            time.sleep(self.restart_delay)
            self.restart()
