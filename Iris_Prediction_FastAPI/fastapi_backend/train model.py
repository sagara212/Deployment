from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save model ke file
with open("D:\DOCUMENT\INFORMATIKA\FULL PROJEK\FastAPI\iris_fastAPI_project\model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model sudah dilatih dan disimpan di model/model.pkl")
