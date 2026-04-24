import os
from flask import Flask, render_template, request
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torchvision.utils as vutils
import google.generativeai as genai

# --- ADD YOUR API KEY HERE ---
genai.configure(api_key="PASTE_YOUR_API_KEY_HERE")

app = Flask(__name__)
os.makedirs('static', exist_ok=True)

def apply_poison(input_path, output_path):
    model = models.resnet18(weights='DEFAULT')
    model.eval()
    
    img = Image.open(input_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    img_tensor = transform(img).unsqueeze(0)
    img_tensor.requires_grad = True

    output = model(img_tensor)
    target_label = torch.tensor([output.argmax()])
    loss = torch.nn.functional.cross_entropy(output, target_label)
    model.zero_grad()
    loss.backward()
    
    # Lowered epsilon so the image looks completely normal to humans!
    epsilon = 0.05 
    noise = epsilon * img_tensor.grad.sign()
    poisoned_image_tensor = torch.clamp(img_tensor + noise, 0, 1)
    
    vutils.save_image(poisoned_image_tensor, output_path)

def generate_certificate():
    # Ask Gemini to generate a custom security badge text
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = "Write a 2-sentence official-sounding 'Data Privacy Certificate' for a user who just protected their uploaded photo using Adversarial Machine Learning to block facial recognition and deepfakes."
    response = model.generate_content(prompt)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            input_path = os.path.join('static', 'uploaded_image.jpg')
            output_path = os.path.join('static', 'protected_image.jpg')
            
            file.save(input_path)
            apply_poison(input_path, output_path)
            
            # Generate the Gemini certificate
            cert_text = generate_certificate()

            return render_template('index.html', result_image=output_path, certificate=cert_text)

    return render_template('index.html', result_image=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)