# 🤖 RoleFlow Chat: The Smart RBAC RAG Chatbot That Actually Gets You! 

*Because waiting for department approvals is SO last decade* 💸

Ever tried getting data from another department and felt like you were negotiating a peace treaty? 🕊️ **RoleFlow Chat** is here to end the corporate data wars! This isn't just another chatbot – it's your personal AI assistant that knows exactly what you're allowed to see and serves it up faster than your morning coffee ☕

## 🎯 The Problem

Picture this: You need sales data for your quarterly report, but Steve from Sales is on vacation 🏖️, Karen from Finance is in meetings all day 📅, and IT says "have you tried turning it off and on again?" 🔄

**RoleFlow Chat says:** "Hold my algorithms" 🤖✨

RoleFlow Chat is a secure, role-based chatbot that cuts through organizational red tape like a hot knife through butter. No more email chains, no more "quick sync meetings," just instant, accurate, department-specific answers!

## 🔥 Why RBAC RAG

Traditional RAG systems are like that friend who overshares – they'll tell you EVERYTHING, even stuff you shouldn't know! 🤐

But RBAC RAG is more like your wise, security-conscious colleague who:
- 🛡️ Only shows you what you're supposed to see
- 🎯 Keeps sensitive info locked down tighter than Fort Knox
- 🧠 Still gives you brilliant, contextual answers
- 🚪 Makes sure the right people get through the right doors

## ✨ Features That'll Make You Go "WOW!"

🎪 **Role-Based Access Control**: Like having a digital bouncer who actually knows you  
🗣️ **Natural Language Processing**: Talk to it like a human, not a search engine  
🧩 **Contextually Rich Responses**: Answers so good, you'll think it read your mind  
🔐 **JWT Authentication**: Security so tight, even your password manager is impressed  
💬 **Interactive Chat Interface**: Features a smooth and intuitive UI designed for effortless interaction

## 🛠️ Tech Stack That Doesn't Mess Around

Didn't just pick cool-sounding technologies – assembled one of the best AI tools:

<div align="center">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="50" height="50"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" width="50" height="50"/>
<img src="./Images/chromadb icon.png" width="50" height="50"/>  
<img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" width="50" height="50"/>
<img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="50" height="50"/>
<img src="https://python.langchain.com/img/brand/wordmark.png" width="80" height="50"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/json/json-original.svg" width="50" height="50"/>
<img src="./Images/openrouter icon.png" width="50" height="50"/>    
</div>

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="20" height="20"/> **Python**: Because life's too short for JavaScript (just kidding, JS fans!)

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" width="20" height="20"/> **FastAPI**: Lightning-fast backend that makes Usain Bolt jealous

<img src="./Images/chromadb icon.png" width="20" height="20"/> **ChromaDB**: Vector magic that finds needles in haystacks

<img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" width="20" height="20"/> **HuggingFace Embeddings**: The secret sauce for understanding your docs

<img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="20" height="20"/> **Streamlit**: Making beautiful UIs since developers stopped crying about frontend

<img src="https://python.langchain.com/img/brand/wordmark.png" width="40" height="20"/> **LangChain**: The Swiss Army knife of language models

<img src="./Images/openrouter icon.png" width="20" height="20"/>  **OpenRouter**: Your gateway to AI model paradise

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/json/json-original.svg" width="20" height="20"/> **JWT**: Digital passports that actually work

## 🚀 Get This Bad Boy Running

### What You'll Need
- Python 3.11 (the cool kid on the block)
- pip (your package-installing sidekick)

### Let's Do This! 🎯

**1. Grab the Code:**
```bash
git clone <your-repo-url>
cd roleflow-chat
```

**2. Install the Magic:**
```bash
pip install -r requirements.txt
```

**3. Set Your Secrets** (shh! 🤫):
Create a `.env` file and add:
```bash
JWT_SECRET_KEY=your_super_secret_key_that_nobody_can_guess
OPENROUTER_API_KEY=your_openrouter_api_key
```

**4. Point to Your Data:**
Update `document_loader.py` with your document paths (make it point to the good stuff!)

**5. Launch Time!** 🚀
```bash
# Terminal 1 - Fire up the backend
uvicorn main:app --host 0.0.0.0 --port 8000  

# Terminal 2 - Launch the UI
streamlit run app.py
```

## 🎮 How to Be a RoleFlow Chat Pro

1. **🔑 Login Like a Boss**: Hit the sidebar, enter your name and department
2. **💬 Ask Away**: Type your questions like you're texting a friend
3. **📚 Check the Receipts**: See exactly where your answers came from
4. **📁 Export Everything**: Save your chat history because knowledge is power!

## 🙏 Props Where Props Are Due

Massive shoutout to [CodeBasics](https://codebasics.io/challenges/resume-project-challenge) for the challenge that sparked this digital revolution! 🔥

## 🌟 Want to Join the Revolution?

Love what you see? **STAR would be appreciated** ⭐ 

Ready to contribute? I am always looking for fellow code warriors:
1. Fork this bad boy 🍴
2. Make it even more awesome 💪
3. Submit a pull request 📬
4. Become part of the legend 🏆

---

*Built with ❤️ and just the right amount of controlled chaos* 🎭

---

## 📸 Gallery

<div align="center">

### 🔐 **Authentication & Access Control**
<img src="./Images/Login%20Screen.png" width="500" alt="Secure Login Interface"/>

*Role-based authentication ensures users only access their authorized data*

---

### 💬 **Department-Specific Chat Interfaces**

| General Department | Finance Department | C-Level Executive |
|:---:|:---:|:---:|
| <img src="./Images/RBAC%20CHT%20interface%20for%20general.png" width="280" alt="General Department Chat Interface"/> | <img src="./Images/RBAC%20CHT%20interface%20for%20finance.png" width="280" alt="Finance Department Chat Interface"/> | <img src="./Images/RBAC%20CHT%20interface%20for%20c-level%20(example).png" width="280" alt="C-Level Executive Chat Interface"/> |
| **General Access** | **Finance Access** | **Executive Access** |
| Standard queries & responses | Financial data & insights | Strategic & comprehensive view |

---

### 🎯 **Smart Role-Based Responses**

<details>
<summary><strong>🏢 C-Level Executive Responses</strong> (Click to expand)</summary>
<br>
<img src="./Images/RoleFlow%20Response%20for%20C-level.png" width="600" alt="C-Level Executive Response"/>
<br><br>
<em>Comprehensive, strategic insights with cross-departmental data access</em>
</details>

<details>
<summary><strong>⚙️ Engineering Department Responses</strong> (Click to expand)</summary>
<br>

| Technical Query Response | Detailed Engineering Data |
|:---:|:---:|
| <img src="./Images/RoleFlow%20Response%20for%20eng%20dept%20-1.png" width="400" alt="Engineering Response 1"/> | <img src="./Images/RoleFlow%20Response%20for%20eng%20dept%20-2.png" width="400" alt="Engineering Response 2"/> |
| **Quick Technical Answers** | **In-Depth Engineering Insights** |

<em>Role-specific technical information tailored for engineering teams</em>
</details>

---

### 🚀 **Key Features Demonstrated**
- ✅ **Secure Authentication** - Role verification before access
- ✅ **Department-Specific UI** - Tailored interfaces for different roles  
- ✅ **Contextual Responses** - Answers filtered by user permissions
- ✅ **Scalable Architecture** - Supports multiple departments seamlessly

</div>
