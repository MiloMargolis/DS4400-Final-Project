# Boston Properties Redevelopment Potential Prediction

**Authors:** Milo Margolis

**Course:** DS4400 Final Project

## Project Overview

This project develops binary classification models to predict the redevelopment potential for Boston properties using parcel data. Properties are labeled as high potential based on indicators such as low building-to-land ratios and underutilized FAR (Floor Area Ratio). The project implements and compares multiple machine learning models including logistic regression, KNN, and decision trees with proper training, validation, and hyperparameter tuning to demonstrate overfitting prevention.

## Project Structure

```
DS4400-Final-Project/
├── data/
│   └── raw/
│       └── boston_properties.csv    # Exported dataset from Supabase
├── notebooks/
│   ├── 00_data_check.ipynb         # Data verification notebook
│   └── final_project.ipynb          # Main project notebook
├── scripts/
│   ├── export_data.py               # Export data from Supabase to CSV
│   └── verify_env.py                # Verify environment variables
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (not in git)
└── README.md                        # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SECRET_KEY=your-secret-key-here
```

### 3. Verify Setup

```bash
python scripts/verify_env.py
```

### 4. Export Data from Supabase

```bash
python scripts/export_data.py
```

This will create `data/raw/boston_properties.csv`.

## Usage

### Main Project Notebook

Open and run `notebooks/final_project.ipynb` in Jupyter. The notebook includes:

1. **Data Cleaning**: Missing values, duplicates, outliers
2. **Feature Engineering**: Building-to-land ratio, property age, FAR gap
3. **Exploratory Data Analysis**: Correlation heatmaps, target distribution
4. **Modeling**: 
   - Baseline Logistic Regression
   - Regularized Logistic Regression (with cross-validation)
   - KNN (with hyperparameter tuning)
   - Decision Tree (with depth tuning)
5. **Results**: Model comparison, ROC curves, test set evaluation

### Data Verification

Run `notebooks/00_data_check.ipynb` to verify the exported dataset.

## Key Features

- **Data Export**: Automated export from Supabase with pagination
- **Comprehensive Cleaning**: Missing value handling, outlier removal, duplicate detection
- **Feature Engineering**: Created 3 new features for modeling
- **Multiple Models**: Comparison of 4 different classification algorithms
- **Overfitting Prevention**: Cross-validation, regularization, hyperparameter tuning
- **Evaluation**: Multiple metrics (accuracy, precision, recall, F1, AUC) with ROC curves

## Dependencies

- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `scikit-learn` - Machine learning models
- `supabase` - Database connection
- `python-dotenv` - Environment variable management

## Notes

- The `.env` file is excluded from git for security
- Data files are large (>200MB) and excluded from git
- All models use stratified train/validation/test splits (70/15/15)
- Features are standardized using StandardScaler fitted only on training data

