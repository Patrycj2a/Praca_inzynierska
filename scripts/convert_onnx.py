import torch

weights = r"yolov5\runs\train\exp6\weights\best.pt"

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)
#print(model)

# Create a dummy input tensor matching the input shape of the model
dummy_input = torch.randn(1, 3, 640, 640)
# Convert and save as ONNX
torch.onnx.export(model, dummy_input, 'output.onnx')
