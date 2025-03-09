# SuperWiser - Your AI Research Supervisor Assistant

![SuperWiser](imgs/emily.png)

## Introduction
**SuperWiser** is an AI-powered assistant designed to help you find the best research supervisor for your academic journey. By analyzing your research interests, CV, and preferences, it recommends suitable faculty members, refines your CV, and drafts a professional introduction email.

## 🚀 How to Run

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
You can start SuperWiser using the following command:

```bash
python superwiser_demo.py
```

## ✨ Features
✅ **AI-powered chatbot** for an interactive and seamless user experience  
✅ **Personalized supervisor recommendations** based on research alignment  
✅ **CV refinement** to match supervisor expectations  
✅ **Professional email drafting** for effective first contact  
✅ **Ensures CV accuracy**, avoiding misleading or irrelevant information  

## 🔍 How It Works
SuperWiser leverages cutting-edge AI to streamline the research supervisor search process:

1. **User Input**: You provide details such as:
   - Research interests & supervision preferences
   - CV draft path

2. **AI Analysis & Matching**:
   - SuperWiser analyzes your input using a **GPT embedder** and retrieves the most relevant supervisor.
   - The system uses **Qdrant** to store and efficiently match faculty members based on research similarity.

3. **Personalized Output**:
   - An explanation of the matching process is provided.
   - Your CV is enhanced based on the chosen supervisor’s research focus.
   - A professional introduction email is drafted.

4. **Iteration & Refinement**:
   - Not satisfied? Adjust your input, and SuperWiser will refine recommendations accordingly.

## 📚 Data Source
SuperWiser’s supervisor database is built using publicly available data from **Technion’s DDS, CS, and ECE department websites**. Each supervisor profile includes:
- **Recent research papers (up to 20 titles & abstracts)** retrieved via **Semantic Scholar API**.
- **Stored in Qdrant**, utilizing **GPT embeddings** for optimized similarity-based matching.

## 📂 Examples
Explore the `examples/` folder, where you’ll find four sample input-output cases, each in a dedicated Jupyter Notebook.

---
✨ **SuperWiser: Your AI-powered guide to academic success!** ✨