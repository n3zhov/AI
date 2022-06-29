import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from sklearn.metrics import ConfusionMatrixDisplay
from Layers import *


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        loaded = pickle.load(fo, encoding='bytes')
    return loaded['labels']


def plot_training_progress(x, y_data, fig, ax):
    styles = ['k--', 'g-']
    # remove previous plot
    while ax.lines:
        ax.lines.pop()
    # draw updated lines
    for i in range(len(y_data)):
        ax.plot(x, y_data[i], styles[i])
    ax.legend(ax.lines, ['training accuracy', 'validation accuracy'],
              loc='upper center', ncol=2)

def print_loss_accuracy(res):
    print("Initial loss and accuracy = {}, {}".format(res[0][0][1], res[0][0][2]))
    print("Final loss and accuracy = {}, {}".format(res[0][len(res[0])-1][1], res[0][len(res[0])-1][2]))
    print("Validation loss and accuracy = {}, {}".format(res[1][len(res[1])-1][1], res[1][len(res[1])-1][2]))


#Функция для вывода распределения классов в датасете
def bar_dataset_info(labels):
    indexes, counts = np.unique(labels, return_counts=True)
    plt.bar(indexes, counts)
    return plt


class Net:
    def __init__(self):
        self.layers = []

    def add(self, l: Layer):
        self.layers.append(l)

    def forward(self, x):
        for l in self.layers:
            x = l.forward(x)
        return x

    def backward(self, z):
        for l in self.layers[::-1]:
            z = l.backward(z)
        return z

    def update(self, lr):
        for l in self.layers:
            if 'update' in l.__dir__():
                l.update(lr)

    def get_loss_acc(self, x, y, loss=CrossEntropyLoss()):
        p = self.forward(x)
        l = loss.forward(p, y)
        pred = np.argmax(p, axis=1)
        acc = (pred == y).mean()
        return l, acc

    def train_epoch(self, train_x, train_labels, loss=CrossEntropyLoss(), batch_size=4, lr=0.1):
        for i in range(0, len(train_x), batch_size):
            xb = train_x[i:i + batch_size]
            yb = train_labels[i:i + batch_size]

            p = self.forward(xb)
            l = loss.forward(p, yb)
            dp = loss.backward(l)
            dx = self.backward(dp)
            self.update(lr)

    def train_and_plot(self, n_epoch, train_x, train_labels, test_x, test_labels, loss=CrossEntropyLoss(), batch_size=4,
                       lr=0.1):
        fig, ax = plt.subplots()
        ax.set_xlim(0, n_epoch + 1)
        ax.set_ylim(0, 1)

        train_acc = np.empty((n_epoch, 3))
        train_acc[:] = np.NAN
        valid_acc = np.empty((n_epoch, 3))
        valid_acc[:] = np.NAN
        for epoch in range(1, n_epoch + 1):
            self.train_epoch(train_x, train_labels, loss, batch_size, lr)
            tloss, taccuracy = self.get_loss_acc(train_x, train_labels, loss)
            train_acc[epoch - 1, :] = [epoch, tloss, taccuracy]
            vloss, vaccuracy = self.get_loss_acc(test_x, test_labels, loss)
            valid_acc[epoch - 1, :] = [epoch, vloss, vaccuracy]

            ax.set_ylim(0, max(max(train_acc[:, 2]), max(valid_acc[:, 2])) * 1.1)

            plot_training_progress(train_acc[:, 0], (train_acc[:, 2],
                                                          valid_acc[:, 2]), fig, ax)
            fig.canvas.draw()
            fig.canvas.flush_events()

        return train_acc, valid_acc

    def print_confusion_res(self, x, labels, res):
        pred = np.argmax(self.forward(x),axis=1)
        print(ConfusionMatrixDisplay.from_predictions(labels, pred))
        print_loss_accuracy(res)

    def print_confusion(self, x, labels):
        pred = np.argmax(self.forward(x),axis=1)
        print(ConfusionMatrixDisplay.from_predictions(labels, pred))