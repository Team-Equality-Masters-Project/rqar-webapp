
## To setup and run webapp
0. Set up environment:
```python -m venv ~/.streamlit_ve```
```source ~/.streamlit_ve/bin/activate```

1. Install dependencies: 
```pip install -r requirements.txt```

2. Run streamlit app: 
```streamlit run app.py```

(Note: If running into issues of "ModuleNotFoundError", try uninstalling and re-installing package.)

3. Open browser and navigate to page: 
```http://localhost:8501/```


## Github CI/CD
Reference: https://docs.github.com/en/actions/deployment/deploying-to-google-kubernetes-engine
