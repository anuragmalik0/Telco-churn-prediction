# Telecom Customer Churn Prediction
### End-to-End Machine Learning Project

Telecom companies spend 5–7x more acquiring new customers than retaining 
existing ones. This project builds a complete machine learning pipeline to 
identify customers who are likely to churn, helping businesses take proactive 
retention action before losing them.

---

## Problem Statement

Given historical data about 7,043 telecom customers — including their contract 
type, services subscribed, tenure, and monthly charges — the goal is to predict 
whether a customer will churn (cancel their subscription) or not.

This is a **binary classification problem** with real business impact:
- Correctly identifying a churner = opportunity to retain them
- Missing a churner = lost revenue
- False alarm = wasted retention budget

---

## Dataset

- **Source:** IBM Telco Customer Churn Dataset
- **Size:** 7,043 customers × 20 features
- **Target:** Churn (Yes/No) — 26.5% churn rate
- **Challenge:** Imbalanced dataset (73% No, 27% Yes)

**Features include:**
- Demographics: gender, senior citizen, partner, dependents
- Services: phone, internet, streaming, online security, tech support
- Account: contract type, payment method, tenure, monthly & total charges

---

## Project Workflow

### 1. Exploratory Data Analysis (EDA)
- Analyzed churn patterns across all features
- Found that month-to-month contract customers churn at **42%** vs 
  only **3%** for two-year contract customers
- Customers in their first 12 months have a **47% churn rate**
- Higher monthly charges (above $65) strongly correlate with churn
- Visualized distributions, correlations, and segment-wise churn rates

### 2. Data Preprocessing
- Removed `customerID` (irrelevant unique identifier)
- Converted `TotalCharges` from string to numeric
- Handled 11 missing values using median imputation
- Encoded all categorical variables using Label Encoding

### 3. Feature Engineering
Created 3 new features to improve model performance:

| Feature | Description |
|---------|-------------|
| `ChargesPerMonth` | TotalCharges / Tenure — measures spending intensity |
| `IsLongTermContract` | 1 if annual/two-year contract, 0 if month-to-month |
| `NumServices` | Count of services subscribed (phone, security, streaming etc.) |

### 4. Handling Class Imbalance — SMOTE
The dataset had a 73/27 split. Without fixing this, models would be 
biased toward predicting "No Churn" and miss actual churners.

Applied **SMOTE (Synthetic Minority Over-sampling Technique)** on training 
data only to avoid data leakage. SMOTE creates synthetic samples of the 
minority class rather than simply duplicating them.

### 5. Model Training
Trained and evaluated 5 machine learning models:

| Model | Why Used |
|-------|----------|
| Logistic Regression | Baseline linear model, interpretable |
| K-Nearest Neighbors | Distance-based, captures local patterns |
| Random Forest | Ensemble of decision trees, handles non-linearity |
| Gradient Boosting | Sequential boosting, strong on tabular data |
| Stacking Ensemble | Combines all models for best performance |

### 6. Hyperparameter Tuning
Used **GridSearchCV with StratifiedKFold (5 folds)** to tune Gradient 
Boosting. Optimized for **AUC-ROC** instead of accuracy because:
- Accuracy is misleading on imbalanced data
- AUC-ROC measures the model's ability to distinguish churners from 
  non-churners at all thresholds

Tuned parameters: `n_estimators`, `learning_rate`, `max_depth`, 
`subsample`, `min_samples_split`

---

## Results

| Model | Accuracy | F1-Score | AUC-ROC |
|-------|----------|----------|---------|
| Gradient Boosting (Tuned) | 87% | 0.75 | 0.92 |
| Stacking Ensemble | 86% | 0.74 | 0.91 |
| Random Forest | 83% | 0.70 | 0.88 |
| Logistic Regression | 79% | 0.64 | 0.85 |
| KNN | 77% | 0.61 | 0.82 |

**Best Model: Gradient Boosting (Tuned)**
- Accuracy improved from ~79% (baseline) to **87%**
- AUC-ROC of **0.92** means the model correctly ranks a random churner 
  above a non-churner 92% of the time

---

## Key Business Insights

Based on feature importance and EDA, the top churn drivers are:

1. **Contract Type** — Month-to-month customers are the highest risk segment
2. **Tenure** — First year customers need special attention
3. **Monthly Charges** — High-paying customers are more price-sensitive
4. **Online Security & Tech Support** — Customers without these churn more
5. **Number of Services** — More services = more stickiness = less churn

**Recommendations:**
- Offer discounts to move month-to-month customers to annual contracts
- Create an onboarding loyalty program for customers in their first 12 months
- Bundle security and tech support at a lower price to increase retention
- Build a risk score dashboard using this model for the retention team

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3 |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Class Imbalance | Imbalanced-learn (SMOTE) |
| Environment | Jupyter Notebook |

---

## Project Structure

telco-churn-prediction/
│
├── Telco_Churn_Project.ipynb    # Main notebook with full pipeline
├── Telco-Customer-Churn.csv     # Dataset
└── README.md                    # Project documentation

## How to Run

```bash
# Install dependencies
pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn jupyter

# Launch notebook
jupyter notebook Telco_Churn_Project.ipynb
```

---

## What I Learned

- How to approach a real-world imbalanced classification problem
- Why AUC-ROC is a better metric than accuracy for churn prediction
- The importance of feature engineering in improving model performance
- How ensemble methods like Stacking and Gradient Boosting outperform 
  single models on structured data
- Translating ML results into actionable business recommendations

---

*Built by Anurag Malik | 2nd Year CSE-AI | Chitkara University*
