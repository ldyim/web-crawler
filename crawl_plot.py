import matplotlib.pyplot as plt
import numpy as np



def plot_graph(title, xlabel, ylabel, data, filename):
    plt.figure()
    plt.plot(*zip(*data))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.show()
    plt.savefig(filename)
    plt.close()
    
def plot_bar_graph(title, xlabel, ylabel, data, filename):
    plt.figure()
    plt.barh(*zip(*data))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.show()
    plt.savefig(filename)
    plt.close()