from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import requests
from PIL import Image
import io
import numpy as np
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Load your .h5 models
scenery_model = tf.keras.models.load_model('models/scenery_model.h5')
environment_model = tf.keras.models.load_model('models/environment_model.h5')
category_model = tf.keras.models.load_model('models/category_model.h5')

# Function to get place details and image URL from Google Places API
def get_place_details(place_name):
    api_key = os.getenv("GOOGLE_API_KEY")
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=photos,formatted_address,name,rating,geometry&key={api_key}"
    
    response = requests.get(search_url)
    response_json = response.json()
    
    if 'candidates' in response_json and len(response_json['candidates']) > 0:
        candidate = response_json['candidates'][0]
        photo_reference = candidate['photos'][0]['photo_reference'] if 'photos' in candidate else None
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}" if photo_reference else None
        place_details = {
            "name": candidate['name'],
            "image_url": photo_url,
            "description": candidate.get('formatted_address', 'No description available'),
            "rating": candidate.get('rating', 'No rating available'),
            "latitude": candidate['geometry']['location']['lat'],
            "longitude": candidate['geometry']['location']['lng']
        }
        return place_details
    else:
        raise HTTPException(status_code=404, detail="Place not found or no photos available")

# Define your image preprocessing function
def preprocess_image(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))
    image = image.resize((224, 224))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = np.expand_dims(image_array, 0)
    preprocessed_image = image_array / 255.0
    return preprocessed_image

# Function to classify image using the loaded models
def classify_image(image_url):
    processed_image = preprocess_image(image_url)
    
    scenery_prediction = scenery_model.predict(processed_image)
    environment_prediction = environment_model.predict(processed_image)
    category_prediction = category_model.predict(processed_image)
    
    scenery_classes = ['Nature', 'Urban']
    environment_classes = ['Land', 'Water']
    category_classes = ['Attraction', 'Greenery', 'Historical']
    
    scenery_label = scenery_classes[np.argmax(scenery_prediction)]
    environment_label = environment_classes[np.argmax(environment_prediction)]
    category_label = category_classes[np.argmax(category_prediction)]
    
    return {
        "scenery_classes": scenery_label,
        "environment_classes": environment_label,
        "category_classes": category_label
    }

# Define API endpoint to classify images
@app.post("/classify_image/")
def classify_image_endpoint(name: str = Form(...)):
    try:
        place_details = get_place_details(name)
        predicted_class = classify_image(place_details["image_url"])
        response_body = {
            "id": "some_id",
            "name": place_details["name"][:21],
            "photoURL": place_details["image_url"],
            "description": place_details["description"],
            "rating": place_details["rating"],
            "lat": place_details["latitude"],
            "lon": place_details["longitude"],
            **predicted_class
        }
        doc_ref = db.collection('wisata').document()
        response_body["id"] = doc_ref.id
        doc_ref.set(response_body)
        return response_body
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)