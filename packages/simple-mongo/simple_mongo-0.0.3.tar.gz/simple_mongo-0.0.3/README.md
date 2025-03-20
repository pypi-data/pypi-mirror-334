# Simple Mongo (A Simple Mongodb Library)

## Getting Started:

- To run and test the library, it should required to provide an environment variables by creating an <i>.env</i> file:

```bash
    MONGODB_URL="mongodb://your-url-here"
    MONGODB_NAME="your-database-name-here"
```

### Running a simple query:

- Get All documents within a collection

```python

from simple_mongo.database import MongoDB

MongoDB.all('<COLLECTION-NAME-HERE>')

```
