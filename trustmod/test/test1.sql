create temp view if not exists solo_cast_films (film, shared_key, idol) as select distinct fi.film_name, i.shared_key, i.name from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having count(distinct i.shared_key) = 1; 
--maybe but count is only for solo films and not the total number of films that idol has been in
select shared_key, count(film) cnt from solo_cast_films group by shared_key order by cnt desc;
