# caMouse - Hand gestures recognition model for remote mouse controlling

![caMouse](icon.png)

## Authors
* Erik Terres
* Lander San Millán

## Launch the app
Locate at the base folder of the project and execute:
```
pip install -r requirements.txt
python src/DataCheckApp.py
```

## Model training
The hand gesture recognition model makes use of the 'hand_dataset.csv' located on the folder data, if you want to re-train the model, delete all the rows of the file excepting the first. The model can be easily trained by selecting a gesture on the app and using the 'Capture' button for saving the actual instance of the hand labeled.

## Available gestures
* Left & Right Click
* Mouse Move
* Scroll Up & Down
* Zoom In & Out
* Change Window