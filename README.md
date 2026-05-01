# Telecom Customer Churn Prediction

A machine learning project to identify telecom customers likely to cancel their subscription, enabling proactive retention strategies.

## Results

| Model | Accuracy | AUC-ROC |
|-------|----------|---------|
| Gradient Boosting (Tuned) | 87% | 0.92 |
| Stacking Ensemble | 86% | 0.91 |
| Random Forest | 83% | 0.88 |
| Logistic Regression | 79% | 0.85 |
| KNN | 77% | 0.82 |

## What I Did

- Cleaned and explored a dataset of 7,043 telecom customers
- Built 3 new features: spending intensity, contract type flag, and service count
- Handled class imbalance (73/27 split) using SMOTE
- Trained and compared 5 ML models
- Tuned Gradient Boosting using GridSearchCV optimized for AUC-ROC
- Identified key churn drivers: contract type, tenure, and monthly charges

## Tech Stack

Python, Pandas, Scikit-learn, Imbalanced-learn, Matplotlib, Seaborn

## How to Run

```bash
pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn jupyter
jupyter notebook Telco_Churn_Project.ipynb
```

## Dataset

IBM Telco Customer Churn dataset — 7,043 customers, 20 features including contract type, services subscribed, tenure, and monthly charges.
