*This is the repo for the upcoming Hackathon project! Detail about this project is going to be updated later...🪴*

### Project Structure
```
hackathon_project/
│
├── backend/
│   ├── venv/                # Virtual environment for backend (FastAPI)
│   ├── logic/
│   │   ├── model.py
│   │   ├── graph.py
│   │   ├── utils.py          # Main entry for Backend
│   ├── main.py 
│   ├── requirements.txt      # Backend dependencies (FastAPI, Uvicorn)
│
├── frontend/
│   ├── venv/                # Virtual environment for frontend (Flask)
│   ├── app.py               # Main entry for frontend
│   ├── templates/
│   │   ├── index.html
│   │   ├── chatbot.html
│   │   ├── other_page.html
│   ├── static/
│   │   ├── css
│   │   ├── js
│   │   ├── ....
│   ├── requirements.txt      # Frontend dependencies (Flask, Requests)
└── README.md
```

* ```backend``` handle the chatbot logic and create API as well as provide endpoints for the ```frontend``` can interact with

* ```frontend``` using Flask as a framework to render webpage and use endpoint provided by ```backend``` (You can use any frontend stack you want built, for example: React, Vue, or Angular, can make requests to the FastAPI backend using libraries like fetch or axios for HTTP requests)

