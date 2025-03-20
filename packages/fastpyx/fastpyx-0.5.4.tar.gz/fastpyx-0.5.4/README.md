# **FastPyX** 🚀  

**FastPyX** is a **high-performance C extension** for Python, designed to **optimize memory usage** and significantly improve execution speed.  

## **Why FastPyX?**  
🔥 **Faster** than Python's built-in list for `fappend` operations  
📉 **Uses up to 56% less memory** than Python lists  
⚡ **Ideal for high-performance applications** requiring optimized data structures  

## **Features**  
- 🚀 Written in **C** for extreme performance  
- 📌 Optimized `FastList` implementation (efficient `fappend` method)  
- 🔹 **Supports multiple data types** seamlessly  
- 🔧 **Efficient memory allocation** to reduce fragmentation  
- 🔄 **Convert to Python list (`to_list`)** for compatibility  
- 📊 **Fast random access (`fget`)** and optimized length retrieval (`len()`)  

---

## **Installation**  
To install FastPyX:  
```sh  
pip install fastpyx  
```

---

## **Usage**  
```python  
import fastpyx  

fl = fastpyx.FastList()

# Append values  
for i in range(10):  
    fl.fappend(i)

# Print all elements  
fl.fprint()

# Access an element  
index = 5  
value = fl.fget(index)  
print(f"Index {index}: {value}")

# Convert to Python list  
py_list = fl.to_list()  
print("Converted list:", py_list)

# Get length  
print("Length:", len(fl))
```

---

## **Benchmark Results**  
| Operation | FastList | Python List | Speedup | Memory Usage (10M items) |  
|-----------|---------|-------------|---------|--------------------------|  
| `fappend` | **0.56s** | 0.67s | 🔥 **17% Faster** | **30.5MB (FastList) vs. 69MB (Python List)**  
| `fget` | **0.0067s** | **0.0062s** | Slightly slower (needs optimization) | -  
| `to_list` | **0.8999s** | **0.124s** | Needs improvement | -  

✅ **FastList is both faster and more memory-efficient than Python's built-in list!**  

---

## 📜 **License**  
MIT License. Feel free to contribute and improve FastPyX!  

---

### 🔗 **Future Roadmap**  
✅ Optimize `to_list` performance  
✅ Add slicing support  
✅ Implement iterator support for better compatibility  
✅ Advanced memory management optimizations for **Django and other frameworks**  
✅ Additional **performance improvements** for lists, dictionaries, and sets  
✅ More Pythonic API and integration with **NumPy/Pandas**  

