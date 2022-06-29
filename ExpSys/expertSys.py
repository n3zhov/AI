from pyknow import *

stopAsking = False


class AdviseCountry(KnowledgeEngine):
    @Rule(OR(
        AND(
            AND(Fact('Пляжный'), Fact('Активный')),
            Fact('Экстремальный')),
        Fact('Подводный мир')))
    def diving(self):
        self.declare(Fact('Дайвинг'))

    @Rule(OR(
        AND(
            AND(Fact('Пляжный'), Fact('Активный')),
            Fact('Экстремальный')),
        Fact('Скейтборд')))
    def surfing(self):
        self.declare(Fact('Серфинг'))

    @Rule(AND(Fact('Активный'), Fact('Культурный')))
    def excursions(self):
        self.declare(Fact('Экскурсии'))

    @Rule(AND(Fact('Людные мероприятия'), Fact('Культурный')))
    def fests(self):
        self.declare(Fact('Фестивали'))

    @Rule(AND(Fact('Активный'), Fact('Экстремальный'), Fact('Горнолыжный')))
    def ski(self):
        self.declare(Fact('Лыжи/Сноуборд'))

    @Rule(AND(Fact('Местная кухня'), Fact('Культурный')))
    def food(self):
        self.declare(Fact('Гастрономия'))

    @Rule(AND(Fact('Магазины'), Fact('Культурный')))
    def shopping(self):
        self.declare(Fact('Шоппинг'))

    @Rule(OR(
        AND(Fact('Дайвинг'), Fact('Дешево'), NOT(Fact('Без загранника'))),
        AND(Fact('Серфинг'), Fact('Дешево'), NOT(Fact('Без загранника'))),
        AND(Fact('Лыжи/Сноуборд'), Fact('Дешево'), NOT(Fact('Без загранника'))),
        AND(Fact('Гастрономия'), Fact('Дешево'), NOT(Fact('Без загранника'))),
        AND(Fact('Шоппинг'), Fact('Дешево'), NOT(Fact('Без загранника')))))
    def turkey(self):
        self.declare(Fact(country='Турция'))

    @Rule(OR(
        AND(Fact('Серфинг'), Fact('Дешево'), Fact('Без загранника')),
        AND(Fact('Экскурсии'), Fact('Дешево'), Fact('Без загранника')),
        AND(Fact('Фестивали'), Fact('Дешево'), Fact('Без загранника')),
        AND(Fact('Лыжи/Сноуборд'), Fact('Дешево'), Fact('Без загранника')),
        ))
    def russia(self):
        self.declare(Fact(country='Россия'))

    @Rule(OR(
        AND(Fact('Дайвинг'), Fact('Дорого'), NOT(Fact('Без загранника'))),
        AND(Fact('Экскурсии'), Fact('Дорого'), NOT(Fact('Без загранника'))),
        AND(Fact('Фестивали'), Fact('Дорого'), NOT(Fact('Без загранника'))),
        AND(Fact('Лыжи/Сноуборд'), Fact('Дорого'), NOT(Fact('Без загранника'))),
        AND(Fact('Гастрономия'), Fact('Дорого'), NOT(Fact('Без загранника'))),
        AND(Fact('Шоппинг'), Fact('Дорого'), NOT(Fact('Без загранника'))),
    ))
    def italy(self):
        self.declare(Fact(country='Италия'))

    @Rule(OR(
        AND(Fact('Дайвинг'), Fact('Дорого'), Fact('Тропический климат'), NOT(Fact('Без загранника'))),
        AND(Fact('Серфинг'), Fact('Дорого'), Fact('Тропический климат'), NOT(Fact('Без загранника'))),
    ))
    def maldives(self):
        self.declare(Fact(country='Мальдивы'))

    @Rule(Fact(country=MATCH.a))
    def print_result(self, a):
        global stopAsking
        stopAsking = True
        print('Страна - {}'.format(a))

    def factz(self, l):
        for x in l:
            self.declare(x)


if __name__ == '__main__':
    ex1 = AdviseCountry()
    ex1.reset()

    print("Вам будут задаваться вопросы, отвечайте при помощи y или n y означает да, n означает нет")

    print('У вас большой бюджет?')
    c = str(input())
    if c == 'y':
        ex1.declare(Fact('Дорого'))
    elif c == 'n':
        ex1.declare(Fact('Дешево'))

    questions = (['Вы любите тропический климат?',
                  'У вас нет загран паспорта?',
                  'Хочется посмотреть подводный мир?',
                  'Вы хотите отдыхать на пляже?',
                  'Предпочитаете активный отдых?',
                  'Занимаетесь экстремальными видами спорта?',
                  'Вы катались на скейтборде?',
                  'Вас интересует культурный туризм?',
                  'Вы хотели бы посетить людные мероприятия?',
                  'Вы хотели бы отдохнуть в горах?',
                  'Интересует местная кухня?',
                  'Хотите пройтись по магазинам?'])
    facts = (['Тропический климат', 'Без загранника', 'Дайвинг', 'Пляжный', 'Активный', 'Экстремальный', 'Скейтборд',
              'Культурный', 'Людные мероприятия', 'Горнолыжный', 'Местная кухня', 'Магазины'])

    for question, fact in zip(questions, facts):
        if not stopAsking:
            print(question)
            c = str(input())
            if c == 'y':
                ex1.declare(Fact(fact))
            elif c == 'n':
                continue
            ex1.run()
        else:
            break
