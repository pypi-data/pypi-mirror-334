# Development

## Install

```
pip install '.[dev]'
```

## Configure

To run the configure command outside the main `docketanalyzer` package, use this:

```
python -m docketanalyzer_core configure
```

## Test

```
pytest -vv
```

## Format

```
ruff format . && ruff check --fix .
```

## Build and Push to PyPi

```
python -m docketanalyzer_core dev build
python -m docketanalyzer_core dev build --push
```
