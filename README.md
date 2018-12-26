## DebtsBot
#### Telegram бот для зберігання боргів


### Необхідне ПО і бібліотеки: 

- компілятор Python (Pycharm etc.)
- Python 3 
- pyTelegramBotAPI v.3.6.6
- pymongo v.3.7.2

### Запуск бота
- Cтворити бота за допомогою Telegram бота @BotFather, отриманий токен помістити у змінну token у файлі config.py
- Зареєструйтесь на mLab, створіть бд, помість url бази даних у змінну dbtoken у файлі config.py
- Щоб розгорнути свій проект на сервері зареєструйтесь на heroku.com і виконайте кроки відповідно до гайду 
https://devcenter.heroku.com/articles/getting-started-with-python

### Запуск бота за допомогою системи збірки PyInstaller
1. Встановити PyInstaller із PyPI: <br/>
    pip install pyinstaller
2. Перейдіть до директорію де міститься програма та запустіть:<br/>
pyinstaller --onefile main.py <br/>
Ця дія згенерує виконавчий файл у піддиректорії dist <br/>
3. Запустити цей файл

### Запуск бота за допомогою Docker
1. docker build -t bot .
2. docker run -p 80:80 -v ${pwd}:${pwd}/app/ bot

### Автори:
Команда: КІА
- **К**оля Тарановський 
- **І**лля Зубар 
- **А**ндрій Шурук
