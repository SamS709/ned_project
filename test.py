import keras
import os
import keras.backend as K

model = keras.models.load_model(filepath=os.getcwd()+"\Connect4\AI\models"+"\model21")
print(model.summary())
