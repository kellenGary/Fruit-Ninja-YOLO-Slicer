from ultralytics import YOLO
import os

# Load my current YOLO model for more training
model = YOLO('./fruit-ninja-model.pt')

# Input directory containing images
training_images_dir = os.path.abspath("./dataset/images/train")
training_labels_dir = os.path.abspath("./dataset/labels/train")

results = model.train(
    data='./dataset/data.yaml',
    epochs=100,
    batch=16,
    lr0=0.01,
    optimizer="SGD",
    device='mps',
    save=True,
    cache=True,
    workers=8
)

model.val()

# Save model to venv for use in Main.py
model.save('./fruit-ninja-model.pt')