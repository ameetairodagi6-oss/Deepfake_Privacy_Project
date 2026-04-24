import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torchvision.utils as vutils

def poison_image():
    print("Loading AI Model...")
    # 1. Load a pre-trained AI (ResNet18) - This represents the "Deepfake" AI
    model = models.resnet18(weights='DEFAULT')
    model.eval() 

    print("Loading Test Image...")
    # 2. Load your image
    try:
        img = Image.open("test_image.jpg").convert('RGB')
    except FileNotFoundError:
        print("ERROR: Could not find 'test_image.jpg'. Make sure it is in the same folder!")
        return

    # Resize and convert to a mathematical tensor
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    img_tensor = transform(img).unsqueeze(0)
    img_tensor.requires_grad = True # Tracks vulnerabilities

    print("Calculating Poison (Adversarial Noise)...")
    # 3. Ask the AI what it thinks the image is
    output = model(img_tensor)
    target_label = torch.tensor([output.argmax()]) 
    
    # 4. Calculate how to confuse the AI
    loss = torch.nn.functional.cross_entropy(output, target_label)
    model.zero_grad()
    loss.backward() 
    
    # 5. Apply the FGSM Attack (The Poison)
    epsilon = 0.05
     # Strength of the poison
    noise = epsilon * img_tensor.grad.sign()
    poisoned_image_tensor = img_tensor + noise
    
    # Keep the pixel values valid
    poisoned_image_tensor = torch.clamp(poisoned_image_tensor, 0, 1)

    print("Saving Poisoned Image...")
    # 6. Save the new, protected image
    vutils.save_image(poisoned_image_tensor, "POISONED_image.jpg")
    print("SUCCESS! Check your folder for 'POISONED_image.jpg'.")

if __name__ == "__main__":
    poison_image()