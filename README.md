# Silent Talk

### Real time application for translating American Sign Language into English text, delivering seamless communication accessibility.

## Project Features

- Real time app that converts American sign language to English text.
- Custom VGG-16 model was created using Tensorflow (an open source Python library for AI and ML).
- The model was trained on the [Kaggle dataset](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) that had over 90k images (including upper case alphabets, numbers and special signs for 'space' and 'delete').
- To increase the accuracy, several models were created and trained. (All characters may be predicted by the main model, but a different and unique model was also trained for each group, such as "GHU," "JY," "LTX," and "BMN," because these certain groups of characters had similar signs).
- The model has the accuracy of around 93%.
- The user interface of the app was created using Tkinter (Python GUI library) and OpenCV (computer vision library).
- The app also has the feature to convert text into speech.

## Technology Used

- Python
- TensorFlow
- VGG‑16
- Tkinter
- OpenCV

## Project Demo

https://github.com/user-attachments/assets/8d2ab200-aef9-446f-b097-0bc91baf7279
