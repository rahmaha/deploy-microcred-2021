# -*- coding: utf-8 -*-
"""beras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tvQMVa1pxniMsQNBCY6qpyuXE-Ln0VWI
"""



"""Kelompok 06

Anggota kelompok:

1. Ahmad Azrial Nubail
2. Priskila Destriani Banjarnahor
3. Rahma Hayuning Astuti

Kelas : UGM-04

Universitas Host : Universitas Gadjah Mada
"""

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# import library for build model 
from keras.layers import Dense,Dropout,SimpleRNN,LSTM
from keras.models import Sequential

# import library untuk data preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from datetime import datetime

df=pd.read_csv('beras - Sheet1 (2).csv', parse_dates=['Date'], index_col=['Date'])
df

df.describe()

df.isna().sum()

df.info()

df.plot(figsize=(16, 10))
plt.legend(fontsize="large")
plt.xlabel("Date")
plt.ylabel("Harga beras (kg)");

# Kolom 'low' yang akan kita gunakan dalam membangun model
# Slice kolom 'low' 

Low_data = df.iloc[:,0:1].values

# cek output low_data
Low_data



"""###  Data Preprocessing"""

# Menskalakan data antara 1 dan 0 (scaling) pada low data

scaler = MinMaxScaler(feature_range=(0,1))

# definisikan variabel step dan train 

Low_scaled = scaler.fit_transform(Low_data)                    

step_size = 21                    

train_x = []
train_y = []

# membuat fitur dan lists label

for i in range(step_size,723):                
    train_x.append(Low_scaled[i-step_size:i,0])
    train_y.append(Low_scaled[i,0])

# mengonversi list yang telah dibuat sebelumnya ke array

train_x = np.array(train_x)                  
train_y = np.array(train_y)

# cek dimensi data dengan function .shape

print(train_x.shape)

# 202 hari terakhir akan digunakan dalam pengujian
# 500 hari pertama akan digunakan dalam pelatihan

test_x = train_x[500:]            
train_x = train_x[:500]           
test_y = train_y[500:]  
train_y = train_y[:500]

# reshape data untuk dimasukkan kedalam Keras model

train_x = np.reshape(train_x, (500, step_size, 1))           
test_x = np.reshape(test_x, (202, step_size, 1))

# cek kembali dimensi data yang telah di reshape dengan function .shape

print(train_x.shape)
print(test_x.shape)

"""Sekarang kita bisa mulai membuat model kita, dimulai dengan RNN

## Build Model - RNN
"""

# buat varibel penampung model RNN
rnn_model = Sequential()

# Output dari SimpleRNN akan menjadi bentuk tensor 2D (batch_size, 40) dengan Dropout sebesar 0.20

rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=True, input_shape=(train_x.shape[1],1)))
rnn_model.add(Dropout(0.15))

rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=True))
rnn_model.add(Dropout(0.15))

rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=False))
rnn_model.add(Dropout(0.15))

# Add a Dense layer with 1 units.
rnn_model.add(Dense(1))

# menambahkan loss function kedalam model RNN dengan tipe MSE

rnn_model.compile(optimizer="adam",loss="MSE")

# fit the model RNN, dengan epoch 20 dan batch size 25

rnn_model.fit(train_x,train_y,epochs=20,batch_size=75)

# Prediksi Model RNN
rnn_predictions = rnn_model.predict(test_x)

rnn_score = r2_score(test_y,rnn_predictions)

rnn_score



"""###  Build Model - LSTM

"""

# buat varibel penampung model LSTM
lstm_model = Sequential()

# Add a LSTM layer with 40 internal units. dengan Dropout sebesar 0.20

lstm_model.add(LSTM(40,activation="tanh",return_sequences=True, input_shape=(train_x.shape[1],1)))
lstm_model.add(Dropout(0.15))

lstm_model.add(LSTM(40,activation="tanh",return_sequences=True))
lstm_model.add(Dropout(0.15))

lstm_model.add(LSTM(40,activation="tanh",return_sequences=False))
lstm_model.add(Dropout(0.15))

# Add a Dense layer with 1 units.
lstm_model.add(Dense(1))

# menambahkan loss function kedalam model lstm dengan tipe MSE

lstm_model.compile(optimizer="adam",loss="MSE")

# fit lstm model, dengan epoch 20 dan batch size 25

lstm_model.fit(train_x,train_y,epochs=20,batch_size=75)

# Prediksi Model LSTM
lstm_predictions = lstm_model.predict(test_x)

lstm_score = r2_score(test_y,lstm_predictions)

lstm_score

"""## Evaluasi

"""

# Cetak nilai prediksi masing-masing model dengan menggunakan r^2 square

print("R^2 Score dari model RNN",rnn_score)
print("R^2 Score dari model LSTM",lstm_score)

"""### Visualisasi Perbandingan Hasil Model prediksi dengan data original"""

lstm_predictions = scaler.inverse_transform(lstm_predictions)
rnn_predictions = scaler.inverse_transform(rnn_predictions)
test_y = scaler.inverse_transform(test_y.reshape(-1,1))

plt.figure(figsize=(16,12))

plt.plot(test_y, c="blue",linewidth=2, label="original")
plt.plot(lstm_predictions, c="green",linewidth=2, label="LSTM")
plt.plot(rnn_predictions, c="red",linewidth=2, label="RNN")
plt.legend()
plt.title("PERBANDINGAN",fontsize=20)
plt.grid()
plt.show()