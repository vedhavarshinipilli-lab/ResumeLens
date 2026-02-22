ResumeLens – AI Resume Analyzer
Live Demo
Frontend: https://resumelens-frontend.onrender.com�
Backend: https://resumelens-backend.onrender.com�
Overview
ResumeLens is an AI-powered web application that analyzes a resume against a job description and generates a structured match report.
It calculates:
Match percentage
Match level (Strong / Moderate / Weak)
Matched skills
Missing skills
Improvement suggestions
Downloadable PDF report

This project demonstrates full-stack architecture with AI integration and production deployment.
Architecture

Client (Browser)
↓
React Frontend (Vite)
↓
FastAPI Backend (Render)
↓
Hugging Face AI Model

The frontend communicates with the backend via REST API.
The backend securely calls the Hugging Face inference API using environment variables for authentication.

Tech Stack
Frontend
React
Vite
JavaScript
Fetch API
Static deployment using serve
Backend
Python
FastAPI
Uvicorn
CORS Middleware
Hugging Face Inference API
Deployment
Render (Frontend + Backend)
Environment Variables for production config

Security
Hugging Face API token stored securely in backend environment variables
Token never exposed to frontend
CORS configured properly
Backend binds to 0.0.0.0:$PORT for production compatibility

Screenshots
![Home Page] "C:\Users\amrutha varshini\Pictures\Screenshots\Screenshot 2026-02-22 071733.png"
![Analysis Result] "C:\Users\amrutha varshini\Pictures\Screenshots\Screenshot 2026-02-22 071902.png"

Future Improvements
User authentication
Resume history tracking
Database integration
Improved AI prompt engineering
Performance optimization
Rate limiting
What I Learned
Full-stack architecture design
REST API development
AI model integration
Production deployment
Environment variable management
Debugging cloud hosting issues
Cold start behavior in serverless environments
Author vedha varshini
GitHub: https://github.com/vedhavarshinipilli-lab
LinkedIn: https://www.linkedin.com/in/vedha-varshini-dev
