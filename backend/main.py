
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prediction_service import predict_future, fetch_data
import os

app = FastAPI()

# Configure CORS for frontend access
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/predict")
def get_prediction():
    try:
        # Predict next 8 weeks
        data = predict_future(weeks_to_predict=8)
        return data
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
