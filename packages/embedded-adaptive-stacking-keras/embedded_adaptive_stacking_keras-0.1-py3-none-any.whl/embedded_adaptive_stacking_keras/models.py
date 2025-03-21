import tensorflow as tf
from tensorflow.keras import layers, Model

class SlidingWindowEmbedding(Model):
    """Cria embeddings a partir de janelas deslizantes usando múltiplas camadas LSTM."""
    def __init__(self, input_dim, hidden_dims, embedding_dim):
        super(SlidingWindowEmbedding, self).__init__()
        self.lstm_layers = [layers.LSTM(h, return_sequences=True) for h in hidden_dims[:-1]]
        self.lstm_layers.append(layers.LSTM(hidden_dims[-1], return_sequences=False))
        self.dense = layers.Dense(embedding_dim, activation="relu")

    def call(self, inputs):
        x = inputs
        for lstm in self.lstm_layers:
            x = lstm(x)
        return self.dense(x)

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
        super(StackingModel, self).__init__()
        self.threshold_alpha_layer = ThresholdAlphaLayer()
        self.gru = SlidingWindowEmbedding(input_dim, hidden_dims, embedding_dim)
        self.lstm = SlidingWindowEmbedding(input_dim, hidden_dims, embedding_dim)
        self.bi_gru = SlidingWindowEmbedding(input_dim, hidden_dims, embedding_dim)
        self.meta_layer1 = layers.Dense(128, activation="relu")
        self.meta_layer2 = layers.Dense(64, activation="relu")
        self.meta_layer_output = layers.Dense(output_dim, activation="sigmoid")

    def call(self, inputs):
        out1 = self.gru(inputs)
        out2 = self.lstm(inputs)
        out3 = self.bi_gru(inputs)
        combined_out = tf.concat([out1, out2, out3], axis=-1)
        x = self.meta_layer1(combined_out)
        x = self.meta_layer2(x)
        return self.meta_layer_output(x), self.threshold_alpha_layer()
