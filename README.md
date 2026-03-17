# MarketMind - AI-Powered Sales & Marketing Intelligence

![MarketMind](https://img.shields.io/badge/Status-Production-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**MarketMind** is a production-ready AI SaaS platform that transforms sales and marketing workflows with enterprise-grade generative AI. Generate professional campaigns, sales pitches, and lead scoring insights in seconds.

---

## 🚀 Key Features

### 1. **AI Campaign Generator**
- Platform-specific marketing strategies (LinkedIn, Instagram, Email, Google Ads, Facebook)
- Data-driven campaign recommendations
- Compelling copy and actionable insights
- One-click PDF export

### 2. **Sales Pitch Intelligence**
- Persuasive, AI-powered sales messaging
- Value proposition highlighting
- Pain point addressing
- Customizable for any product/service

### 3. **Lead Scoring & Qualification**
- Automated lead scoring (0-100)
- AI-driven qualification recommendations (Hot, Warm, Lukewarm, Cold)
- Engagement signal analysis
- Prioritization for high-value opportunities

### 4. **Professional UX**
- Clean, modern SaaS interface
- Copy-to-clipboard functionality
- PDF export for all outputs
- Live character counters with input guidance
- Step-based loading progress
- Session-based output history (last 5 per module)
- Responsive design

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- Groq API (AI model: `llama-3.3-70b-versatile`)

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Font Awesome (Icons)
- Google Fonts (Inter)

**AI Features:**
- Deterministic seeding for consistent outputs
- Dual-temperature system (decision vs. creative)
- Fallback scoring with narrow variance
- Recommendation locking to score categories

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/marketmind.git
cd marketmind
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5001`

---

## 🌐 Usage

### Access the Application
1. **Landing Page:** `http://127.0.0.1:5001/`
2. **Login:** `http://127.0.0.1:5001/login.html`
   - Demo mode: Use any email/password to access
3. **Dashboard:** `http://127.0.0.1:5001/dashboard`

### Generate AI Content
1. Select a module (Marketing, Sales, or Lead Scoring)
2. Fill in the required fields
3. Click "Generate" and wait for AI processing
4. Copy or download the output as PDF

---

## 📂 Project Structure

```
marketmind/
├── app.py                      # Flask backend
├── ai_engine.py                # AI logic and API integration
├── landing.html                # Landing page
├── login.html                  # Login page
├── index.html                  # Main dashboard
├── app.js                      # Frontend logic
├── style.css                   # Main styles
├── animations.css              # UI animations
├── form-enhancements.css       # Form styling
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
└── README.md                   # This file
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI model access | Yes |

---

## 🎯 Core Functionality

### AI Consistency Features
- **Deterministic Seeding:** Same inputs = same core decisions
- **Dual Temperature:** Low (0.4) for decisions, high (0.7-0.85) for creativity
- **Score Variance:** ±3-5 points for realistic variation
- **Recommendation Locking:** Categories locked to score ranges

### User Workflow
1. **Login** → Session-based authentication
2. **Select Module** → Choose from 3 AI tools
3. **Input Data** → Fill forms with character guidance
4. **Generate** → AI processes with step-based progress
5. **Review** → View formatted output
6. **Export** → Copy or download as PDF

---

## 🚀 Deployment

### Production Checklist
- ✅ Set `GROQ_API_KEY` in environment
- ✅ Use production WSGI server (e.g., Gunicorn)
- ✅ Enable HTTPS
- ✅ Configure CORS for your domain
- ✅ Set up error logging

### Example Deployment (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/login.html` | GET | Login page |
| `/dashboard` | GET | Main dashboard |
| `/api/marketing` | POST | Generate marketing campaign |
| `/api/sales` | POST | Generate sales pitch |
| `/api/lead-scoring` | POST | Score and qualify lead |

---

## 🔮 Future Enhancements

- [ ] Multi-user authentication with database
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Template library
- [ ] Email integration
- [ ] CRM integration
- [ ] Multi-language support
- [ ] Custom AI model fine-tuning

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

**Project Maintainer:** Aditya Raj  
**Email:** adrj281205@gmail.com  
**Live Demo:** [[https://marketmind.example.com](https://marketmind.example.com)](https://mega.nz/file/qVFRRSZI#iB_yGjCbcnUMqh3AB3E99bqkOnhZxoT0FUlzOvIeWbQ)

---

## 🙏 Acknowledgments

- Groq for providing the AI infrastructure
- Font Awesome for icons
- Google Fonts for typography
- The open-source community

---

**Built with ❤️ for modern sales and marketing teams**
