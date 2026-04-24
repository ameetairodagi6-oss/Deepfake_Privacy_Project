# 🛡️ Shield.AI: Deepfake Data Poisoning for Personal Privacy

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Adversarial%20ML-EE4C2C)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)
![Google AI](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-F9AB00)

**A proactive cybersecurity tool built for the Hack2Skill Build with AI Hackathon (2026).**

## 🛑 The Problem
With the rapid advancement of generative AI, malicious actors can scrape unconsented personal images from social media to train deepfake models. Everyday internet users currently lack accessible tools to protect their digital identity and biometric data from being harvested. 

## 💡 The Solution
Shield.AI acts as a "Digital Bodyguard." It is a full-stack web application that allows users to upload their personal photos and inject them with invisible adversarial data poisoning. 

By applying mathematical noise (via PyTorch) that is completely imperceptible to the human eye, the image becomes "radioactive" to AI. If a scraper attempts to use the protected image for facial recognition or deepfake generation, the adversarial noise forces the model to misclassify the data, rendering it useless to the attacker.

## ⚙️ How It Works (Tech Stack)
* **Backend:** Python & Flask handle the secure file routing and local server environment.
* **Adversarial Engine:** PyTorch uses a pre-trained ResNet18 model to calculate the gradient of the image and apply a Fast Gradient Sign Method (FGSM) attack with an imperceptible epsilon value (`0.05`).
* **AI Verification:** Google's **Gemini 2.5 Flash API** dynamically generates a contextual "Data Privacy Certificate" confirming the cryptographic protection of the asset.
* **Frontend:** Custom HTML/CSS with a dark-mode cybersecurity aesthetic for a seamless user experience.

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/shield-ai.git](https://github.com/your-username/shield-ai.git)
   cd shield-ai