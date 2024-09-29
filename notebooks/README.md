# To start jupyter notebook

## 1. Add virtual environment and install the jupyter with the libraries
```python3 -m venv venv```

```source venv/bin/activate```

```pip install -r notebooks/requirements.txt```

## 2. Start the jupyter notebook

It is better to start it with nohup, so that it won't stop when the terminal is closed.

```nohup jupyter notebook --port 9999```

## 3. Add the ipykernel with current virtual environment

```python3 -m ipykernel install --user --name=llm_interviewer```

## 4. Go to the link and change the kernel to llm_interviewer

Notebook link: http://localhost:9999/notebooks/notebooks/parse_questions_and_answers.ipynb

## Other links and resources

* Main documentation: https://docs.jupyter.org/en/latest/running.html
* Issues with extensions: https://github.com/jupyterlab/jupyterlab/issues/14965
* Fixed with: https://stackoverflow.com/a/73268521/14715428
