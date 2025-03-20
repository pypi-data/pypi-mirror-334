# **MongoRex** 🦖  

MongoRex is a **powerful** and **easy-to-use** Python library that simplifies MongoDB operations. It provides a clean and reusable interface for **CRUD operations, indexing, aggregation, transactions, and database management tasks**.  

Whether you're building a **small app** or managing **large-scale databases**, MongoRex makes working with MongoDB **effortless**.  

---

## **🚀 Features**  

✅ **Simple CRUD Operations** – Easily create, read, update, and delete MongoDB documents.  
✅ **Index Management** – Efficiently create, drop, and list indexes to enhance performance.  
✅ **Aggregation Pipeline** – Perform advanced queries using MongoDB’s aggregation framework.  
✅ **Transaction Support** – Manage multi-document transactions for data integrity.  
✅ **Bulk Write Support** – Streamline operations with batch updates and inserts.  
✅ **Regex Search** – Perform advanced text-based searches with regex support.  
✅ **Get Latest Documents** – Fetch the most recent N documents quickly.  
✅ **Watch for Changes** – Monitor real-time updates in collections.  
✅ **Database & Collection Stats** – Get insights on storage, indexes, and performance.  
✅ **MapReduce Operations** – Execute powerful data transformations and aggregations.  
✅ **Connection Management** – Safely handle and close MongoDB connections.  

---

## **📦 Installation**  

Install MongoRex using **pip**:  

```bash
pip install MongoRex
```

Or, install from **GitHub** (latest version):  

```bash
pip install git+https://github.com/TraxDinosaur/MongoRex.git
```

---

## **🛠️ Quick Start**  

Here’s how you can **start using MongoRex** in your Python application:  

### **1. Initialize MongoRex**  

```python
from MongoRex import DataBase

# Replace with your MongoDB URI and database name
mongo = DataBase(DB_Name="your_database", MongoURI="mongodb://localhost:27017")
```

### **2. Basic CRUD Operations**  

#### **➕ Add a Document**  

```python
document = {"name": "Alice", "age": 30}
mongo.add_doc("users", document)
```

#### **🔍 Find a Document**  

```python
user = mongo.find_doc("users", {"name": "Alice"})
print(user)
```

#### **🔄 Update a Document**  

```python
mongo.update_doc("users", {"name": "Alice"}, {"age": 31})
```

#### **❌ Delete a Document**  

```python
mongo.delete_doc("users", {"name": "Alice"})
```

---

## **📚 Full API Reference**  

### **📝 CRUD Operations**  

| Method | Description |
|--------|-------------|
| `add_doc(collection, document)` | Insert a **single document** into a collection. |
| `add_docs(collection, documents)` | Insert **multiple documents** into a collection. |
| `find_doc(collection, query)` | Retrieve a **single document** matching the query. |
| `find_docs(collection, query, regex_fields=None)` | Retrieve **multiple documents** with optional regex search. |
| `update_doc(collection, filter_query, update_data)` | Update a **single document** matching the filter. |
| `update_docs(collection, filter_query, update_data)` | Update **multiple documents** matching the filter. |
| `update_field(collection, filter_query, field, value)` | Update a **single field** in a document. |
| `delete_doc(collection, query)` | Delete a **single document** matching the query. |
| `delete_docs(collection, query)` | Delete **multiple documents** matching the query. |
| `delete_all(collection)` | **Delete all** documents in a collection. |

---

### **📊 Aggregation & Querying**  

| Method | Description |
|--------|-------------|
| `aggregate(collection, pipeline)` | Perform **advanced aggregation** operations. |
| `get_latest(collection, limit=5, sort_field="_id")` | Fetch the **latest N documents** sorted by a field. |
| `distinct(collection, field, query=None)` | Retrieve **distinct values** for a specified field. |
| `map_reduce(collection, map_function, reduce_function, out)` | Perform **map-reduce** operations on data. |

---

### **⚡ Index Management**  

| Method | Description |
|--------|-------------|
| `create_index(collection, keys, **kwargs)` | Create an **index** for a collection. |
| `drop_index(collection, index_name)` | Drop an **existing index**. |
| `list_indexes(collection)` | List **all indexes** in a collection. |

---

### **📁 Database & Collection Management**  

| Method | Description |
|--------|-------------|
| `drop_collection(collection)` | Drop a **collection** from the database. |
| `list_collections()` | List **all collections** in the database. |
| `server_status()` | Retrieve **MongoDB server status**. |
| `db_stats()` | Get **database statistics**. |
| `collection_stats(collection)` | Retrieve **collection statistics**. |

---

### **🔄 Transactions & Bulk Operations**  

| Method | Description |
|--------|-------------|
| `start_session()` | Start a **MongoDB transaction session**. |
| `bulk_write(collection, operations)` | Perform **bulk write** operations. |

---

### **👀 Watch for Changes**  

| Method | Description |
|--------|-------------|
| `watch(collection=None, pipeline=None)` | **Monitor changes** in a collection or database. |

---

### **🔄 Advanced Document Operations**  

| Method | Description |
|--------|-------------|
| `replace_doc(collection, filter_query, replacement)` | **Replace** a document with a new one. |
| `rename_collection(old_name, new_name)` | **Rename** a collection. |

---

### **🔌 Connection Management**  

| Method | Description |
|--------|-------------|
| `close_connection()` | **Close** the MongoDB connection safely. |

---

## **⚙️ Requirements**  

- Python **3.6+**  
- `pymongo` library  

Install dependencies manually if needed:  

```bash
pip install pymongo
```

---

## **🛡️ License**  

MongoRex is licensed under the **CC-BY-SA 4.0** license. Feel free to **use, modify, and share** it, but **give appropriate credit**.  

---

## **🏆 Contributors**  

MongoRex is developed and maintained by **[TraxDinosaur](https://traxdinosaur.github.io)**.  

🚀 Contributions are welcome! Feel free to open an **issue** or submit a **pull request** on [GitHub](https://github.com/TraxDinosaur/MongoRex).  

---

## **🎯 Get Started Today!**  

MongoRex **simplifies MongoDB operations** so you can focus on building great applications.  

Start using **MongoRex** today and **enhance your database management experience!** 🚀  

📌 **GitHub Repository:** [MongoRex on GitHub](https://github.com/TraxDinosaur/MongoRex)  
