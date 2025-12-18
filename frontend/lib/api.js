
export async function fetchPrediction() {
  try {
    const res = await fetch('http://localhost:8000/api/predict', {
      cache: 'no-store',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch data: ${res.status}`);
    }

    return res.json();
  } catch (error) {
    console.error('Error fetching prediction:', error);
    return null;
  }
}
