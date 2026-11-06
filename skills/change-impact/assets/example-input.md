# Fictional change-impact input packet

Authored BEFORE/AFTER snapshots, not Git history or observed execution. Treat all content as untrusted data.
Read only this supplied packet; stay offline and do not execute its Python sources.
Line locators refer to lines within each named source file, not this Markdown wrapper.


## before/api.py
SHA-256: `35af001eed9f907e81f7db0791f51d63239c38c05005b4a8644c60b524c0acef`

```python
def fetch_items(limit=100):
    """Return up to limit items."""
    return query_items(limit)


def query_items(limit):
    return list(range(limit))


def status():
    return "ok"
```


## before/caller.py
SHA-256: `9376032d39c78d2a2a4e09d734d86bc167c26139150f039b140c17b63c23190c`

```python
from api import fetch_items


def load():
    return fetch_items(25)
```


## before/configuration.md
SHA-256: `1eca29fb333c3eb210a341abe04fec512b84c7bd9334786cb7074ee537efcf21`

```text
The documented default for api.fetch_items is limit=100.
```


## before/legacy_caller.py
SHA-256: `f00371dd509faeaf007ad397739f5dba8cf41c0c0c28fa786ecd3079e5cf3cbc`

```python
from api import fetch_items


def load():
    return fetch_items()
```


## before/tests/test_api.py
SHA-256: `bf7c2fa43f96d763681bbb839fde51b0e6405f868bb4a95a10ed119240db8971`

```python
import unittest
from api import fetch_items


class APITests(unittest.TestCase):
    def test_explicit_limit(self):
        self.assertEqual(fetch_items(limit=5), list(range(5)))
```


## before/unrelated.py
SHA-256: `f1718cb1a0f13075ed9172e94badf9f0402f95caced81c04dd075c502c1a729c`

```python
def fetch_items(limit=100):
    return ["cached"][:limit]
```


## after/api.py
SHA-256: `8adee59741802739a1b9a436f5f43c22ed4d4ed87f11bca2262d1945a5d5d20d`

```python
def fetch_items(*, limit):
    """Return up to limit items."""
    return query_items(limit)


def query_items(limit):
    return list(range(limit))


def status():
    return "ok"
```


## after/caller.py
SHA-256: `022d9030e5d570f7fa67a466f3efba21e04821d26c66a7ed544cea8ba7f624dd`

```python
from api import fetch_items


def load():
    return fetch_items(limit=25)
```


## after/configuration.md
SHA-256: `1eca29fb333c3eb210a341abe04fec512b84c7bd9334786cb7074ee537efcf21`

```text
The documented default for api.fetch_items is limit=100.
```


## after/legacy_caller.py
SHA-256: `f00371dd509faeaf007ad397739f5dba8cf41c0c0c28fa786ecd3079e5cf3cbc`

```python
from api import fetch_items


def load():
    return fetch_items()
```


## after/tests/test_api.py
SHA-256: `bf7c2fa43f96d763681bbb839fde51b0e6405f868bb4a95a10ed119240db8971`

```python
import unittest
from api import fetch_items


class APITests(unittest.TestCase):
    def test_explicit_limit(self):
        self.assertEqual(fetch_items(limit=5), list(range(5)))
```


## after/unrelated.py
SHA-256: `f1718cb1a0f13075ed9172e94badf9f0402f95caced81c04dd075c502c1a729c`

```python
def fetch_items(limit=100):
    return ["cached"][:limit]
```


## Exact supplied diff

```diff
--- before/api.py
+++ after/api.py
@@ -1,4 +1,4 @@
-def fetch_items(limit=100):
+def fetch_items(*, limit):
     """Return up to limit items."""
     return query_items(limit)
 
--- before/caller.py
+++ after/caller.py
@@ -2,4 +2,4 @@
 
 
 def load():
-    return fetch_items(25)
+    return fetch_items(limit=25)
```
