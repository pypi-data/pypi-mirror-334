# etag_generator

Given a python list or dictionary that will represents a JSON return value, generate an ETag that is guaranteed to be stable.

Will generate an etag from most data commonly used types:
* dict
* list
* string
* int / float

Works to create stable identifiers even with complex, multi-level objects.

Does not have the smarts to handle circular references.

Currently doesn't deal with the following data types:
* tuple
* classes
* boolean
* none
* other stuff that might exist that isn't in the supported list

## installation

pip install etag_generator

## usage

```python
from etag_generator import generate_etag

etag = generate_etag({"any_object":"value"})
```