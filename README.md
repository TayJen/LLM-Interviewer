# LLM-Interviewer

## Статистика по данным

### Deep Learning - Ian Goodfellow

* Общее количество символов: **1768399**
* Общее количество слов: **263367**

### Yandex ML Handbook

* Общее количество символов: **640943**
* Общее количество слов: **81495**

Количество символов и слов по главам:

| Название главы         | Количество символов | Количество слов |
|------------------------|:-------------------:|:---------------:|
| prob_genclass          |        16305        |      1972       |
| ensembles              |        15443        |      2075       |
| cross_validation       |        21843        |      3057       |
| neural_nets            |        72885        |      8776       |
| matrix_diff            |        11821        |      1386       |
| model_evaluation       |        42767        |      5644       |
| intro                  |        33733        |      4637       |
| prob_maxent            |        13497        |      1494       |
| prob_bayes             |        35694        |      4135       |
| optimization           |        89547        |      11260      |
| decision_tree          |        40123        |      5294       |
| prob_calibration       |        12381        |      1499       |
| clustering             |        33116        |      4220       |
| prob_intro             |        17075        |      2122       |
| grad_boost             |        20575        |      2574       |
| hyperparameters_tuning |        32705        |      4214       |
| prob_glm               |        10117        |      1255       |
| ml_theory              |        13547        |      1799       |
| linear_models          |        74505        |      9865       |
| metric_based           |        33264        |      4217       |

### Вопросы-ответы

* Общее количество символов: **635155**
* Общее количество слов: **94046**

Количество вопросов, слов и символов по темам:

| Тема                   | Количество символов | Количество слов | Количество вопросов-ответов |
|------------------------|:-------------------:|:---------------:|:---------------------------:|
| Behaviour              |         351         |       60        |              4              |
| Classic ML             |       196607        |      30664      |             232             |
| Computer vision        |       244649        |      34472      |             110             |
| Deep Learning          |        72793        |      10608      |             43              |
| LLM                    |        65178        |      8942       |             19              |
| Probability_Statistics |        34885        |      5975       |             34              |
| Python                 |        8323         |      1284       |             12              |
| SQL_DB                 |        12369        |      2041       |             12              |

## Оценка качества работы RAG

* Оценивалось, была ли пара вопрос-ответ сгенерирована на основе найденных документов (Accuracy)
* Оценка была по 4 темам (классическое МО, глубокое обучение, вероятностные модели, метрики оценивания)
* 10 пар вопрос-ответ на каждую тему

|          Тема         |       Accuracy      | 
|---------------------- |:-------------------:|
|    Классическое МО    |         90%         |     
|   Глубокое обучение   |         80%         |    
|  Вероятностные модели |         90%         |       
|   Метрики оценивания  |         90%         |     

* Общая Accuracy - 86%
     
## Структура проекта

```
LLM-Interviewer/
├── bot.py                      # Main bot setup and initialization
├── handlers/
│   ├── start.py                # Handles start and topic selection
│   ├── interview.py            # Manages interview flow (question/answer, hint, etc.)
├── utils/
│   ├── question_loader.py      # Utility to load and manage questions from JSON
│   ├── hints.py                # Utility for handling hints
│   ├── resources_loader.py     # Utility to fetch resources for each question
│   └── progress_tracker.py     # Utility for tracking progress and resuming sessions
└── interview_questions.json    # The questions JSON file
```

## Авторы

Евгений Тайчинов и Елизавета Талынкова
