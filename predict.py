from tensorflow import keras as ks
import numpy as np

class_indices = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 
                'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 
                'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'del': 36, 'nothing': 37, 'space': 38}

datamap = dict()

for index in class_indices:
    datamap[class_indices[index]] = index

model = ks.models.load_model("Models/cnnModel1.h5")
model_asze = ks.models.load_model("Models/cnnModel_asze.h5")
model_ghu = ks.models.load_model("Models/cnnModel_ghu.h5")
model_jy = ks.models.load_model("Models/cnnModel_jy.h5")
model_ltx = ks.models.load_model("Models/cnnModel_ltx.h5")
model_mnb = ks.models.load_model("Models/cnnModel_mnb.h5")
model_vkwf = ks.models.load_model("Models/cnnModel_vkwf.h5")

def predict(sign):
    image = ks.preprocessing.image.img_to_array(sign)
    image = np.expand_dims(image,axis=0)
    
    result = model.predict(image)
    prediction = result[0].argsort()[::-1][:39]

    char = datamap[prediction[0]]

    if char == 'G' or char == 'H' or char == 'U':
        result_ghu = model_ghu.predict(image)
        prediction_ghu = result_ghu[0].argsort()[::-1][:3]

        if prediction_ghu[0] == 0:
            char = 'G'
        elif prediction_ghu[0] == 1:
            char = 'H'
        else:
            char = 'U'

    if char == 'J' or char == 'Y':
        result_jy = model_jy.predict(image)
        prediction_jy = result_jy[0].argsort()[::-1][:2]

        if prediction_jy[0] == 0:
            char = 'J'
        else:
            char = 'Y'

    if char == 'L' or char == 'T' or char == 'X':
        result_ltx = model_ltx.predict(image)
        prediction_ltx = result_ltx[0].argsort()[::-1][:3]

        if prediction_ltx[0] == 0:
            char = 'L'
        elif prediction_ltx[0] == 1:
            char = 'T'
        else:
            char = 'X'

    if char == 'B' or char == 'M' or char == 'N':
        result_mnb = model_mnb.predict(image)
        prediction_mnb = result_mnb[0].argsort()[::-1][:3]

        if prediction_mnb[0] == 0:
            char = 'B'
        elif prediction_mnb[0] == 1:
            char = 'M'
        else:
            char = 'N'

    return char

