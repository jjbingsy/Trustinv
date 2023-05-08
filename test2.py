from trustmod.classes   import GuruFilm, JavFilm, MissFilm, Idol

ff = GuruFilm(name="SSIS-715")
print (ff.description, ff.film_link)
for f in ff.idols:
    print (f.name)