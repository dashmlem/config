import unittest
from unittest.mock import patch, MagicMock
import os
import json
import shutil
import zipfile


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем временную директорию для тестирования
        cls.test_dir = '/tmp/test_vfs'
        os.makedirs(cls.test_dir, exist_ok=True)

        # Создаем тестовые файлы
        cls.test_file = os.path.join(cls.test_dir, 'test.txt')
        with open(cls.test_file, 'w') as f:
            f.write("line1\nline2\nline2\nline3\nline1\n")

        # Создаем zip-файл виртуальной файловой системы
        cls.zip_file = '/tmp/test_vfs.zip'
        with zipfile.ZipFile(cls.zip_file, 'w') as zip_ref:
            zip_ref.write(cls.test_file, arcname='test.txt')

    @classmethod
    def tearDownClass(cls):
        # Удаляем временные файлы и директории
        os.remove(cls.zip_file)
        shutil.rmtree(cls.test_dir)

    def setUp(self):
        # Перед каждым тестом мы создаем эмулятор
        from emulator import ShellEmulator
        self.emulator = ShellEmulator('test_host', self.zip_file, '/tmp/test_log.json')
        self.emulator.load_virtual_filesystem()

    def tearDown(self):
        # Удаление лог-файла после каждого теста
        log_file_path = '/tmp/test_log.json'
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

    def test_ls_non_existent_directory(self):
        # Тест для несуществующей директории
        self.emulator.current_path = '/non_existent_directory'  # Устанавливаем несуществующий путь

        with patch('builtins.print') as mocked_print:
            self.emulator.ls()  # Запускаем метод ls

            # Проверяем, что был вызван print с сообщением об ошибке
            mocked_print.assert_called_once_with("Директория не найдена.")

    def test_ls_no_dir(self):
        self.emulator.current_path = '/non_existent_dir'
        with patch('builtins.print') as mocked_print:
            self.emulator.ls()
            mocked_print.assert_called_once_with("Директория не найдена.")

    def test_cd(self):
        self.emulator.cd('dir1')  # Измените на корректный подкаталог
        self.assertEqual(self.emulator.current_path, '/dir1')

    def test_cd_invalid_dir(self):
        with patch('builtins.print') as mocked_print:
            self.emulator.cd('non_existent')
            mocked_print.assert_called_once_with("Директория не найдена.")

    def test_cd_to_file(self):
        # Проверка попытки перейти в файл вместо директории
        original_path = self.emulator.current_path
        self.emulator.cd('test.txt')  # попытаемся перейти в файл
        self.assertEqual(self.emulator.current_path,
                         original_path)  # Проверяем, что текущая директория осталась неизменной

    def test_uniq(self):
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write("line1\nline2\nline2\nline3\nline1\n")  # Подготовка файла с дубликатами

        self.emulator.current_path = self.test_dir  # Установите путь к тестовой директории
        with patch('builtins.print') as mocked_print:
            self.emulator.uniq('test.txt')

            # Получите список вызовов
            print_calls = [call[0][0] for call in mocked_print.call_args_list]

            # Проверяем, что все уникальные строки выведены
            self.assertIn("line1", print_calls)
            self.assertIn("line2", print_calls)
            self.assertIn("line3", print_calls)

    def test_uniq_file_not_found(self):
        with patch('builtins.print') as mocked_print:
            self.emulator.uniq('non_existent.txt')
            mocked_print.assert_called_once_with("Файл не найден.")

    def test_tree(self):
        with patch('builtins.print') as mocked_print:
            self.emulator.tree()
            mocked_print.assert_called_with("test.txt")

    def test_cal(self):
        with patch('builtins.print') as mocked_print:
            self.emulator.cal()
            mocked_print.assert_called()  # Проверяем, что cal выводит что-то

if __name__ == '__main__':
    unittest.main()

''' python -m unittest emulator_test.py'''