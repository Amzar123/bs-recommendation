# Description 
Repository ini digunakan untuk aplikasi backend sistem rekomendasi 

# How to run
Pastikan anda sudah menginstall docker dan docker compose.
Jalankan perintah berikut 
```
docker-compose -f docker-compose.yml up
```
Akses API dokumentasi  melalui `http://localhost:80/docs`

# Migrations Guidlines 
1. flask db init
2. flask db migrate -m "message"
3. flask db revision -am "message for name file"
4. flask db upgrade

# Run linters 
Analyze code
```
pylint src/controller/*.py
```

Auto fix error 
```
autopep8 --in-place --aggressive --aggressive *.py
```