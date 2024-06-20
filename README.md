# End Point Model Machine Learning | Fast API |

# Hirarki Proyek
### project-root/
### ├── models/ # File untuk menyimpan model
###     ├── category_model.h5
###     ├── environment_model.h5
### │   └── scenery_model.h5 # Model .h5 yang digunakan untuk klasifikasi gambar
### ├── .env # File untuk menyimpan apiKey
### ├── .gitignore # File untuk menentukan file/direktori yang harus diabaikan oleh Git 
### ├── main.py # File kode utama untuk aplikasi FastAPI
### ├──  requirements.txt #  File untuk menyimpan semua dependensi yang digunakan
### └── serviceAccount.json # File untuk menyimpan kredensial Firebase

# Memulai Proyek :
1. Untuk menjalankan proyek ini di dalam lingkungan virtual (virtual environment) yang bernama myenv, kamu perlu mengikuti langkah-langkah berikut:
    Membuat Virtual Environment:
    Buat lingkungan virtual baru bernama myenv (jika belum ada):
    #
        python -m venv myenv
2. Aktivasi Virtual Environment lingkungan virtual yang sudah dibuat:
    ### Di Windows:
        myenv\Scripts\activate
    ### Di macOS/Linux:
        source myenv/bin/activate
3. Menginstal semua Dependencies library yang diperlukan di dalam myenv:
    #
        pip install fastapi uvicorn tensorflow requests pillow numpy python-dotenv google-cloud-firestore
4. Membuat dan Menjalankan Script: Buat file Python (main.py)
5. Menjalankan FastAPI Server menggunakan uvicorn:
    #
        uvicorn main:app --reload
        uvicorn main:app --host 0.0.0.0 --port 8080
6. Setelah langkah-langkah ini selesai, kamu bisa mengakses endpoint http://127.0.0.1:8000/classify_image/ untuk mengirimkan request POST dengan name dan mendapatkan hasil klasifikasi.
    ### body request
    <img width="944" alt="Postman" src="https://github.com/B4gasAhmad/Capstone/assets/116440854/95a5b32b-07c1-479c-9d20-2c81523ad92f">
        
    ### body respone
        {
            "id": "2e2adaf4190d4fbca748e",
            "name": "Pantai Kuta",
            "photoURL": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=AUc7tXV66w-jkkriOrf5XN0EBcjZvsCUeoKpOMyHPPik_iagI_KA-1yBJwXWsmeVjcBIgChI1vlnIAbX57pMwHxN11qZQxJDVY9nfqRXpgkTrErTGbkIyjGauf9aMLeSipo6n56oRaUjK1JrID5ieN204AHG-uthcQBHySEBnvgjViQ4Z-cD&key=ApiKey",
            "description": "Pantai Kuta, Kec. Kuta, Kabupaten Badung, Bali, Indonesia",
            "rating": 4.5,
            "lat": -8.7184926,
            "lon": 115.1686322,
            "scenery_classes": "Nature",
            "environment_classes": "Water",
            "category_classes": "Greenery"
        }
