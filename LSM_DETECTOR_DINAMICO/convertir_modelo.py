import tensorflowjs as tfjs
from tensorflow import keras

# Cargar el modelo .keras entrenado
modelo = keras.models.load_model('models/modelo_lsm_lstm.keras')

# Convertir y guardar en formato web
tfjs.converters.save_keras_model(modelo, 'LSM_DETECTOR_WEB/model')

print("✅ Conversión completada y guardada en LSM_DETECTOR_WEB/model/")
