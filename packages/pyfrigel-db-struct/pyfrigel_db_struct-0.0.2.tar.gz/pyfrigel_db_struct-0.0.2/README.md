# How to use

First of all clone the repo.

To run the script anywhere:
    
    1) pip install -r requirements.txt
    2) Run the script!

If you want to run the script in a virtual env then:
    
    1) Install pipenv (pip install pipenv)
    2) Install requirements (pipenv install)
    3) Run the script! (inside the env)


# How to release new version to PyPi

1) Update the version in pyproject.toml
2) Run the following commands:

```python -m pip install --upgrade build```

```cd src```

```python -m pip install --upgrade twine```

```python -m build```


```python -m twine upload dist/*```
