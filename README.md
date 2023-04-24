# the-movies

Generar imágen
```
docker build -t movies:v1 .
```

Correr contenedor
```
docker run -p 5000:5000 the-movies:v1
```


post localhost:5000/movies 
body 
```
{
    "movie":"Titanic"
}
```

Recomendará 15 películas con báse en la enviada en el post