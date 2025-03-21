import tensorflow as tf
from embedded_adaptive_stacking_keras.loss import CustomLossWithRegression


def save_model(model, path="model_keras.h5"):
    """Salva o modelo treinado no formato do TensorFlow."""
    model.save(path)

def load_model(path="model_keras.h5"):
    """Carrega um modelo salvo."""
    return tf.keras.models.load_model(path, custom_objects={"CustomLossWithRegression": CustomLossWithRegression})
