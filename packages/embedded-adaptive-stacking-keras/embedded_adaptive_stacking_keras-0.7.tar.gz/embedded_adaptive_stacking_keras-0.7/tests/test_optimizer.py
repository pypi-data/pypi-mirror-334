import tensorflow as tf
from embedded_adaptive_stacking_keras.optimizer import LORO

# Criando um modelo simples
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])

# Criando o otimizador LORO
optimizer = LORO(learning_rate=0.001)

# Gerando dados aleatórios
x = tf.random.normal((32, 10))
y = tf.random.normal((32, 1))

# Testando uma iteração de treinamento
with tf.GradientTape() as tape:
    predictions = model(x)
    loss = tf.reduce_mean(tf.square(predictions - y))

gradients = tape.gradient(loss, model.trainable_variables)
optimizer.apply_gradients(zip(gradients, model.trainable_variables))

print("Otimização realizada com sucesso!")
