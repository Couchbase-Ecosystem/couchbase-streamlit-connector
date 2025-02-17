import streamlit as st

# Title
st.title("Couchbase Connector for Streamlit")

st.header("1. Introduction")
st.write("This project is about creating an SDK in Streamlit for Couchbase, "
            "making it easy for developers using Streamlit to interact with Couchbase databases seamlessly.")
st.write("The goal of this project is to help developers work easily with Couchbase in Streamlit, "
            "allowing them to fetch, insert, update, and delete data with minimal effort.")
st.write("It eliminates the inconvenience of switching between Streamlit and the Couchbase Python SDK ecosystems, "
            "providing a more streamlined development experience.")
st.write("For a working demo please checkout `src/Demo.py` file. You can run it by the command")
st.code("""
git clone https://github.com/Couchbase-Ecosystem/couchbase_streamlit_connector.git
cd ./couchbase_streamlit_connector
pip install -r requirements.txt
pip install plotly geopy numpy
streamlit run src/Demo.py
""", language="bash")

st.header("2. Prerequisites")
st.subheader("System Requirements")
st.write("- Couchbase Capella account [Docs](https://docs.couchbase.com/cloud/get-started/intro.html)")
st.write("- Operational cluster created in a project")
st.write("- Cluster access permissions and allowed IP address configured [Docs](https://docs.couchbase.com/cloud/get-started/connect.html#prerequisites)")
st.write("- Connection string obtained from Couchbase Capella")

st.subheader("Installing Dependencies")
st.code("pip install couchbase streamlit")

st.header("3. Usage Guide")

st.subheader("Initializing the Connector")
st.write("You can configure the Couchbase connection using two approaches: storing credentials in a secrets file or passing them directly via arguments.")

st.write("**Option 1: Using `secrets.toml` (Recommended)**")
st.write("For security and convenience, store credentials in a `.streamlit/secrets.toml` file in your project's root directory [[Streamlit Secrets management]](https://docs.streamlit.io/develop/concepts/connections/secrets-management):")
st.code("""
[connections.couchbase]
CONNSTR = "<CONNECTION_STRING>"
USERNAME = "<CLUSTER_ACCESS_USERNAME>"
PASSWORD = "<CLUSTER_ACCESS_PASSWORD>"
BUCKET_NAME = "<BUCKET_NAME>"
SCOPE_NAME = "<SCOPE_NAME>"
COLLECTION_NAME = "<COLLECTION_NAME>"
""", language="toml")

st.write("Then, initialize the connection in your Streamlit app:")
st.code("""
import streamlit as st
from couchbase_streamlit_connector.connector import CouchbaseConnector

connection = st.connection(
    "couchbase",
    type=CouchbaseConnector
)
st.help(connection)
""", language="python")

st.write("**Option 2: Passing Credentials Directly (Alternative)**")
st.write("You can also pass the connection details directly as keyword arguments:")
st.code("""
import streamlit as st
from couchbase_streamlit_connector.connector import CouchbaseConnector

st.connection(
    "couchbase", 
    type=CouchbaseConnector, 
    CONNSTR=<CONNSTR>, 
    USERNAME=<USERNAME>, 
    PASSWORD=<PASSWORD>, 
    BUCKET_NAME=<BUCKET_NAME>, 
    SCOPE_NAME=<SCOPE_NAME>, 
    COLLECTION_NAME=<COLLECTION_NAME>
)
st.help(connection)
""", language="python")


import streamlit as st

st.subheader("Performing CRUD Operations")
st.write("Insert a Document")
st.code("""
connection.insert_document("222", {"key": "value"})
st.write(connection.get_document("222"))
""", language="python")

st.write("Fetch a Document")
st.code("""
st.write(connection.get_document("111"))
""", language="python")

st.write("Replace a Document")
st.code("""
connection.replace_document("222", {"new_key": "new_value"})
st.write(connection.get_document("222"))
""", language="python")

st.write("Delete a Document")
st.code("""
connection.remove_document("222")
st.write("Document 222 deleted")
""", language="python")

st.write("Run a Query")
st.code("""
result = connection.query("SELECT * FROM `travel-sample`.`inventory`.`airline` LIMIT 5;")
st.write(result)
""", language="python")
