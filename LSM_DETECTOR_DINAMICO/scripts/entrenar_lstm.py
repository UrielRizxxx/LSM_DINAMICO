import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

data = []
labels = []
label_dict = {}

carpeta_data = "data"
clases = os.listdir(carpeta_data)

for i, clase in enumerate(clases):
    archivos = os.listdir(os.path.join(carpeta_data, clase))
    label_dict[i] = clase
    for archivo in archivos:
        secuencia = np.load(os.path.join(carpeta_data, clase, archivo))
        data.append(secuencia)
        labels.append(i)

X = np.array(data)
y = to_categorical(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(LSTM(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(label_dict), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=30, batch_size=16, validation_data=(X_test, y_test))

model.save("models/modelo_lsm_lstm.keras")
np.save("models/labels_lstm.npy", label_dict)
