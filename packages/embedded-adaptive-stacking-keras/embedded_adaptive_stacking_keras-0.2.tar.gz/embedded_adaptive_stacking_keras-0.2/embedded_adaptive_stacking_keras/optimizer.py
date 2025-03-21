import tensorflow as tf

class LORO(tf.keras.optimizers.Optimizer):
    """
    Otimizador que ajusta a taxa de aprendizado com base na função de custo.
    """
    def __init__(self, learning_rate=0.001, adapt_factor=0.1, gamma=1.0, name="LORO", **kwargs):
        super().__init__(name, **kwargs)
        self.learning_rate = tf.Variable(learning_rate, dtype=tf.float32)
        self.adapt_factor = adapt_factor
        self.gamma = gamma
        self.prev_loss = tf.Variable(1.0, dtype=tf.float32)

    def _resource_apply_dense(self, grad, var, apply_state=None):
        loss = tf.reduce_mean(tf.abs(grad))
        delta_loss = loss - self.prev_loss
        adjusted_lr = self.learning_rate * (1 + self.adapt_factor * tf.tanh(delta_loss))
        factor = 1 + self.gamma * (loss / (self.prev_loss + 1e-8))
        var.assign_sub(adjusted_lr * factor * grad)
        self.prev_loss.assign(loss)

    def get_config(self):
        return {"learning_rate": self.learning_rate.numpy(), "adapt_factor": self.adapt_factor, "gamma": self.gamma}
