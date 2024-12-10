import os
import zipfile
import json
import argparse
import datetime


class ShellEmulator:
    def __init__(self, hostname, zip_path, log_path):
        self.hostname = hostname
        self.zip_path = zip_path
        self.log_path = log_path
        self.current_path = "/"
        self.actions = []

        # Загрузка виртуальной файловой системы
        self.load_virtual_filesystem()

    def load_virtual_filesystem(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp/vfs')  # Извлекаем во временную директорию
        print(f"Виртуальная файловая система загружена из {self.zip_path}")

    def log_action(self, action):
        timestamp = datetime.datetime.now().isoformat()
        self.actions.append({"timestamp": timestamp, "action": action})

    def save_log(self):
        with open(self.log_path, 'w') as log_file:
            json.dump(self.actions, log_file, indent=4)

    def ls(self):
        dir_path = os.path.join('/tmp/vfs', self.current_path.lstrip('/'))
        try:
            files = os.listdir(dir_path)
            print("\n".join(files))
            self.log_action(f"ls {self.current_path}")
        except FileNotFoundError:
            print("Директория не найдена.")

    def cd(self, path):
        if path == "..":
            self.current_path = os.path.dirname(self.current_path) or "/"
        else:
            new_path = os.path.join(self.current_path, path)
            if os.path.isdir(os.path.join('/tmp/vfs', new_path.lstrip('/'))):
                self.current_path = new_path
                self.log_action(f"cd {path}")
            else:
                print("Директория не найдена.")

    def uniq(self, filename):
        try:
            with open(os.path.join(self.current_path, filename), 'r') as f:
                lines = f.readlines()
                unique_lines = list(dict.fromkeys(line.strip() for line in lines))
                print("Unique Lines:", unique_lines)  # Для отладки
                for line in unique_lines:
                    print(line)
        except FileNotFoundError:
            print("Файл не найден.")

    def tree(self, path=''):
        full_path = os.path.join('/tmp/vfs', self.current_path.lstrip('/'), path)
        if os.path.isdir(full_path):
            print(path)
            for item in os.listdir(full_path):
                self.tree(os.path.join(path, item))
        else:
            print(path)

    def cal(self):
        from datetime import datetime
        now = datetime.now()
        print(now.strftime("%B %Y"))
        print("Mo Tu We Th Fr Sa Su")
        for i in range(1, 8):
            print(f"{i:2}", end=" ")
        print()

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_path} $ ").strip().split()
            if not command:
                continue

            cmd = command[0]
            if cmd == "exit":
                self.save_log()
                break
            elif cmd == "ls":
                self.ls()
            elif cmd == "cd":
                if len(command) > 1:
                    self.cd(command[1])
                else:
                    print("Укажите путь.")
            elif cmd == "uniq":
                if len(command) > 1:

                    self.uniq(command[1])
                else:
                    print("Укажите имя файла.")
            elif cmd == "tree":
                self.tree()
                self.log_action("tree")
            elif cmd == "cal":
                self.cal()
                self.log_action("cal")
            else:
                print("Неизвестная команда.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки')
    parser.add_argument('--hostname', required=True, help='Имя компьютера для приглашения')
    parser.add_argument('--zip', required=True, help='Путь к архиву виртуальной файловой системы')
    parser.add_argument('--log', required=True, help='Путь к лог-файлу')

    args = parser.parse_args()
    emulator = ShellEmulator(args.hostname, args.zip, args.log)
    emulator.run()

