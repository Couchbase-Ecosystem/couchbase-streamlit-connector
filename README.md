# Couchbase-Streamlit Connector

## Overview  

The **Couchbase-Streamlit Connector** provides a seamless way to integrate Couchbase with Streamlit applications. It simplifies database operations, allowing developers to interact with Couchbase clusters directly within Streamlit without requiring extensive SDK knowledge.  

With this connector, developers can efficiently perform CRUD (Create, Read, Update, Delete) operations, execute SQL++ queries, and dynamically manage Couchbase collections, scopes, and buckets—all within a Streamlit app. This enables rapid prototyping and interactive data visualization while leveraging Couchbase’s powerful database capabilities.  

**Key Benefits**
- **Simplified Database Access**: Eliminates the need for seperate SDK implementations.  
- **Streamlit-Native Integration**: Designed to work seamlessly with `st.connection()`.  
- **Flexible Querying**: Supports both key-value operations and SQL-like queries using SQL++.  
- **Dynamic Data Management**: Easily switch between different Couchbase buckets, scopes, and collections.  
- **Improved Developer Productivity**: Reduces boilerplate code, allowing developers to focus on building interactive applications.  


## Prerequisites

### System Requirements  
- Ensure you have **Python 3.10 or higher** (check [compatibility](https://docs.couchbase.com/python-sdk/current/project-docs/compatibility.html#python-version-compat) with the Couchbase SDK).  
- A **Couchbase Capella account** ([Docs](https://docs.couchbase.com/cloud/get-started/intro.html)) **or** a local installation of **Couchbase Server** ([Download](https://www.couchbase.com/downloads)).  
- An **operational cluster** created in a project (Capella) or properly configured on your local machine (Couchbase Server).  
- Ensure proper access control:  
  - For **Couchbase Capella**, configure cluster access permissions and allowlisted IP addresses ([Docs](https://docs.couchbase.com/cloud/get-started/connect.html#prerequisites)).  
  - For **Couchbase Server**, set up appropriate user roles and permissions ([Docs](https://docs.couchbase.com/server/current/manage/manage-security/manage-users-and-roles.html)).  
- Obtain the **connection string** for **Couchbase Capella** or **Couchbase Server** by following the official guide: [Docs](https://docs.couchbase.com/python-sdk/current/hello-world/start-using-sdk.html#connect).  


### Installing Dependencies
To install the required dependencies, run:
```sh
pip install couchbase-streamlit-connector
```

## Getting Started  

Setting up the **Couchbase-Streamlit Connector** is straightforward. You can configure the connection using **Streamlit's Secrets Management (recommended for security)** or **by passing credentials directly** in your script.  

#### **Option 1: Using `secrets.toml` (Recommended)**  
For better security and maintainability, store your Couchbase credentials in `.streamlit/secrets.toml` at the root of your project.  

```toml
[connections.couchbase] # This can be of the form [connections.<ANY_NAME>]
CONNSTR = "<CONNECTION_STRING>"
USERNAME = "<CLUSTER_ACCESS_USERNAME>"
PASSWORD = "<CLUSTER_ACCESS_PASSWORD>"
BUCKET_NAME = "<BUCKET_NAME>"
SCOPE_NAME = "<SCOPE_NAME>"
COLLECTION_NAME = "<COLLECTION_NAME>"
```

Then, initialize the connection in your Streamlit app:  

```python
import streamlit as st
from couchbase_streamlit_connector.connector import CouchbaseConnector

connection = st.connection(
    "couchbase", # This should match the name you have given in the toml file in the [connections.<ANY_NAME>]. So you must put "<ANY_NAME>" here.
    type=CouchbaseConnector
)
st.help(connection)
```  

#### **Option 2: Passing Credentials Directly**  
If you prefer, you can provide the connection details directly in your script:  

```python
import streamlit as st
from couchbase_streamlit_connector.connector import CouchbaseConnector

connection = st.connection(
    "couchbase",
    type=CouchbaseConnector,
    CONNSTR="<CONNECTION_STRING>",
    USERNAME="<USERNAME>",
    PASSWORD="<PASSWORD>",
    BUCKET_NAME="<BUCKET_NAME>",
    SCOPE_NAME="<SCOPE_NAME>",
    COLLECTION_NAME="<COLLECTION_NAME>"
)
st.help(connection)
```  
**Verify the Connection**: To ensure that the connection is working correctly, the `st.help(connection)` line is added. If everything is set up correctly, this should display the connection object. Now, you're ready to start using Couchbase within your Streamlit application!  


## Usage  
Once the **Couchbase-Streamlit Connector** is set up, you can interact with your Couchbase database using simple functions for **CRUD (Create, Read, Update, Delete) operations** and **SQL++ queries**.  

### Performing CRUD Operations  
You can insert, retrieve, update, and delete documents in your Couchbase collection using the following methods.  
**NOTE**: Create, Read, Update, and Delete operations only work on the specific bucket, scope, and collection specified during connection setup.

#### **Insert a Document**  
To store a new document in the database:  
```python
connection.insert_document("222", {"key": "value"})
st.write("Inserted document with document id 222")
```  

#### **Retrieve a Document**  
To fetch a document by its key:  
```python
document = connection.get_document("222")
st.write("Retrieved document:", document)
```  

#### **Update (Replace) a Document**  
To update an existing document, use `replace_document()`:  
```python
connection.replace_document("222", {"new_key": "new_value"})
st.write("Updated document:", connection.get_document("222"))
```  

#### **Delete a Document**  
To remove a document from the database:  
```python
connection.remove_document("222")
st.write("Document with id 222 deleted successfully.")
```  

### Running Queries  
You can execute **SQL++ queries** to retrieve and analyze data. 
**NOTE**: Queries can work across any bucket, scope, and collection in the cluster, regardless of the connection settings.
For example, to fetch five records from the `airline` collection:  
```python
query = "SELECT * FROM `travel-sample`.`inventory`.`airline` LIMIT 5;"
result = connection.query(query)
st.write("Query result:", result)
```  

## Tutorials & Examples  
Now that you understand the basics of using the **Couchbase-Streamlit Connector**, you can explore practical implementations through the following tutorials:  
- **[Streamlit Quickstart Tutorial](https://github.com/couchbase-examples/streamlit-quickstart)** – A beginner-friendly guide that walks you through building a simple Streamlit application with Couchbase. This tutorial covers fundamental database interactions, including CRUD operations and queries.  
- **[Couchbase Connector Demo App](https://github.com/couchbase-examples/couchbase-tutorials/tree/main/tutorial/markdown/python/streamlit)** – A more advanced example demonstrating how to integrate Couchbase with a feature-rich Streamlit application. This tutorial showcases additional functionalities and best practices for building scalable applications.  

These examples will help you apply what you've learned and explore more advanced use cases for Couchbase within Streamlit.  


## Understanding `CouchbaseConnector`

The `CouchbaseConnector` class extends `BaseConnection` from Streamlit and serves as a custom connector for interacting with Couchbase. It facilitates database connections, collection management, CRUD operations, and query execution. The `BaseConnection` class is an **abstract base class (ABC)** that all Streamlit connection types must inherit from. It provides a framework for creating custom database connectors within Streamlit, ensuring standardization across different connection implementations. The core responsibility of `BaseConnection` is to handle connection initialization, caching, and secret management. This ensures that `CouchbaseConnector` follows Streamlit's connection framework while adding database-specific logic. By inheriting `BaseConnection`, the `CouchbaseConnector` class benefits from **automatic reconnection, secret updates, and standardized connection handling**.  

### 1. **Class Structure and Connection Initialization**
The class defines `_connect()`, which establishes a connection to a Couchbase cluster:  

```python
def _connect(self, **kwargs):
    connstr = kwargs.pop("CONNSTR", None) or self._secrets.get("CONNSTR", None)
    username = kwargs.pop("USERNAME", None) or self._secrets.get("USERNAME", None)
    password = kwargs.pop("PASSWORD", None) or self._secrets.get("PASSWORD", None)
    self.bucket_name = kwargs.pop("BUCKET_NAME", None) or self._secrets.get("BUCKET_NAME", None)
    self.scope_name = kwargs.pop("SCOPE_NAME", None) or self._secrets.get("SCOPE_NAME", None)
    self.collection_name = kwargs.pop("COLLECTION_NAME", None) or self._secrets.get("COLLECTION_NAME", None)
```

- This method must be implemented (as described in the abstract `BaseConnection` class).
- It retrieves the required connection details either from Streamlit secrets or keyword arguments.  
- Ensures all necessary parameters are provided before attempting a connection.  
- Uses `ClusterOptions` with `PasswordAuthenticator` to authenticate and establish a connection.  
- The method also includes exception handling for authentication, timeouts, and other Couchbase-specific errors.  

### 2. **Managing Buckets, Scopes, and Collections**
The class provides methods to handle collections dynamically:  

#### **Setting Bucket, Scope, and Collection**
```python
def set_bucket_scope_coll(self, bucket_name: str, scope_name: str = "_default", collection_name: str = "_default"):
    self.bucket_name = bucket_name
    self.scope_name = scope_name
    self.collection_name = collection_name
    self.bucket = self.cluster.bucket(bucket_name)
    self.scope = self.bucket.scope(scope_name)
    self.collection = self.scope.collection(collection_name)
```
- Dynamically updates the collection being used.  
- Should be used cautiously as it overrides the predefined configuration.  

#### **Retrieving Bucket, Scope, and Collection Details**
```python
def get_bucket_scope_coll(self):
    return {
        "bucket_name": self.bucket_name,
        "scope_name": self.scope_name,
        "collection_name": self.collection_name,
        "bucket": self.bucket,
        "scope": self.scope,
        "collection": self.collection
    }
```
- Returns the currently active bucket, scope, and collection details.  

### 3. **CRUD Operations**
These methods interact with documents stored within a Couchbase collection:  

#### **Insert a Document**
```python
def insert_document(self, doc_id: str, doc: JSONType, opts: InsertOptions = InsertOptions(timeout=timedelta(seconds=5)), **kwargs):
    return self.collection.insert(doc_id, doc, opts, **kwargs)
```
- Adds a new document to the collection with a specified ID.  
- Uses `InsertOptions` for timeout settings.  

#### **Retrieve a Document**
```python
def get_document(self, doc_id: str, opts: GetOptions = GetOptions(timeout=timedelta(seconds=5), with_expiry=False), **kwargs):
    result = self.collection.get(doc_id, opts, **kwargs)
    return result.content_as[dict]
```
- Fetches a document by ID and returns its content.  

#### **Replace an Existing Document**
```python
def replace_document(self, doc_id: str, doc: JSONType, opts: ReplaceOptions = ReplaceOptions(timeout=timedelta(seconds=5), durability=Durability.MAJORITY), **kwargs):
    return self.collection.replace(doc_id, doc, opts, **kwargs)
```
- Updates an existing document while ensuring durability.  

#### **Delete a Document**
```python
def remove_document(self, doc_id: str, opts: RemoveOptions = RemoveOptions(durability=ServerDurability(Durability.MAJORITY)), **kwargs):
    return self.collection.remove(doc_id, opts, **kwargs)
```
- Removes a document from the collection, using server-side durability settings.  

### 4. **Executing Queries**
```python
def query(self, q, opts=QueryOptions(metrics=True, scan_consistency=QueryScanConsistency.REQUEST_PLUS)):
    result = self.cluster.query(q, opts)
    return result
```
- Runs a SQL++ query on the Couchbase cluster.  
- Uses `QueryOptions` to ensure query consistency.  

### 5. **Error Handling**
The class includes exception handling for different scenarios:  
```python
except AuthenticationException as e:
    raise Exception(f"ERROR: Authentication failed!\n{e}")
except TimeoutException as e:
    raise Exception(f"ERROR: Connection timed out!\n{e}")
except CouchbaseException as e:
    raise Exception(f"ERROR: Couchbase-related issue occurred\n{e}")
except Exception as e:
    raise Exception(f"Unexpected Error occurred\n{e}")
```
- Ensures that meaningful error messages are displayed when an issue occurs.  


## Contributing  

We welcome contributions! Follow these steps to set up your development environment and contribute effectively.  

### Setting Up the Development Environment  
1. Fork the repository and clone your fork:  
```sh
git clone https://github.com/Couchbase-Ecosystem/couchbase-streamlit-connector
cd couchbase-streamlit-connector
```
2. Create a virtual environment and install dependencies:  
```sh
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

### Contribution Workflow  
- Follow GitHub’s [PR workflow](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).  
- Create a branch for each feature or bug fix:  
```sh
git checkout -b <feature-name>
```
- Open a PR to `main`. Merges to `production` trigger CI/CD, which builds, tests, and publishes the release.  

### Reporting Issues  
Open a GitHub issue with:  
- Problem description  
- Steps to reproduce  
- Expected behavior  

## Appendix
Here are some helpful resources for working with Couchbase and Streamlit:
### **Couchbase Documentation**
- [Couchbase Python SDK Compatibility](https://docs.couchbase.com/python-sdk/current/project-docs/compatibility.html#python-version-compat)  
- [Getting Started with Couchbase Capella](https://docs.couchbase.com/cloud/get-started/intro.html)  
- [Connecting to Couchbase Capella](https://docs.couchbase.com/cloud/get-started/connect.html#prerequisites)  
- [SQL++ Query Language Guide](https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/index.html)  
- [Couchbase SDKs Overview](https://docs.couchbase.com/home/sdk.html)  

### **Streamlit Documentation**
- [Streamlit Secrets Management](https://docs.streamlit.io/develop/concepts/connections/secrets-management)  
- [Using `st.connection`](https://docs.streamlit.io/develop/api-reference/connections)  
- [Streamlit Components](https://docs.streamlit.io/develop/api-reference)  
