import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

def plot_time_series_comparison(y_true, y_pred, time_range=None, title="Comparação de Séries Temporais", figsize=(10, 5)):
    if isinstance(y_true, tf.Tensor):
        y_true = y_true.numpy()
    if isinstance(y_pred, tf.Tensor):
        y_pred = y_pred.numpy()

    time_axis = np.arange(len(y_true))
    if time_range is not None:
        inicio, fim = time_range
        time_axis = time_axis[inicio:fim]
        y_true = y_true[inicio:fim]
        y_pred = y_pred[inicio:fim]

    plt.figure(figsize=figsize)
    plt.plot(time_axis, y_true, label="Real", linestyle="-", marker="o", color="blue", alpha=0.7)
    plt.plot(time_axis, y_pred, label="Previsto", linestyle="--", marker="s", color="red", alpha=0.7)
    
    plt.xlabel("Tempo")
    plt.ylabel("Valor da Série")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
