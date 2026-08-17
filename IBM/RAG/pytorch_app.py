#==>this application will predicts the class of the image using ResNet18 model trained on ImageNet dataset

import torch
from torchvision.models import resnet18
from torchvision import transforms
import requests

# Load ResNet18 using modern torchvision API (compatible with torch 2.13.0)
model = resnet18(pretrained=True).eval()

# Download human-readable labels for ImageNet
response = requests.get("https://git.io/JJkYN")
labels = [l.strip() for l in response.text.split("\n") if l.strip()]

# Define image preprocessing (IMPORTANT for ResNet)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],#mean
        [0.229, 0.224, 0.225]#std deviation
    )
])

def predict(inp):
    # preprocess image
    inp = transform(inp).unsqueeze(0)

    # ensure model runs in inference mode
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)

    # map predictions to labels
    confidences = {}
    for i in range(len(labels)):
        confidences[labels[i]] = float(prediction[i])
    return confidences
#Using the gradio interface for web 
import gradio as gr

test_app=gr.Interface(fn=predict,
       inputs=gr.Image(type="pil"),#pil is the inp's image object
       outputs=gr.Label(num_top_classes=3),
       examples=["/content/lion.jpg", "/content/cheetah.jpg"])

test_app.launch()