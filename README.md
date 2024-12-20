# Постановка задачи
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
zip. Эмулятор должен работать в режиме CLI.
Ключами командной строки задаются:
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
Лог-файл имеет формат json и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указаны дата и время.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. uniq.
2. tree.
3. cal.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

# Shell Emulator

## Описание
Этот проект представляет собой эмулятор командной оболочки, который позволяет выполнять некоторые базовые команды файловой системы, такие как `ls`, `cd`, `exit`, `uniq`, `tree` и `cal`. Он написан на Python и включает тесты для проверки функциональности.

### Файлы
- **emulator.py**: основной файл, в котором реализован класс `ShellEmulator`, позволяющий выполнять базовые операции с файловой системой.
- **emulator_test.py**: файл с тестами для проверки правильности работы класса `ShellEmulator`, используя библиотеку `unittest`.

## Установка

1. Убедитесь, что у вас установлен Python (версии 3.6 и выше).
2. Клонируйте этот репозиторий или загрузите файлы:
   ```bash
   git clone <URL_TO_REPOSITORY>
   cd <DIRECTORY_NAME>
   ```
Установите необходимые зависимости (при наличии):

  ```pip install -r requirements.txt```

## Использование

Чтобы использовать эмулятор, в консоли пропишите:

```python emulator.py --hostname "my_computer" --zip "files.zip" --log "log.json"```

(при условии, что поинтер текущей директории находится в папке проекта, иначе - нужно прописать путь до файла emulator.py)

## Доступные команды

### 1. ls
Команда ls используется для отображения содержимого текущей директории.

#### Описание:
- Функция: Перебирает все файлы и директории в текущем пути и выводит их названия.
- Обработка ошибок: 
  - Если указанная директория не существует, выводится сообщение "Директория не найдена."
  - Если директория пуста, не производится никакой вывод (т.е. нет вызовов print).

### Пример использования:

current_path = '/path/to/your/directory'
ls

### 2. cd
Команда cd (change directory) используется для смены текущей директории.

#### Описание:
- Синтаксис: cd <путь>
- Функция: Меняет текущую директорию на указанную.
- Обработка ошибок: Если указанная директория не существует, выводится сообщение "Директория не найдена."

### Пример использования:

cd '/path/to/new/directory'

### 3. exit
Команда exit используется для выхода из эмулятора.

#### Описание:
- Функция: Завершает выполнение эмулятора.
- Примечание: Просто вызывает выход из программы.

### Пример использования:

exit

### 4. uniq
Команда uniq используется для фильтрации повторяющихся строк в текстовых файлах.

#### Описание:
- Синтаксис: uniq <файл>
- Функция: Сравнивает строки в указанном файле и выводит только уникальные.

### Пример использования:

uniq 'input.txt'

### 5. tree
Команда tree отображает дерево директорий и файлов в текущем пути.

#### Описание:
- Функция: Выводит иерархию директорий и файлов в виде дерева.

### Пример использования:

tree

### 6. cal
Команда cal выводит календарь.

#### Описание:
- Функция: Показывает текущий месяц и год в виде календаря.

### Пример использования:

cal

## Запуск тестов
Чтобы запустить тесты для эмулятора, в консоли пропишите

```python -m unittest emulator_test.py```

(при условии, что поинтер текущей директории находится в папке проекта, иначе - нужно прописать путь до файла emulator_test.py)


