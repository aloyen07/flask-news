# Что ты такое?!
Это - сайт новостей. Тут можно просматривать и создавать новости. Правда, заспамить вас флудом тоже могут ибо модерации нет))0) А удалять новости можно только через прямой запрос в MySQL. 
Приятного пользования :з

## Технологии
Использованы модули: Flask, Flask-WTF, SQLAlchemy

### Как оживить этого инвалида?
Скачайте архив, распакуйте его, в консоли перейдите в директорию этого проета и пропишите...
```
python -m venv envirovment
```
Далее, активируйте виртуальное кружение...
Для Linux:
```
source ./envirovment/bin/activate
```
Для Windows:
```
source ./envirovment/Scripts/activate
```
И далее допишите:
```
pip install -r requirements.txt
```
Для запуска в директории проекта перейдите в виртуальное окружение и пропишите...
```
flask run
```