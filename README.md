# Сервис с mongodb и кэшем

Cервис, в котором будет реализована доска объявлений. К каждому объявлению можно добавлять комментарии и теги. У этого сервиса также доступна статистика по каждому объявлению, в которой дается количество тегов и комментариев.

1. Скачать репозиторий `git clone https://github.com/nsud/fib.git`
2. Перейти в директорию advertisement
3. Поднять докеры `docker-compose up -d`

Доступны следующие методы запросов:
1. `GET` для просмотра информации
2. `POST` для добавления и обновления данных

Примеры хапросов:

```python
import requests


# просмотр информации об объявлении
requests.get(f'http://{YOUR_WEB_IP}/message/{id_message}') 

# добавление нового объявления
data = {'text': {'title': 'name', 'message': 'mess', 'tags': ['tag1'], 'comments': ['comment1']}}
requests.post('http://{YOUR_WEB_IP}/message', params=data) 

# добавление нового комментария
requests.post('http://{YOUR_WEB_IP}/comment/{id_message}', params={'text': 'comm222'})

# добавление нового тега
requests.post('http://{YOUR_WEB_IP}/tag/{id_message}', params={'text': 'tag222'})

# просмотр статистики по объявлению
requests.get(f'http://{YOUR_WEB_IP}/stats/{id_message}') 

```