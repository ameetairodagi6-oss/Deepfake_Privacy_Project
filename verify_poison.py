import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import urllib.request
import json

def test_ai_vision():
    # 1. Load the AI
    model = models.resnet18(weights='DEFAULT')
    model.eval()

    # 2. Download the official "Dictionary" the AI uses to name things
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    response = urllib.request.urlopen(url)
    labels = json.loads(response.read())

    # 3. Setup the image processor
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    def ask_ai(image_path):
        try:
            img = Image.open(image_path).convert('RGB')
            tensor = transform(img).unsqueeze(0)
            output = model(tensor)
            best_guess_index = output.argmax().item()
            return labels[best_guess_index]
        except Exception as e:
            return "File not found!"

    # 4. The Grand Reveal
    print("\n--- AI VISION TEST ---")
    
    original_guess = ask_ai("test_image.jpg")
    print(f"AI looks at Original Image: I see a '{original_guess}'")
    
    poisoned_guess = ask_ai("POISONED_image.jpg")
    print(f"AI looks at Poisoned Image: I see a '{poisoned_guess}'")
    
    print("----------------------\n")

if __name__ == "__main__":
    test_ai_vision()