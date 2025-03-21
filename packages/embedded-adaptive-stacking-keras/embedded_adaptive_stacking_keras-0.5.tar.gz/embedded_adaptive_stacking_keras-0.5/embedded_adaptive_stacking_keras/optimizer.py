import tensorflow as tf

class LORO(tf.keras.optimizers.Optimizer):
    """
    Loss-Oriented Rate Optimizer (LORO)
    Otimizador que ajusta a taxa de aprendizado com base na função de custo.
    """
    def __init__(self, learning_rate=0.001, adapt_factor=0.1, gamma=1.0, name="LORO", **kwargs):
        super().__init__(name, **kwargs)
        
        # Definir a taxa de aprendizado corretamente no TensorFlow 2.x
        self._set_hyper("learning_rate", learning_rate)  
        self.adapt_factor = adapt_factor
        self.gamma = gamma
        self.prev_loss = tf.Variable(1.0, dtype=tf.float32, trainable=False)  # Valor inicial da perda

    def _resource_apply_dense(self, grad, var, apply_state=None):
        lr = self._get_hyper("learning_rate")  # Pegando a taxa de aprendizado correta
        loss = tf.reduce_mean(tf.abs(grad))

        # Ajustando a taxa de aprendizado dinamicamente
        delta_loss = loss - self.prev_loss
        adjusted_lr = lr * (1 + self.adapt_factor * tf.tanh(delta_loss))

        # Ajuste de peso baseado na perda
        factor = 1 + self.gamma * (loss / (self.prev_loss + 1e-8))
        var.assign_sub(adjusted_lr * factor * grad)

        # Atualiza a perda anterior
        self.prev_loss.assign(loss)

    def get_config(self):
        config = super().get_config()
        config.update({
            "learning_rate": self._serialize_hyperparameter("learning_rate"),
            "adapt_factor": self.adapt_factor,
            "gamma": self.gamma,
        })
        return config
