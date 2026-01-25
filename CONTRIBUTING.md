# Разработчикам бэкенда

[TOC]

## Как развернуть локально

### Необходимое ПО

Для запуска ПО вам понадобятся консольный Git и Make. Инструкции по их установке ищите на
официальных сайтах:

- [Git SCM](https://git-scm.com/)
- [GNU Make](https://www.gnu.org/software/make/)

Вы можете проверить, установлены ли эти программы с помощью команд:
```shell
$ git --version
git version 2.37.1.windows.1

$ make --version
GNU Make 4.4.1
Built for Windows32
<...>
```

Для тех, кто использует Windows необходимы также программы **git** и **git bash**. В **git bash** необходимо дополнительно установить
**make**:

- Перейдите на сайт [ezwinports](https://sourceforge.net/projects/ezwinports/files/)
- Скачайте `make-4.4.1-without-guile-w32-bin.zip` (выберите версию без `guile`)
- Извлеките архив
- Скопируйте содержимое архива в `C:\ProgramFiles\Git\mingw64\` **БЕЗ** перезаписи/замены любых вложенных файлов.

Все дальнейшие команды запускать из-под **git bash**.

### Создание виртуального окружения для работы с IDE

IDE для корректной работы подсказок необходимо развернуть виртуальное окружение со всеми установленными зависимостями.

В качестве пакетного менеджера на проекте используется [uv](https://docs.astral.sh/uv/).

[Установите uv](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/Uv-package-manager#1-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-uv) и в корне репозитория выполните команду

```shell
$ uv sync
```

[uv](https://docs.astral.sh/uv/) создаст виртуальное окружение, установит необходимую версию Python и все необходимые зависимости.

После этого активируйте виртуальное окружение в текущей сессии терминала:

```shell
$ source .venv/bin/activate  # для Linux
$ .\.venv\Scripts\activate  # Для Windows
```

### Локальное развертывание хранилища S3
Из папки проекта запустите команду:
```shell
$ docker compose -f docker-compose-minio.yml up -d
```
В браузере откройте веб-консоль minio по адресу http://localhost:9001/. В разделе Buckets создайте бакет с именем fastai (можено использовать свое имя). В совйствах бакета установите Access Policy: Public.
В разделе Access keys создайте ключи доступа. Сохраните Access Key и Secret Key (они понадобятся далее при настройке переменных окружения).

### Настройка pre-commit хуков

В репозитории используются хуки [pre-commit](https://pre-commit.com/), чтобы автоматически запускать линтеры и автотесты.

В корне репозитория в **активированном виртуальном окружении** запустите команду для настройки хуков:

```shell
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

В последующем при коммите автоматически будут запускаться линтеры и другие проверки. Если проверки не пройдут, то коммит прервётся с ошибкой.

Если вам потребуется сделать коммит без проверок, то вы можете отключить их с помощью флага `--no-verify`:
```shell
git commit -m 'Message' --no-verify
```

### Настройка переменных окружения

В корне репозитория создайте файл .env и скопируйте туда содержимое файла example.env. Добавьте/отредактируйте значения переменных:
- FASTAI_DEEPSEEK__BASE_URL - URL API DeepSeek, см. [документацию](https://api-docs.deepseek.com/quick_start/pricing), пример: `https://api.deepseek.com`
- FASTAI_DEEPSEEK__MODEL - Название модели DeepSeek, см. [документацию](https://api-docs.deepseek.com/quick_start/pricing)
- FASTAI_DEEPSEEK__API_KEY - Ваш АПИ-ключ, полученный при регистрации на DeepSeek
- FASTAI_UNSPLASH__BASE_URL - URL API Unsplash, см. [документацию](https://unsplash.com/documentation#creating-a-developer-account), пример: `https://api.unsplash.com`
- FASTAI_UNSPLASH__API_KEY - Ваш АПИ-ключ, полученный при регистрации на Unsplash
- FASTAI_STORAGE__ENDPOINT_URL - URL вашего хранилища S3
- FASTAI_STORAGE__BUCKET_NAME - имя публичного (важно!) бакета для сохранения сгенерированных сайтов
- FASTAI_STORAGE__ACCESS_KEY - Access key для доступа к хранилищу S3
- FASTAI_STORAGE__SECRET_KEY - Secret key для доступа к хранилищу S3
- FASTAI_STORAGE__MAX_POOL_CONNECTIONS - число параллельных операций
- FASTAI_STORAGE__CONNECT_TIMEOUT - таймаут подключения
- FASTAI_STORAGE__READ_TIMEOUT - таймаут чтения данных

## Как вести разработку

Код проекта находится в папке `/src`.

Находясь в корневой директории проекта, запустить проект можно командой:

```shell
$ fastapi dev src/main.py
```

Проект будет работать по адресу http://127.0.0.1:8000/

### Как установить python-пакет в виртуальное окружение

В качестве менеджера пакетов используется [uv](https://docs.astral.sh/uv/).

Вот пример как добавить в зависимости библиотеку `beautifulsoup4`.

```shell
$ uv add beautifulsoup4
```

Конфигурационные файлы `pyproject.toml` и `uv.lock` обновятся автоматически.

Аналогичным образом можно удалять python-пакеты:

```shell
$ uv remove beautifulsoup4
```

Если необходимо обновить `uv.lock` вручную, то используйте команду:

```shell
$ uv lock
```

### Команды для быстрого запуска с помощью make

Для вывода списка часто используемых коротких команд используйте команду

```shell
$ make list
...
```

### Локальное развертывание фронтэнда
В папке фронтэнда (frontend/) создать файл frontend-settings.json со следующим содержимым:
```json
{
    "backendBaseUrl": "/frontend-api/"
}
```