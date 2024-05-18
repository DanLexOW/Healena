# ***Healena***
Ваш помощник в ведении здорового образа жизни :gift_heart:
## Участники проекта:
+ Марьин Даниил Сергеевич (БКЛ232) :pizza:
+ Кукушкина Ольга Андреевна (БКЛ233) :mortar_board:
+	Данченко Алексей Дмитриевич (БКЛ233) :dragon:
+	Герасимова Екатерина Ильинична (БКЛ231) :nail_care:
## Кто такая Healena?
Healena – это Telegram-бот, созданный, чтобы мотивировать пользователей самого популярного мессенджера вести здоровый образ жизни. С помощью этого виртуального помощника можно: 
- рассчитать суточную норму калорий специально для Вас по Вашим характеристикам; 
-	получить рекомендации по физическим тренировкам, основанным на Ваших предпочтениях;
-	узнать некоторые лайфхаки по борьбе с алкогольной и никотиновой зависимостями;
-	а также просто поговорить по душам (функция на этапе разработки).
## Как это работает?
1. Войдите в свой аккаунт в Telegram (Если Вас ещё там нет, то создайте его. Уверены, он Вам ещё пригодится).
2. Напишите в поисковой строке «@Healena_bot».
3. Нажмите на первый и единственный аккаунт в разделе «Глобальный поиск».
4. Вот и всё. Приятного времяпрепровождения с Healen’ой! Будьте здоровы!
## Структура репозитория
+ ***Программирование*** - папка, в которой находится код всех версий бота.
  - _Healena_0_ - самая первая попытка создать какого-либо бота (по сути, не имеет ничего общего с итоговым вариантом)
  - _Healena_1_ - первая версия проекта, в которой добавились основные команды, код счётчика калорий и Базы Данных по тренировкам и продуктам питания.
  - _Healena_2_ - появились функции подбора тренировок и советы по отказу от вредных привычек.
  - _Healena_3_ - готовая и работающая версия бота, однако без парсинга.
  - ***Healena_final*** - итоговый вариант кода бота со всеми функциями и оформлением (**если Вы хотите воспользоваться ботом, Вам нужно содержимое именно этой папки**).
    * _common_
      - bot_commands.py - модель команд меню.
    * _data_base_
      - engine.py - файл для записи движка.
      - models.py - файл для описания таблиц (модели таблиц).
      - orm_query.py - файл для действий с Базой Данных.
    * _filters_
      - chat_types.py - функция, импортируемая в другие файлы с хендлерами, чтобы уточнить, какие роутеры будут работать в каких видах чатов.
    * _handlers_
      - bad_habits.py - хэндлер взаимодействия с пользователем в рамках вредных привычек. 
      - calculator.py - хэндлер взаимодействия с пользователем в рамках калькулятора калорий. 
      - menu_processing.py - управление меню, описание меню, подключение клавиатур.
      - training.py - хэндлер взаимодействия с пользователем в рамках плана тренировок. 
    * _keyboards_
      - inline.py - модель клавиатуры инлайн.
      - reply.py - модель клавиатуры реплай.
    * _middlewares_
      - db.py - создание и подключение сессий для взаимодействия с Базой Данных.
    * aicron.py - подключение выдачи сообщения по времени.
    * main.py - импорт библиотек и функций, подключение диспетчера и роутеров, запуск бота.
    * my_base.db - созданная База Данных.
+ ***Additional*** - папка с дополнительными файлами, которые создавались и/или использовались при написании кода (таблицы, тексты, инструкции, картинки и тд).
+ Файл _Readme.md_, который Вы сейчас читаете :sunglasses:
+ Файл _requirements.txt_ - список всех модулей, необходимых для работы проекта, и их версий.
## Перспективы проекта
- Доработка функции общения с ботом;
- Добавление опции планирования;
- Создание функции напоминания о тренировках/питании и тд.
## Список использованных ресурсов
1. [Telegram бот на python. Курс по разработке Telegram ботов на aiogram 3.](https://www.youtube.com/playlist?list=PLNi5HdK6QEmWLtb8gh8pwcFUJCAabqZh_)
   - [Гитхаб блогера.](https://github.com/PythonHubStudio/aiogram-3-course-telegram-bot)
2. [Официальная документация  aiogram.](https://docs.aiogram.dev/en/dev-3.x/index.html)
3. [Дебажили благодаря.](https://stackoverflow.com/)


