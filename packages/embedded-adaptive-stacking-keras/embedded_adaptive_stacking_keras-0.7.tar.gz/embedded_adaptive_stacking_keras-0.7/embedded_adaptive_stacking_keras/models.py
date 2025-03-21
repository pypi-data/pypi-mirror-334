import tensorflow as tf
from tensorflow.keras import layers, Model

class SlidingWindowEmbedding(Model):
    """Cria embeddings a partir de janelas deslizantes usando múltiplas camadas LSTM."""
    def __init__(self, input_dim, hidden_dims, embedding_dim):
        """
        :param input_dim: Dimensão de entrada
        :param hidden_dims: Lista com os tamanhos das camadas ocultas
        :param embedding_dim: Dimensão do embedding final
        """
        super(SlidingWindowEmbedding, self).__init__()
        self.lstm_layers = [layers.LSTM(h, return_sequences=True) for h in hidden_dims[:-1]]
        self.lstm_layers.append(layers.LSTM(hidden_dims[-1], return_sequences=False))

        # Camada densa com LeakyReLU
        self.dense = layers.Dense(embedding_dim)
        self.leaky_relu = layers.LeakyReLU(alpha=0.01)  # Substituindo ReLU por LeakyReLU

    def call(self, inputs):
        x = inputs
        for lstm in self.lstm_layers:
            x = lstm(x)
        x = self.dense(x)
        return self.leaky_relu(x)  # Aplicando LeakyReLU na saída


class ThresholdAlphaLayer(Model):
    """Camada regressiva treinável para threshold e alpha."""
    def __init__(self):
        super(ThresholdAlphaLayer, self).__init__()
        self.threshold = tf.Variable(0.7, trainable=True, dtype=tf.float32)
        self.alpha = tf.Variable(2.0, trainable=True, dtype=tf.float32)

    def call(self):
        return tf.nn.softplus(self.threshold), tf.nn.softplus(self.alpha)


class StackingModel(Model):
    """Modelo de stacking adaptativo com aprendizado de parâmetros dinâmicos e múltiplas camadas ocultas."""
    def __init__(self, input_dim, hidden_dims, embedding_dim, output_dim):
        """
        :param input_dim: Dimensão de entrada
        :param hidden_dims: Lista de dimensões ocultas para cada modelo base
        :param embedding_dim: Dimensão do embedding final
        :param output_dim: Número de saídas
        """
        super(StackingModel, self).__init__()
        self.threshold_alpha_layer = ThresholdAlphaLayer()

        # Criando os 4 modelos base SEPARADAMENTE no stacking
        self.gru = layers.GRU(hidden_dims[-1], return_sequences=False)
        self.lstm = layers.LSTM(hidden_dims[-1], return_sequences=False)
        self.bi_gru = layers.Bidirectional(layers.GRU(hidden_dims[-1], return_sequences=False))
        self.bi_lstm = layers.Bidirectional(layers.LSTM(hidden_dims[-1], return_sequences=False))

        # Camadas do meta-modelo (agora com LeakyReLU)
        self.meta_layer1 = layers.Dense(128)
        self.leaky_relu1 = layers.LeakyReLU(alpha=0.01)
        self.meta_layer2 = layers.Dense(64)
        self.leaky_relu2 = layers.LeakyReLU(alpha=0.01)
        self.meta_layer_output = layers.Dense(output_dim, activation="sigmoid")

    def call(self, inputs):
        out1 = self.gru(inputs)
        out2 = self.lstm(inputs)
        out3 = self.bi_gru(inputs)
        out4 = self.bi_lstm(inputs)

        # Concatenando todas as saídas dos modelos de Stacking
        combined_out = tf.concat([out1, out2, out3, out4], axis=-1)

        # Passando pelo meta-modelo com LeakyReLU
        x = self.meta_layer1(combined_out)
        x = self.leaky_relu1(x)
        x = self.meta_layer2(x)
        x = self.leaky_relu2(x)

        return self.meta_layer_output(x), self.threshold_alpha_layer()
