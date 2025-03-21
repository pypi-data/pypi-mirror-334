import tensorflow as tf
from tensorflow.keras.losses import Loss

class CustomLossWithRegression(Loss):
    """Função de custo personalizada com threshold e alpha aprendíveis."""
    def __init__(self, threshold_alpha_layer):
        super(CustomLossWithRegression, self).__init__()
        self.threshold_alpha_layer = threshold_alpha_layer

    def call(self, y_true, y_pred):
        threshold, alpha = self.threshold_alpha_layer()
        diff = tf.abs(y_true - y_pred)
        intense_mask = tf.cast(y_true > threshold, tf.float32)
        return tf.reduce_mean(diff * (1 + alpha * intense_mask))
