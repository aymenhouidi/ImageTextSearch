from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
from IPython.display import display
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import numpy as np
from tensorflow.keras.models import Model
from elasticsearch import Elasticsearch
from joblib import load
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()
origins = ["http://localhost:3000"]  # Replace with the origin of your React app

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
es = Elasticsearch(["http://localhost:9200"])
base_model = VGG16(weights='imagenet', include_top=True)
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
pca = load('best_pca_model.pkl')

def reduce_features(file):
                
    if file.ndim == 1:
        file = file.reshape(1, -1)
    reduced_features = pca.transform(file)
    return reduced_features[0]

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # VGG16 input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

                # Extract features using the VGG16 model
    features = model.predict(img_array)[0]

    return reduce_features(features / np.linalg.norm(features))

UPLOAD_DIR = "uploads"


@app.post('/imagesearch')
async def root(image_path:str= Form(...)):
    try:
            features=extract_features(image_path)
            # Construct an Elasticsearch query
            search_query = {
                "query": {
                    "elastiknn_nearest_neighbors": {
                        "field": "featurevector",
                        "vec": {
                            "values": features,
                            "dims": 795
                        },
                        "similarity": "l2",  
                        "model": "exact",
                        "candidates": 100
                    }
                }
            }

            # Search for the nearest neighbors in the index
            index_name = 'features'  # Replace with your actual index name
            response = es.search(index=index_name, body=search_query)
            # Print out the results
            urls=list(element['_source']['imgUrl'].replace('\\','/') for element in response['hits']['hits'])
    
            return JSONResponse(content=urls)
    except Exception as e:
        return JSONResponse(content={"error": f"Error processing image: {str(e)}"}, status_code=500)
# @app.post('/textsearchs')
# async def root(text:str= Form(...)):
#         text=str(text)
#         search_query = {
    
#                 "query": {
#                     "match": {
#                     "tags": text
#                     }
#                 }

#                 }

#             # Search for the nearest neighbors in the index
#         index_name = 'features'  # Replace with your actual index name
#         response = es.search(index=index_name, body=search_query)
#             # Print out the results
#         urls=list(element['_source']['imgUrl'].replaFce('\\','/') for element in response['hits']['hits'])
    
#         return JSONResponse(content=urls)
    
@app.post('/textsearch')
async def textsearch(text:str= Form(...)):
    try:
            
            search_query = {
                    
                "query": {
                    "multi_match": {
                        "query": text,  
                        "fields": ["tags^2", "another_field"],
                        "type": "cross_fields",
                        "operator": "or",
                        "minimum_should_match": "75%",  
                        "tie_breaker": 0.3,
                       
                    }

                }}
            # search_query = {
    
            #     "query": {
            #         "match": {
            #         "tags": 'man'
            #         }
            #     }

            #     }

            # Search for the nearest neighbors in the index
            index_name = 'features'  # Replace with your actual index name
            response = es.search(index=index_name, body=search_query)
            # Print out the results
            urls=list(element['_source']['imgUrl'].replace('\\','/') for element in response['hits']['hits'])
    
            return JSONResponse(content=urls)
    except Exception as e:
        return JSONResponse(content={"error": f"Error processing image: {str(e)}"}, status_code=500)

@app.post('/imagetextsearch')
async def root(image_path:str= Form(...),text:str= Form(...)):
    try:
            features=extract_features(image_path)
            # Construct an Elasticsearch query
            search_query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "elastiknn_nearest_neighbors": {
                                    "field": "featurevector",
                                    "vec": {
                                        "values": features,
                                        "dims": 795
                                    },
                                    "similarity": "l2",  
                                    "model": "exact",
                                    "candidates": 100
                                }
                            },
                            {
                                "match": {
                                    "tags": text 
                                }
                            }
                        ]
                    }
                },
                
            }


            # Search for the nearest neighbors in the index
            index_name = 'features'  # Replace with your actual index name
            response = es.search(index=index_name, body=search_query)
            # Print out the results
            urls=list(element['_source']['imgUrl'].replace('\\','/') for element in response['hits']['hits'])
    
            return JSONResponse(content=urls)
    except Exception as e:
        return JSONResponse(content={"error": f"Error processing image: {str(e)}"}, status_code=500)
    
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Create the uploads directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save the uploaded file
    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as image_file:
        shutil.copyfileobj(file.file, image_file)
    
    return {"message": "File uploaded successfully"}
    
if __name__ == "__main__":
    uvicorn.run(app=app  , host="0.0.0.0")