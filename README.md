# Registration Prediction Website

This project is a full-stack application designed to predict student registrations. It consists of a FastAPI backend that serves predictions using an XGBoost model and a Next.js frontend for visualizing the data.

## Project Structure

- **backend/**: Contains the FastAPI application, machine learning model training scripts, and prediction logic.
- **frontend/**: A Next.js application for the user interface.
- **data/**: Contains the dataset used for training and fallback data.

## Prerequisites

- **Python 3.8+**
- **Node.js 18+** & **npm**

## Installation and Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Retrain the model:
   The repository comes with a pre-trained model. If you wish to retrain it:
   ```bash
   python train_model.py
   ```

5. Run the server:
   ```bash
   python main.py
   ```
   The backend API will be available at `http://localhost:8000`.
   - Health check: `http://localhost:8000/health`
   - Prediction endpoint: `http://localhost:8000/api/predict`

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000` to view the application.

## API Documentation

### `GET /api/predict`

Returns historical data and future predictions for student registrations.

**Response Format:**
```json
{
  "last_updated": "2023-10-27T10:00:00.000000",
  "history": [ ... ],
  "forecast": [
    {
      "week_ending": "2023-11-03",
      "prediction": 150,
      "confidence_lower": 120,
      "confidence_upper": 180
    },
    ...
  ]
}
```
