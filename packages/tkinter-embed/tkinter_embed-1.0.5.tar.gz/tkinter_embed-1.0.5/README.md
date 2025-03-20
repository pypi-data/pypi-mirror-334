# tkinter-embed

install tkinter for embedded python

```cmd
.\python pip.pyz install setuptools --target .
.\python pip.pyz install tkinter-embed --target .
```

## build

```cmd
python -m build --sdist
```


## test

```cmd
pip install -v --target embed .\dist\tkinter_embed-1.0.0.tar.gz
```

## upload

```cmd
python -m twine upload dist/*
```
