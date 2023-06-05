from trustmod.classes import MissFilm as MissFilm_msl, GuruFilm, JavFilm

film = "IPX-842"


guru = GuruFilm(name=film, force=True   )
print (guru.description, guru.film_link, guru.series_link, guru.series_name)
# miss = MissFilm_msl(film, force=True)
# jav = JavFilm(name=film, force=True)

# print (miss.description, miss.film_link)
# print (jav.description, jav.film_link)

# for idol in jav.idols:
#     print (idol.name, idol.link)