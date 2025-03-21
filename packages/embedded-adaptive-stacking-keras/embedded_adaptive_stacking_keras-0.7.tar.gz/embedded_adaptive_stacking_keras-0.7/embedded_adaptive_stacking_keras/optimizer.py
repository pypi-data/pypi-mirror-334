import tensorflow as tf

class LORO(tf.keras.optimizers.legacy.Optimizer):
    """
    Loss-Oriented Rate Optimizer (LORO)
    Um otimizador que ajusta dinamicamente a taxa de aprendizado com base na variação da perda.
    """

    def __init__(self, learning_rate=0.001, adapt_factor=0.1, gamma=1.0, name="LORO", **kwargs):
        # Chamando a inicialização da classe base corretamente
        super().__init__(name, **kwargs)

        # Garantindo que a learning rate seja um float ou LearningRateSchedule
        if not isinstance(learning_rate, (float, int, tf.keras.optimizers.schedules.LearningRateSchedule)):
            raise ValueError(
                f"Argument `learning_rate` should be a float or a LearningRateSchedule, but got {type(learning_rate)}"
            )

        # Definindo a learning rate corretamente
        self._set_hyper("learning_rate", learning_rate)

        # Variáveis do LORO
        self.adapt_factor = tf.Variable(adapt_factor, dtype=tf.float32, trainable=False)
        self.gamma = tf.Variable(gamma, dtype=tf.float32, trainable=False)
        self.prev_loss = tf.Variable(1.0, dtype=tf.float32, trainable=False)

    def _resource_apply_dense(self, grad, var, apply_state=None):
        # Obtendo a taxa de aprendizado
        lr = self._get_hyper("learning_rate")
        loss = tf.reduce_mean(tf.abs(grad))

        # Ajuste dinâmico da taxa de aprendizado
        delta_loss = loss - self.prev_loss
        adjusted_lr = lr * (1 + self.adapt_factor * tf.tanh(delta_loss))

        # Ajustando os pesos
        factor = 1 + self.gamma * (loss / (self.prev_loss + 1e-8))
        var.assign_sub(adjusted_lr * factor * grad)

        # Atualizando a perda anterior
        self.prev_loss.assign(loss)

    def get_config(self):
        base_config = super().get_config()
        return {
            **base_config,
            "learning_rate": self._serialize_hyperparameter("learning_rate"),
            "adapt_factor": float(self.adapt_factor.numpy()),
            "gamma": float(self.gamma.numpy()),
        }
