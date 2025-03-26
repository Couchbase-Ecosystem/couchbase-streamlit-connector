from datetime import timedelta
from streamlit.connections import BaseConnection
from couchbase._utils import JSONType
# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ReplaceOptions, InsertOptions, RemoveOptions, GetOptions, QueryOptions)
from couchbase.logic.n1ql import QueryScanConsistency
from couchbase.durability import Durability, ServerDurability
from couchbase.exceptions import CouchbaseException, AuthenticationException, TimeoutException
import pandas as pd

class CouchbaseConnector(BaseConnection[Cluster]):    
    """
    The connector class for performing common Couchbase operations such as insert, get, replace, and remove documents.
        
    Example:
        If, the environment variables are set and contain the needed connstr, username, password, bucket, scope and collection
        ```
        import streamlit as st
        connection = st.connection("couchbase", type=CouchbaseConnection)
        st.help(connection)
        ```
        Else, you can also input them through kwargs.
        ```
        import streamlit as st
        connection = st.connection("couchbase", type=CouchbaseConnection, CONNSTR=<CONNSTR>, USERNAME=<USERNAME>, PASSWORD=<PASSWORD>, BUCKET_NAME=<BUCKET_NAME>, SCOPE_NAME=<SCOPE_NAME>, COLLECTION_NAME=<COLLECTION_NAME>)
        st.help(connection)
        ```
    """
    
    def _connect(self, **kwargs):
        """
        Establishes a connection to the Couchbase cluster and sets up the cluster object. Is called by the `streamlit.connection()`.          
        """
        self.cluster = None
        self.bucket = None
        self.scope = None
        self.collection = None
        self.bucket_name: str = None
        self.scope_name: str = None
        self.collection_name: str = None
        
        connstr = kwargs.pop("CONNSTR", None) or self._secrets.get("CONNSTR", None)
        username = kwargs.pop("USERNAME", None) or self._secrets.get("USERNAME", None)
        password = kwargs.pop("PASSWORD", None) or self._secrets.get("PASSWORD", None)
        self.bucket_name: str = kwargs.pop("BUCKET_NAME", None) or self._secrets.get("BUCKET_NAME", None)
        self.scope_name: str = kwargs.pop("SCOPE_NAME", None) or self._secrets.get("SCOPE_NAME", None)
        self.collection_name: str = kwargs.pop("COLLECTION_NAME", None) or self._secrets.get("COLLECTION_NAME", None)
                
        if not all([connstr, username, password, self.bucket_name, self.scope_name, self.collection_name]):
            missing_vars = []
            if not connstr:
                missing_vars.append("CONNSTR")
            if not username:
                missing_vars.append("USERNAME")
            if not password:
                missing_vars.append("PASSWORD")
            if not self.bucket_name:
                missing_vars.append("BUCKET_NAME")
            if not self.scope_name:
                missing_vars.append("SCOPE_NAME")
            if not self.collection_name:
                missing_vars.append("COLLECTION_NAME")
            raise ValueError(f"Missing required configuration variables: {', '.join(missing_vars)}")
                
        try:
            options = ClusterOptions(PasswordAuthenticator(username, password))
            options.apply_profile('wan_development')
            self.cluster = Cluster(connstr, options) # making connection to the cluster
            self.cluster.wait_until_ready(timedelta(seconds=5))
            self.set_bucket_scope_coll(self.bucket_name, self.scope_name, self.collection_name)
            
        except AuthenticationException as e:
            raise Exception(f"ERROR: Authentication failed!\n{e}")
        except TimeoutException as e:
            raise Exception(f"ERROR: Connection timed out!\n{e}")
        except CouchbaseException as e:
            raise Exception(f"ERROR: Couchbase-related issue occurred\n{e}")
        except Exception as e:
            raise Exception(f"Unexpected Error occured\n{e}")
         
    def set_bucket_scope_coll(self, bucket_name: str, scope_name: str = "_default", collection_name: str = "_default"):
        """
        [WARNING] Only use this function if you're sure that you NEED to change the collection. This will make the collection different from the one mentioned in the secrets file and that could potentially cause problems
        
        Set or change the Couchbase bucket, scope, and collection.

        Args:
            bucket_name (str): The name of the bucket to connect to.
            scope_name (str): The name of the scope within the bucket. Default is "_default".
            collection_name (str): The name of the collection within the scope. Default is "_default".

        Example:
        ```
        connection.set_bucket_scope_coll("new_bucket", "new_scope", "new_collection")
        print(connection.get_bucket_scope_coll())
        ```
        """
        try:
            # Store names for reference
            self.bucket_name = bucket_name
            self.scope_name = scope_name
            self.collection_name = collection_name
            
            self.bucket = self.cluster.bucket(bucket_name)
            self.scope = self.bucket.scope(scope_name)
            self.collection = self.scope.collection(collection_name)
            
        except CouchbaseException as e:
            raise Exception(f"ERROR: Failed to set collection {bucket_name}.{scope_name}.{collection_name}\n{e}")
            
    def get_bucket_scope_coll(self):
        """
        Return the currently set Couchbase bucket, scope, and collection.

        Returns:
            dict: A dictionary containing the bucket, scope, and collection names and objects.

        Example:
        ```
        collection_info = connection.get_bucket_scope_coll()
        print(collection_info)
        ```
        """
        return {
            "bucket_name": self.bucket_name,
            "scope_name": self.scope_name,
            "collection_name": self.collection_name,
            "bucket": self.bucket,
            "scope": self.scope,
            "collection": self.collection
        }
    
    # Create    
    def insert_document(self, doc_id: str, doc: JSONType, opts: InsertOptions = InsertOptions(timeout=timedelta(seconds=5)), **kwargs):
        """
        Insert a new document into the selected Couchbase collection. Works on collection level

        Args:
            doc_id (str): The unique ID of the document.
            doc (JSONType): The document to insert. Can be any JSON-compatible type.
            opts (InsertOptions): Options for the insert operation. Default includes timeout and durability settings.
            **kwargs: Additional keyword arguments passed to the `insert` method.

        Returns:
            Result: The result of the insert operation.

        Example:
        ```
        doc = {"name": "John", "age": 30}
        connection.insert_document("<DOC_ID>", doc)
        ```
    """
        try:
            return self.collection.insert(doc_id, doc, opts, **kwargs)
        except Exception as e:
            raise Exception(f"ERROR: Failed to insert document with ID '{doc_id}'\n{e}")
        
    # Read
    def get_document(self, doc_id: str, opts: GetOptions = GetOptions(timeout=timedelta(seconds=5), with_expiry=False), **kwargs):
        """
        Retrieve a document from Couchbase using the provided document ID and options. Works on collection level.

        Args:
            doc_id (str): The ID of the document to retrieve.
            opts (GetOptions): Options for the get operation, defaulting to timeout of 5 seconds and with_expiry set to False.
            **kwargs: Additional keyword arguments passed to the `get` method.

        Returns:
            dict: The retrieved document as a dictionary.

        Example:
        ```
        doc = connection.get_document("<DOC_ID>")
        ```
        """
        try:
            # Perform the get operation with the provided options
            result = self.collection.get(doc_id, opts, **kwargs)
            return result.content_as[dict]
        except Exception as e:
            raise Exception(f"ERROR: Failed to retrieve document with ID '{doc_id}'\n{e}")
    
    # Update
    def replace_document(self, doc_id: str, doc: JSONType, opts: ReplaceOptions = ReplaceOptions(timeout=timedelta(seconds=5), durability=Durability.MAJORITY), **kwargs):
        """
        Replace an existing document in the Couchbase collection. Works on the collection level.

        Args:
            doc_id (str): The ID of the document to replace.
            doc (dict): The new document to replace the existing one.
            opts (ReplaceOptions): Options for the replace operation, with default timeout and durability settings.
            **kwargs: Additional keyword arguments passed to the `replace` method.

        Returns:
            Result: The result of the replace operation.

        Example:
        ```
        updated_doc = {"name": "John", "age": 31}
        connection.replace_document("<DOC_ID>", updated_doc)
        ```
        """
        try:
            # Perform the replace operation with the provided options
            result = self.collection.replace(doc_id, doc, opts, **kwargs)
            return result
        except Exception as e:
            raise Exception(f"ERROR: Failed to replace document with ID '{doc_id}'\n{e}")
    
    # Delete
    def remove_document(self, doc_id: str, opts: RemoveOptions = RemoveOptions(durability=ServerDurability(Durability.MAJORITY)), **kwargs):
        """
        Remove a document from Couchbase using the provided document ID and options. Works on the collection level.

        Args:
            doc_id (str): The ID of the document to remove.
            opts (RemoveOptions): Options for the remove operation, defaulting to durability settings.
            **kwargs: Additional keyword arguments passed to the `remove` method.

        Returns:
            Result: The result of the remove operation.

        Example:
        ```
        connection.remove_document("user:123")
        ```
        """
        try:
            # Perform the remove operation with the provided options
            result = self.collection.remove(doc_id, opts, **kwargs)
            return result
        except Exception as e:
            raise Exception(f"ERROR: Failed to remove document with ID '{doc_id}'\n{e}")

    # Query
    def query(self, q, opts=QueryOptions(metrics=True, scan_consistency=QueryScanConsistency.REQUEST_PLUS), **kwargs):
        """
        Execute a SQL++ query against the Couchbase cluster. Works on the cluster level.
        
        Args:
            q (str): The N1QL query to execute.
            opts (QueryOptions): Options for the query operation, defaulting to metrics and request plus scan consistency.
            **kwargs: Additional keyword arguments passed to the `query` method.
        
        Returns:
            Result: The result of the query operation.
            
        Example:
        ```
        query = "SELECT * FROM `travel-sample` LIMIT 10"
        result = connection.query(query)
        output = [ row for row in result.rows() ]
        ```
        """
        try:
            result = self.cluster.query(q, opts, **kwargs)
            return result
        except Exception as ex:
            raise Exception(f"ERROR: Couchbase encountered an error\n{ex}")