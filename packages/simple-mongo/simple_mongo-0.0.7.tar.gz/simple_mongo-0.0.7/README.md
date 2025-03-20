# Simple Mongo (A Simple Mongodb Library)

## Getting Started:

- To run and test the library, it should required to provide an environment variables by creating an <i>.env</i> file:

```bash
    MONGODB_URL="mongodb://your-url-here"
    MONGODB_NAME="your-database-name-here"
```

### Running a simple query:

- Get All documents within a collection:

```python
# supposed that we have a 'users' collection

from simple_mongo.database import MongoDB

MongoDB.all('users')

```

- Get a specific document:

```python
MongoDB.find_one({
    'name' : 'Taylor Swift'
})

```

- Create a simple data to a collection:

```python

MongoDB.create('users',
    {
        'name': 'John Doe', 
        'email': 'johndoe@gmail.com'
    }
)
```

- Update a document from a collection:

```python

MongoDB.update('users', {
    'name' : 'John Doe'
}, {
    'name' : 'John Sins'
})

```

- Delete a document from a collection:

```python

MongoDB.delete('users', {
    'name' : 'John Sins'
})

```

<hr/>

Repository Link: <a href="https://github.com/nojram00/simple-mongo">https://github.com/nojram00/simple-mongo</a>
