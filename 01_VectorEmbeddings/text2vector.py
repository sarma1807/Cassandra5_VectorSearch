###############
#!/usr/bin/env python

# imports
from sentence_transformers import SentenceTransformer

# model related files will be downloaded during first execution
# for text to vector : we will use all-MiniLM-L6-v2 pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# model by default works on first 256 chars of input text
print("max text length :", model.max_seq_length)
### output : max text length : 256

# max_seq_length can be adjusted
model.max_seq_length = 100

myText1 = "I Love PlayStation"
myText2 = "we like cars"

vector_embedding1 = model.encode(myText1)
vector_embedding2 = model.encode(myText2)

# vector embedding is an array of float values
print(type(vector_embedding1))
### output : <class 'numpy.ndarray'>

# vector embedding is an array of 384 float values
print(vector_embedding1.shape)
### output : (384,)

print(vector_embedding1)


# vector similarity check
similarity1 = model.similarity(vector_embedding1, vector_embedding2)
similarity2 = model.similarity(vector_embedding1, vector_embedding1)
# aka Semantic Textual Similarity (STS)


# 33% similar
print(similarity1)
### output : tensor([[0.3320]])

# 100% similar
print(similarity2)
### output : tensor([[1.0000]])

###############

