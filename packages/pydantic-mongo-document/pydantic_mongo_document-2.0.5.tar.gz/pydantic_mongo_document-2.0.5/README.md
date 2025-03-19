# Pydantic Mongo Document

`pydantic_mongo_document` is a Python library that combines the power of Pydantic models with MongoDB, providing an elegant way to work with MongoDB documents using Python type hints and data validation.

## Features

- Full Pydantic integration with MongoDB documents
- Support for both synchronous and asynchronous operations
- Type-safe document models with validation
- Built-in ObjectId handling and JSON encoding
- Flexible MongoDB replica configuration
- Rich query interface with type hints
- Automatic index management
- Support for MongoDB transactions

## Installation

Install the package using [pip](https://pip.pypa.io/en/stable/) or [poetry](https://python-poetry.org).

```bash
# Using pip
pip install pydantic_mongo_document

# Using poetry
poetry add pydantic_mongo_document
```

## Basic Usage

### Configuration

First, configure your MongoDB connection:

```python
from pydantic_mongo_document import Document

# Basic configuration
Document.set_replica_config({
    "localhost": {
        "uri": "mongodb://localhost:27017",
        "client_options": {
            "replica_set": "rs0",  # optional
            "max_pool_size": 100,
            "write_concern": "majority",
            "read_preference": "primaryPreferred"
        }
    }
})
```

### Define Your Models

Create document models by inheriting from either sync or async Document classes:

```python
from pydantic_mongo_document.document.asyncio import Document as AsyncDocument
from pydantic_mongo_document.document.sync import Document as SyncDocument

# Async Document
class AsyncUser(AsyncDocument):
    __replica__ = "localhost"
    __database__ = "myapp"
    __collection__ = "users"

    name: str
    email: str
    age: int | None = None

# Sync Document
class User(SyncDocument):
    __replica__ = "localhost"
    __database__ = "myapp"
    __collection__ = "users"

    name: str
    email: str
    age: int | None = None
```

### Async Usage Example

```python
async def user_crud_example():
    # Create a new user
    user = AsyncUser(name="John Doe", email="john@example.com")
    await user.insert()

    # Find a user
    user = await AsyncUser.one(add_query={"email": "john@example.com"})
    
    # Update user
    user.age = 30
    await user.commit_changes()

    # Delete user
    await user.delete()

    # Query multiple users
    async for user in AsyncUser.all(add_query={"age": {"$gt": 25}}):
        print(user)

    # Count users
    count = await AsyncUser.count(add_query={"age": {"$gt": 25}})
```

### Sync Usage Example

```python
# Create a new user
user = User(name="Jane Doe", email="jane@example.com")
user.insert()

# Find a user
user = User.one(add_query={"email": "jane@example.com"})

# Update user
user.age = 28
user.commit_changes()

# Query multiple users
for user in User.all(add_query={"age": {"$gt": 25}}):
    print(user)

# Count users
count = User.count(add_query={"age": {"$gt": 25}})
```

## Advanced Features

### Working with MongoDB Transactions

```python
async def transaction_example():
    async with await AsyncUser.client().start_session() as session:
        async with session.start_transaction():
            user = AsyncUser(name="John", email="john@example.com")
            await user.insert(session=session)
            # Transaction will automatically commit if no exceptions occur
            # or rollback if an exception is raised
```

### Custom Indexes

```python
class User(AsyncDocument):
    __replica__ = "localhost"
    __database__ = "myapp"
    __collection__ = "users"

    name: str
    email: str

    @classmethod
    async def create_indexes(cls):
        # Create custom indexes
        await cls.collection().create_index("email", unique=True)
        await cls.collection().create_index([("name", 1), ("email", 1)])
        return await super().create_indexes()
```

### Advanced Queries

```python
# Find with projection
user = await User.one(
    add_query={"age": {"$gt": 25}},
    projection={"name": 1, "email": 1}
)

# Complex queries
users = User.all(add_query={
    "age": {"$gt": 25},
    "email": {"$regex": "@example\.com$"},
    "$or": [
        {"name": {"$regex": "^John"}},
        {"name": {"$regex": "^Jane"}}
    ]
})
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT License](LICENSE)
