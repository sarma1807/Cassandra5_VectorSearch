###############
#!/usr/bin/env python

# imports
from sentence_transformers import SentenceTransformer
from PIL import Image

# model related files will be downloaded during first execution
# for image to vector : we will use clip-ViT-B-32 pre-trained model
model = SentenceTransformer("clip-ViT-B-32")

vector_embedding = model.encode(Image.open("sample_image.jpg"))

# vector embedding is an array of float values
print("type of vector embedding : " + str(type(vector_embedding)))
### output : <class 'numpy.ndarray'>

# vector embedding is an array of 512 float values
print("shape/size of vector embedding : " + str(vector_embedding.shape))
### output : (512,)

print("vector embedding :")
print(vector_embedding)

###############

