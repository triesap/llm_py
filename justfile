run:
    python3 ./main.py

app:
    uvicorn app.chat:app --reload
