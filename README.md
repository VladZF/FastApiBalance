# Балансировщик нагрузки на приложение FastAPI

## Инструкция по использованию

### Настройка python

1) Скачайте интерпритатор python по [ссылке](https://www.python.org/)
2) При установке обязательно поставьте галку напротив **add to PATH** для корректной работы
3) Клонируйте репозиторий
4) Откройте терминал в папке с проектом
5) Введите команду 
```bash 
pip install -r requirements
```

### Запуск приложения

Для запуска сначала необходимо запустить балансер командой

```bash
python app/main.py
```

Затем подключить экземпляры внутреннего приложения. В отдельных терминалах необходимо ввести следующие команды

```bash
python instances/instance1.py
python instances/instance2.py
python instances/instance3.py
```

После запуска можно работать с приложением. Для этого в браузере введите url в формате
```http://<host>:<main_port>/docs```. Нажмите на вкладку getInfo, далее на Try it out и execute. Вам будет выдан ответ от одного из внутренних приложений. В логах балансера будет выдано сообщение, в котором будет указан экземпляр, ответивший на запрос.
Запросы распределяются между внутренними приложениями по алгоритму Robin Round - каждый новый запрос отправляется на следующий доступный экземпляр в циклическом порядке.
Если экземпляр не отвечает за 5 попыток, интервал между которыми полсекунды, то он удаляется из пула доступных копий и обращение к данному экземпляру уже не производится. В случае, если никакой экземпляр не отвечает, то сервер выдает код 503 с сообщением, что нет ни одного экземпляра.

### Тестовый клиент
Когда приложение полностью запущено, можно запустить файл test_client.py командой
```bash
python tests/test_client.py
```
Клиент пошлет несколько запросов в приложение и в терминал выдаст ответы с сервера, а затем выведет статистику по использованию каждой копии