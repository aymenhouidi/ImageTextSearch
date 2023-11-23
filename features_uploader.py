from elasticsearch import Elasticsearch
import os
import numpy as np

es = Elasticsearch(["http://localhost:9200"])
# index = "image_features"
index = 'features'

def upload(image_name,image_path,features):
   
    doc = {
        "imageId":image_name,
        "featurevector": features.tolist(), 
        "imgUrl": image_path,
       
    }
    
    
    res = es.index(index=index, document=doc)
    print(res['result'], res['_id'])
# Assume you have a corresponding list of image IDs and URLs


# train_path='reduced_extracted_features/'
# images_path='images'
# categories=os.listdir(train_path)
# for category in categories:
#     category_path=os.path.join(train_path,category)
#     destination_category_path=os.path.join(images_path,category)
#     subcategories=os.listdir(category_path)
#     for subcategory in subcategories:
#         print(subcategory)
#         subcategory_path=os.path.join(category_path,subcategory)
#         destination_subcategory_path=os.path.join(destination_category_path,subcategory)
#         #os.makedirs(destination_subcategory_path)
#         items=os.listdir(subcategory_path)
#         if items[0].endswith('.npy'):
#             for item in items:
#                 np_path=os.path.join(subcategory_path,item)
#                 image_name=item.split('.')[0]+'.jpg'
#                 image_path=os.path.join(destination_subcategory_path,image_name)
#                 features=np.load(np_path)
#                 upload(image_name,image_path,features)
#         else:
#             for item in items:
#                 subsubcategory_path=os.path.join(subcategory_path,item)
#                 subsubcategories=os.listdir(subsubcategory_path)
#                 for subsubcategory in subsubcategories:
#                     np_path=os.path.join(subsubcategory_path,subsubcategory)
#                     image_name=item.split('.')[0]+'.jpg'
#                     image_path=os.path.join(destination_subcategory_path,image_name)
#                     features=np.load(np_path)
#                     upload(image_name,image_path,features)
                    
# for filename in os.listdir('0_reduced'):
#     image_name=filename.split('.')[0]+'.jpg'
#     image_path = os.path.join('0',image_name )
#     npy_path=os.path.join('0_reduced', filename)
#     features=np.load(npy_path)
#     upload(image_name,image_path,features)

for dirname in os.listdir('reduced_features'):
    dirpath=os.path.join('reduced_features', dirname)
    for filename in os.listdir(dirpath):
        image_name=filename.split('.')[0]+'.jpg'
        image_dir_path=('images',dirname)
        image_path = os.path.join(image_dir_path, image_name)
        npy_path=os.path.join(dirpath, filename)
        features=np.load(npy_path)
        upload(image_name,image_path,features)
        



