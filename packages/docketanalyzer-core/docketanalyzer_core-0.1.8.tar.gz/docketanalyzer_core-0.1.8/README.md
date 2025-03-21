[![Docs](https://img.shields.io/badge/docs-in%20progress-yellow)](https://docs.docketanalyzer.com/api/main/)

# Docket Analyzer Core

Core utilities for Docket Analyzer modules

Full documentation available at [docs.docketanalyzer.com](https://docs.docketanalyzer.com)

## Install and Configure

Install docketanalyzer:

```
pip install `docketanalyzer[all]`
```

Run the configuration script:

```
da configure
```

## Load Configured Env

```
from docketanalyzer import env

print(env.VARIABLE_NAME)
```

## Service Clients

### Elasticsearch

```python
from docketanalyzer import load_elastic

es = load_elastic()
print(es.ping())
```

### Postgres

```python
from docketanalyzer_core import load_psql

db = load_psql()
print(db.status())
```

### Redis

```python
from docketanalyzer import load_redis

redis = load_redis()
print(redis.ping())
```

### S3

```python
from docketanalyzer import load_s3

s3 = load_s3()
print(s3.status())
```

## Registry

Example usage:

```python
from docketanalyzer import Registry, SomeBaseClass


class SomeRegistry(Registry):
    def find_filter(self, obj):
        return (
            isinstance(obj, type) and
            issubclass(obj, SomeBaseClass) and
            obj is not SomeBaseClass
        )


some_registry = SomeRegistry()

# Find subclasses of SomeBaseClass in this module
some_registry.find(recurse=True)

# Import these into the current namespace
some_registry.import_registered()
```
