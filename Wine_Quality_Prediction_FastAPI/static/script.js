async function predict(event) {
  event.preventDefault();

  const form = document.getElementById('predict-form');
  const formData = new FormData(form);
  const jsonData = {};

  formData.forEach((value, key) => {
    jsonData[key] = parseFloat(value);
  });

  const response = await fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(jsonData)
  });

  const resultDiv = document.getElementById('result');

  if (response.ok) {
    const data = await response.json();
    resultDiv.innerText = `✅ Predicted Wine Quality: ${data.predicted_quality}`;
  } else {
    const error = await response.json();
    resultDiv.innerText = `❌ Error: ${error.detail}`;
  }
}
