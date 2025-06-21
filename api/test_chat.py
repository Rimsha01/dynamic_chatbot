
import requests

# Test upload
with open("test.txt", "w") as f:
    f.write("Python is a high-level programming language known for its simplicity and readability. It is widely used in web development, data science, artificial intelligence, and automation. Python supports multiple programming paradigms including object-oriented, procedural, and functional programming. Machine learning is a subset of artificial intelligence that enables computers to learn from data. Deep learning uses neural networks to solve complex problems.")

with open("test.txt", "rb") as f:
    files = {"data": ("test.txt", f, "text/plain")}
    data = {"file_name": "test.txt", "file_type": "text", "description": "Test"}
    response = requests.post("http://localhost:8000/upload/upload_data", files=files, data=data)
    print("Upload:", response.json())

# Test chat
response = requests.post("http://localhost:8000/chat?query=What is Python?")
print("Chat:", response.json())