import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve, classification_report
import joblib
import os

print("Loading dataset...")
df = pd.read_csv("data/diabetes.csv")
print(f"Shape: {df.shape}")

zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
df[zero_cols] = df[zero_cols].replace(0, np.nan)
df.fillna(df.median(numeric_only=True), inplace=True)

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("Training Random Forest...")
model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced")
model.fit(X_train_scaled, y_train)

y_pred  = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
print(f"\nAccuracy : {acc:.4f}")
print(f"ROC-AUC  : {auc:.4f}")
print(classification_report(y_test, y_pred, target_names=["No Diabetes", "Diabetes"]))

os.makedirs("model", exist_ok=True)
joblib.dump(model,  "model/rf_model.joblib")
joblib.dump(scaler, "model/scaler.joblib")
joblib.dump(list(X.columns), "model/feature_names.joblib")

print("\n✅ Model saved to model/rf_model.joblib")
print("✅ Scaler saved to model/scaler.joblib")
print(f"\nFinal — Accuracy: {acc:.2%}  |  AUC: {auc:.3f}")