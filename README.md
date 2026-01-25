# FastAI

## Локальное развертывание приложения

Инструкции и справочная информация по разворачиванию локальной инсталляции собраны
в документе [CONTRIBUTING.md](./CONTRIBUTING.md).

### Настройка приложения

### Настройка переменных окружения

В корне репозитория создайте файл .env и скопируйте туда содержимое файла example.env. Добавьте значения переменных:

- FASTAI_DEEPSEEK__API_KEY - Ваш АПИ-ключ, полученный при регистрации на DeepSeek
- FASTAI_UNSPLASH__API_KEY - Ваш АПИ-ключ, полученный при регистрации на Unsplash
- FASTAI_STORAGE__ENDPOINT_URL - URL вашего хранилища S3
- FASTAI_STORAGE__BUCKET_NAME - имя публичного (важно!) бакета для сохранения сгенерированных сайтов
- FASTAI_STORAGE__ACCESS_KEY - Access key для доступа к хранилищу S3
- FASTAI_STORAGE__SECRET_KEY - Secret key для доступа к хранилищу S3

Если используются промежуточные провайдеры для доступа к Deepseek и/или Unsplash, отредактируйте значения переменных:
- FASTAI_DEEPSEEK__BASE_URL - URL API DeepSeek, см. [документацию](https://api-docs.deepseek.com/quick_start/pricing), пример: `https://api.deepseek.com`
- FASTAI_DEEPSEEK__MODEL - Название модели DeepSeek, см. [документацию](https://api-docs.deepseek.com/quick_start/pricing)
- FASTAI_UNSPLASH__BASE_URL - URL API Unsplash, см. [документацию](https://unsplash.com/documentation#creating-a-developer-account), пример: `https://api.unsplash.com`

Для продвинутых пользователей - для тонкой настройки параметров хранилища S3 отредактируйте переменные:
- FASTAI_STORAGE__MAX_POOL_CONNECTIONS - число параллельных операций
- FASTAI_STORAGE__CONNECT_TIMEOUT - таймаут подключения
- FASTAI_STORAGE__READ_TIMEOUT - таймаут чтения данных

### Локальный запуск приложения

В терминале введите команду:
```shell
$ make run
```
Приложение будет доступно по адресу http://127.0.0.1:5000/

### Использование приложения
1. Откройте страницу по адресу http://127.0.0.1:5000/;
2. В текстовое поле введите промпт для создания сайта (например - Сайт любителей пива) и нажмите Enter;
3. Ожидайте завершения процесса генерации;
4. Сгенерированные сайты доступны для просмотра и скачивания по ссылке Профиль/Мои сайты