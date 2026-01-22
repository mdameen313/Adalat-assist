# **Adalat Assist: AI Legal Advisory Chatbot**

## **Overview**
Adalat Assist is an intelligent legal advisory chatbot designed to provide educational legal information using AI. Built with FastAPI backend and React frontend, it leverages Google's Gemini 2.5 Flash model to answer legal queries based on a knowledge base of 140+ Indian laws.

## **✨ Features**
- 🤖 AI-powered legal question answering using Gemini 2.5 Flash
- 📚 Knowledge base of 140+ Indian laws with semantic search (FAISS)
- 💬 Interactive chat interface with conversation history
- ⚡ FastAPI backend with Uvicorn server
- 🎨 Clean React frontend with responsive design
- 🔍 Context-aware legal information retrieval
- 📝 Disclaimer system for educational purposes

## **🛠️ Tech Stack**
**Backend:**
- FastAPI + Python 3.9+
- Uvicorn ASGI server
- Google Gemini API (2.5 Flash)
- FAISS vector database
- HuggingFace sentence transformers

**Frontend:**
- React 18+
- Vite build tool
- CSS3 with responsive design
- Fetch API for communication

## **🚀 Installation & Setup**

### **Prerequisites**
- Python 3.9+
- Node.js 16+
- Google Gemini API key

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/adalat-assist.git
cd adalat-assist
```

### **2. Backend Setup**
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Frontend Setup**
```bash
# Open new terminal
cd frontend
npm install
npm run dev
```

## **📁 Project Structure**
```
adalat-assist/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── retriver.py          # FAISS retriever logic
│   ├── kb_builder.py        # Knowledge base builder
│   ├── kb.jsonl            # 140+ laws database
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   ├── api.js          # Backend API calls
│   │   └── styles.css
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

## **🔧 API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Process legal queries |
| GET | `/api/health` | Server health check |
| GET | `/api/laws/count` | Get laws count in KB |

**Chat Request:**
```json
{
  "message": "What are my rights as a tenant?",
  "conversation_history": []
}
```

## **⚙️ Configuration**
1. **Backend**: Set `GEMINI_API_KEY` in `.env` file
2. **Frontend**: Update API URL in `src/api.js` if needed
3. **Knowledge Base**: Add laws to `kb.jsonl` in JSONL format

## **📊 Knowledge Base**
- **Format**: JSON Lines (`.jsonl`)
- **Size**: 140+ Indian laws
- **Fields**: Law name, category, sections, description
- **Indexing**: Automatically vectorized with FAISS

## **⚠️ Important Disclaimer**
**FOR EDUCATIONAL PURPOSES ONLY**
- This chatbot provides general legal information, not professional advice
- Always consult a qualified lawyer for legal matters
- Responses are based on pre-loaded knowledge base
- Accuracy depends on training data quality

## **🤝 Contributing**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## **📄 License**
Distributed under MIT License. See `LICENSE` for more information.

## **🙏 Acknowledgments**
- Google Gemini API for AI capabilities
- FastAPI and React communities
- Indian legal databases for reference material


---

**Note**: This project is for educational purposes. Always verify legal information with certified professionals.
