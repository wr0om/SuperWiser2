<!-- # TODO
1. Fix README.md
2. Add requirements.txt
3. Add 3 examples of input+output to the examples folder -->
# SuperWiser - Your AI Research Supervisor Assistant  

![SuperWiser](imgs/emily.png)  

## Introduction  
**SuperWiser** is an AI-powered assistant designed to help you find the best research supervisor for your academic journey. By analyzing your research interests, CV, and preferences, it recommends suitable faculty members, refines your CV, and drafts a professional introduction email.  

## How to Run  

### 1. Install Dependencies  
Ensure you have **Python 3.11** installed. Then, install the required libraries:  
```bash  
pip install -r requirements.txt  
```

### 2. Set Up API Keys  
Create a `.env` file in the root directory and add your API credentials:  
```bash  
API_KEY=YOUR_OPENAI_API_KEY  
QDRANT_API_KEY=YOUR_QDRANT_API_KEY  
```

### 3. Run the Application  
You can run SuperWiser using the following:  

- **Python script**:  
  ```bash  
  python superwiser_demo.py  
  ```  

## Features  
✅ **Interactive AI chatbot** for seamless user experience  
✅ **Supervisor recommendations** based on research alignment  
✅ **CV enhancement** to match supervisor expectations  
✅ **Professional email drafting** for first contact  
✅ **Ensures CV accuracy**, avoiding misleading information  

## How It Works  
SuperWiser leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques, integrating:  
- **GPT-4o** for text generation  
- **Qdrant** for similarity-based supervisor matching  

The process:  
1. You provide your research interests, supervision preferences, and a CV draft.  
2. SuperWiser analyzes your inputs and suggests **suitable research supervisors**.  
3. It refines your CV and generates a **tailored email draft**.  
4. If needed, you can request additional recommendations with refined preferences.  

## Data Source  
SuperWiser’s supervisor database is built from **Technion’s DDS, CS, and ECE department websites**.  
- For each supervisor, the **20 most recent research papers** (title & abstract) are retrieved via **Semantic Scholar API**.  
- Data is stored in **Qdrant**, with **GPT embeddings** used for efficient retrieval in the recommendation process.  

## Examples
In the `examples/` folder, you can find three examples of inputs and outputs, each in its own python notebook.