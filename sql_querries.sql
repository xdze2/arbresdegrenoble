
-- Liste les (genre, espece, variete)

SELECT count(*) AS c, genre_bota, espece, variete FROM arbres
GROUP BY genre_bota, espece, variete
ORDER BY genre_bota
