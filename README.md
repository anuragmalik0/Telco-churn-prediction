# Telecom Customer Churn Prediction

> End-to-end ML pipeline to predict telecom customer churn — with a live interactive web app built on top.

Telecom companies spend 5–7× more acquiring new customers than retaining existing ones.
This project identifies at-risk customers before they leave, and serves predictions through a
production-style Streamlit dashboard with real-time retention recommendations.

---

## Live App

🔗 **[Open ChurnIQ — Live Demo](https://telco-churn-prediction-vdzndsypitwqxadlvcewry.streamlit.app)**

```bash
# Or run locally
pip install streamlit scikit-learn pandas numpy matplotlib
streamlit run app.py
```

---

## Results

| Model | Accuracy | F1-Score | AUC-ROC |
|-------|----------|----------|---------|
| Gradient Boosting (Tuned) | 87% | 0.75 | 0.92 |
| Stacking Ensemble | 86% | 0.74 | 0.91 |
| Random Forest | 83% | 0.70 | 0.88 |
| Logistic Regression | 79% | 0.64 | 0.85 |
| KNN | 77% | 0.61 | 0.82 |

Best model: **Gradient Boosting (Tuned)** — AUC-ROC 0.92

---

## Problem

Given data on 7,043 telecom customers (contract type, tenure, services, charges),
predict whether they will churn. Binary classification with a 73/27 class imbalance.

Missing a churner = lost revenue. False alarm = wasted retention budget.
The goal is to maximise recall on the minority class while keeping precision reasonable.

---

## What I Built

### 1. EDA
Explored churn patterns across every feature. Key findings:
- Month-to-month customers churn at **42%** vs 3% for two-year contracts
- Customers in their **first 12 months** have a 47% churn rate
- Monthly charges above **$65** strongly correlate with churn

### 2. Feature Engineering
Created 3 new features from the raw data:

| Feature | Description |
|---------|-------------|
| `ChargesPerMonth` | TotalCharges / Tenure — spending intensity |
| `IsLongTermContract` | Binary flag for annual or two-year contracts |
| `NumServices` | Count of active services (security, streaming, support etc.) |

### 3. Class Imbalance — SMOTE
Applied SMOTE on training data only to prevent data leakage.
Balanced 73/27 split to 50/50 before model training.

### 4. Model Training
Trained 5 models and compared across Accuracy, F1, and AUC-ROC — not just accuracy,
since accuracy is misleading on imbalanced datasets.

### 5. Hyperparameter Tuning
GridSearchCV with StratifiedKFold (5 folds), optimising for AUC-ROC.
Tuned: `n_estimators`, `learning_rate`, `max_depth`, `subsample`, `min_samples_split`

### 6. Streamlit App
Built a full interactive dashboard on top of the trained model:
- Real-time churn probability with a visual gauge
- Risk factor breakdown per customer
- Personalised retention action recommendations
- Feature importance chart
- Downloadable prediction report

---

## Key Business Insights

1. **Contract type** is the strongest churn signal — month-to-month customers are 3× more likely to leave
2. **First-year customers** need an onboarding loyalty program
3. **Bundling** online security and tech support reduces churn significantly
4. **High monthly charges** make customers price-sensitive — personalised plans help

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3 |
| Data | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| ML | Scikit-learn |
| Imbalance | Imbalanced-learn (SMOTE) |
| App | Streamlit |
| Environment | Jupyter Notebook |

---

## Project Structure

```
telco-churn-prediction/
├── Telco_Churn_Project.ipynb    # Full ML pipeline notebook
├── app.py                       # Streamlit prediction app
├── model.pkl                    # Trained Gradient Boosting model
├── scaler.pkl                   # Feature scaler
├── feature_cols.pkl             # Feature column names
├── Telco-Customer-Churn.csv     # Dataset
└── README.md
```

---

## What I Learned

- Why AUC-ROC matters more than accuracy for imbalanced classification
- How feature engineering directly improves model signal
- How SMOTE works and why it must only be applied to training data
- Why ensemble methods outperform single models on structured/tabular data
- How to translate ML outputs into actionable business recommendations
- How to deploy a trained model as a real interactive web application

---

*Anurag Malik — 2nd Year CSE-AI, Chitkara University*
