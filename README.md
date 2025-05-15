# ICE-ID: A Novel Historical Census Data Benchmark

**A benchmark for longitudinal identity resolution on 220 years of Icelandic census records (1703–1920), comparing NARS, LLMs, and an ML ensemble.**

## Overview  
ICE-ID provides:  
- A large, open tabular dataset spanning 1703–1920 with person-entity links across generations.  
- Two identity resolution tasks: within-census and across-census matching.  
- Three pipelines:  
  1. **Preprocessing**: cleans, canonicalizes and encodes raw CSVs into ML-ready artifacts.  
  2. **Ensemble**: trains XGBoost/LightGBM/CatBoost/RandomForest ensemble with repeated runs and diagnostics.  
  3. **LLMs**: fine-tunes TriBERTa, DistilBERT and MiniLM cross-encoders for ER.  

## Repo Structure  
```
├── raw_data/                   # Input CSVs (people.csv, manntol_*.csv, geography files)
├── artifacts/                  # Generated features & graphs
├── models_ensemble_gpu/        # Saved ensemble models
├── reports_gpu/                # Ensemble run reports & metrics
├── models_er/                  # Saved LLM checkpoints & summaries
├── ICE-ID-2-Preprocessing.ipynb
├── ICE-ID-2-Ensemble.ipynb
├── ICE-ID-2-LLMs.ipynb
└── README.md
```  

## Prerequisites  
- Python 3.8+  
- CUDA 11+ for GPU (optional)  

## Installation  
```bash
git clone <repo-url>
cd ICE-ID
pip install -r requirements.txt
```  

> **requirements.txt** should include:  
> numpy, pandas, scipy, scikit-learn, torch, torch-geometric, xgboost, lightgbm, catboost, transformers, sentence-transformers, tqdm, joblib, matplotlib  

## Data Preparation  
Place all raw CSVs under `raw_data/`. Then, in a Jupyter session or terminal:  
```bash
jupyter notebook ICE-ID-2-Preprocessing.ipynb
# or
python3 -m notebook ICE-ID-2-Preprocessing.ipynb
```  
This will generate `artifacts/iceid_ml_ready.npz`, `row_labels.csv`, `temporal_graph.pt`, etc.

## Usage  

### 1. Ensemble Pipeline  
Run end-to-end training (10 runs, GPU if available):  
```bash
jupyter notebook ICE-ID-2-Ensemble.ipynb
```  
Outputs saved under `models_ensemble_gpu/` and `reports_gpu/`.

### 2. LLM Pipeline  
Train and evaluate on TriBERTa, DistilBERT, MiniLM:  
```bash
jupyter notebook ICE-ID-2-LLMs.ipynb
```  
Checkpoints and summary CSVs in `models_er/`.

## License 
MIT © 2025  
