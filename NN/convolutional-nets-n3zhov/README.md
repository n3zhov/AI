[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7966964&assignment_repo_type=AssignmentRepo)
# Лабораторная работа по курсу "Искусственный интеллект"
# Классификация изображений.

| Студент | Ежов Никита Павлович |
|------|------|
| Группа  | М8О-307Б-19 |
| Оценка 1 (обучение "с нуля") | *X* |
| Оценка 2 (transfer learning) | *X* |
| Проверил | Сошников Д.В. |

> *Комментарии проверяющего*
### Задание

Решить задачу классификации пород кошек и собак на основе датасета [Oxford-IIIT](https://www.robots.ox.ac.uk/~vgg/data/pets/).

![Dataset we will deal with](images/data.png)

#### Задание 1: Классификация Pet Faces

Обучить свёрточную нейронную сеть для классификации пород кошек и собак на основе упрощённого датасета **Pet Faces**. Самостоятельно придумать архитектуру сети, реализовать предобработку входных данных.

Для загрузки датасета используйте следующий код:

```python
!wget https://mslearntensorflowlp.blob.core.windows.net/data/petfaces.tar.gz
!tar xfz petfaces.tar.gz
!rm petfaces.tar.gz
```

В качестве результата необходимо:

* Посчитать точность классификатора на тестовом датасете
* Посчитать точность двоичной классификации "кошки против собак" на текстовом датасете
* Построить confusion matrix
* **[На хорошую и отличную оценку]** Посчитайте top-3 accuracy
* **[На отличную оценку]** Выполнить оптимизацию гиперпараметров: архитектуры сети, learning rate, количества нейронов и размеров фильтров.

## Первая часть ЛР

Было сделано следующее: 

1. Построена архитектура сети со свёрточными слоями
2. Был произведён поиск подходящих гиперпараметров при помощи GridSearchCV из scikit-learn.
* Во время выполнения данной части лабораторной работы я понял следующее: 
* 1) поиск подходящих параметров должен производиться на уменьшенном количестве данных 
* 2) нужно заранее понимать, из какого диапазона будут производиться поиски.
* 3) нужно идти на компромисс относительно подбираемых параметров. Так например в своей работе я не стал реализовывать подбор сети из разного количества слоёв, а также я не искал параметры для свёрточного слоя. В итоге я искал следующие значения: подходящий алгоритм оптимизации, коэффициент для него, количество нейронов на двух конечных слоях с функцией relu. Конечно, я бы мог произвести гораздо более длительный перебор, но времени было уже мало.
3. Аугментация изображений важна, но в меру. Первое, что я попробовал сделать, когда получил низкую точность - сделать все возможные модификации изображения, т.е. поворот по горизонтали, диагонали, изменение масштаба, яркости, "перемешивание" rgb каналов и т.д., из-за чего проблема переобучения хоть и исчезала, но появлялись очень медленные темпы обучения. Потом я осознал, что в первую очередь надо произвести оптимизацию гиперпараметров, а уже потом делать аугментацию изображений.

Не могу не отметить плохую реализацию преобразования модели из keras в эквивалентную для scikit-learn. Документация по соответсвующей функции банально удалена, она помечена как deprecated, при этом пакет, который предлагают на замену, банально не работает и мигрировать на него было настолько сложно, что я выбрал проводить оптимизацию до конца на модели, полученной из keras.

Также обучение нейросети с нуля не позволило добиться высоких результатов точности для задачи многоклассовой классификации, но при этом при задаче разделения кошек/собак модель показала себя очень неплохо.

Решение оформите в файле [Faces.ipynb](Faces.ipynb).



Использовать нейросетевой фреймворк в соответствии с вариантом задания:
   * Чётные варианты - PyTorch
   * Нечётные варианты - Tensorflow/Keras
#### Задание 2: Классификация полных изображений с помощью transfer learning

Используйте оригинальный датасет **Oxford Pets** и предобученные сети VGG-16/VGG-19 и ResNet для построение классификатора пород. Для загрузки датасета используйте код:

```python
!wget https://mslearntensorflowlp.blob.core.windows.net/data/oxpets_images.tar.gz
!tar xfz oxpets_images.tar.gz
!rm oxpets_images.tar.gz
```

В качестве результата необходимо:

* Посчитать точность классификатора на тестовом датасете отдельно для VGG-16/19 и ResNet, для дальнейших действий выбрать сеть с лучшей точностью
* Посчитать точность двоичной классификации "кошки против собак" на тестовом датасете
* Построить confusion matrix
* **[На отличную оценку]** Посчитайте top-3 и top-5 accuracy

Решение оформите в файле [Pets.ipynb](Pets.ipynb).

Использовать нейросетевой фреймворк, отличный от использованного в предыдущем задании, в соответствии с вариантом задания:
   * Нечётные варианты - PyTorch
   * Чётные варианты - Tensorflow/Keras


## Вторая часть ЛР
Во время выполнения данной ЛР я ощутил заметную разницу между подходами pytorch и tensorflow+keras. Если при помощи последнего фреймворка мне удавалось относительно не раздувать код, т.к. большая часть необходимого функционала была уже "из коробки", то в случае pytorch при попытке найти документацию по похожему принципу я натыкался на то, что очень многое внутри него реализовано руками. Поэтому приходилось буквально склеивать лабораторную из кусочков, найденных по интернету и пытаться в них разобраться. За исключением вручную написанных функций для тренировки по количеству эпох и классов для загрузки/преобразования датасета в ЛР было сделано не так уж и много. Логика вычисления top-n accuracy стала понятна после первой части ЛР, поэтому реализовать её здесь не было особых проблем. Также во время transfer learning я не решился "размораживать" слои верхушки vgg16 и resnet, т.к. я был удовлетворён той точностью, которая получилась в результате обучения. Не производил оптимизацию параметров, т.к. из прошлой работы было ясно, что алгоритм оптимизации Adam c lr=10e-3 очень хорошо подходит для обучения сетей на подобных задачах.
## Материалы для изучения

* [Deep Learning for Image Classification Workshop](https://github.com/microsoft/workshop-library/blob/main/full/deep-learning-computer-vision/README.md)
* [Convolutional Networks](https://github.com/microsoft/AI-For-Beginners/blob/main/4-ComputerVision/07-ConvNets/README.md)
* [Transfer Learning](https://github.com/microsoft/AI-For-Beginners/blob/main/4-ComputerVision/08-TransferLearning/README.md)
