# TODO
1. Fix README.md
2. Add requirements.txt
3. Add 3 examples of input+output to the examples folder

# SuperWiser - Your AI Research Supervisor Assistant

![alt text](imgs/emily.png)

## Introduction
SuperWiser is an AI research supervisor assistant that helps you to manage your research projects. It is designed to help you to keep track of your research projects, papers, and experiments. 

## How to Run
To run the application, you need to install the required libraries in a Python 3.11 environment. You can install the required libraries by running the following command:
```
pip install -r requirements.txt
```

After installing the required libraries, you also need to provide the required API keys. You can provide the API key by creating a `.env` file in the root directory of the project and adding the following lines:
```
API_KEY=YOUR_OPENAI_API_KEY
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
```

After providing the API keys, you can run the application by running the following command:
```
python superwiser_demo.py
```
or run the provided notebook `superwiser_demo.ipynb`.

## Features
* A user-friendly chatbot for seamless interaction.
* Accepts user preferences and a CV draft.
* Recommends suitable research supervisors.
* Generates a tailored email draft and polished CV.
* Ensures CV accuracy, avoiding any misleading information.

## How it Works
SuperWiser uses a combination of NLP and ML techniques to provide a seamless user experience. It uses OpenAI's GPT-4o for generating text and Qdrant for similarity search of research supervisors. You will be asked for a few preferences and a CV draft. Based on your preferences and CV, SuperWiser will recommend suitable research supervisors. It will also generate a tailored email draft and a polished CV for you. If you are dissatisfied with the recommendations, you can ask for more recommendations by providing clearer preferences.