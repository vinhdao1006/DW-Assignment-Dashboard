# define variables

STREAMLIT_APP = app.py
FASTAPI_APP = fastApi_DSS/main.py

.PHONY: frontend backend run_app

frontend:
	streamlit run $(STREAMLIT_APP)

backend:
	uvicorn $(FASTAPI_APP):app --reload &

run_app: backend frontend 