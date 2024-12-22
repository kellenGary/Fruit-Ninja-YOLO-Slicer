from ultralytics import YOLO

# Load a model
model = YOLO("fruit-ninja-model.pt")  # load a partially trained model

# Resume training
results = model.train(resume=True)