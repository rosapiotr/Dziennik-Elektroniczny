# Dziennik-Elektroniczny
Aplikacja internetowa dziennik elektroniczny zaimplementowana w języku Python z wykorzystaniem frameworku Django i MySQL.

## Uruchomienie aplikacji
Aplikację można uruchomić lokalnie używając Dockera. Polecenie które należy wykonać znajdując się w katalogu głównym repozytorium to:
  sudo docker-compose up --build

Gdy aplikacja jest już uruchomiona należy wykonać polecenia:
```
  sudo docker ps
```
Następnie polecenie:
```
sudo docker exec -it <nazwa_kontenera_web> python manage.py makemigrations database
```
gdzie <nazwa_kontenera_web> należy zastąpić nazwą kontenera aplikacji internetowej, która została zwrócona w wyniku poprzedniego polecenia.

Kolejnym krokiem jest wykonaniu migracji:
```
sudo docker exec -it <nazwa_kontenera_web> python manage.py makemigrations database
sudo docker exec -it <nazwa_kontenera_web> python manage.py migrate database 0001
sudo docker exec -it <nazwa_kontenera_web> python manage.py makemigrations
sudo docker exec -it <nazwa_kontenera_web> python manage.py migrate
```
Ostatnim krokiem jest stworzenie konta administratora serwisu poleceniem:
```
sudo docker exec -it projekt_bazy_web_1 python manage.py createsuperuser
```


Aplikacja działa na porcie 8000. Po udaniu się pod adres localhost:8000 wyświetlona zostanie strona domowa portalu:
![Strona Domowa](/presentation_images/home_page.png)

Portal dla administratora znajduje się pod adresem localhost:8000/admin:
![Logowanie](/presentation_images/admin_login.png)
Do zalogowanie się należy użyć loginu i hasła podanych w trakcie tworzenia konta administratora. Widok po zalogowaniu:
![Admin](/presentation_images/admin_home.png)

Widok portalu dla uczniów:
![Ogłoszenia](/presentation_images/student_annotations.png)
![Plan ucznia](/presentation_images/student_plan.png)
![Oceny](/presentation_images/student_grades.png)
![Przedmioty](/presentation_images/student_subjects.png)
![Szczegóły przedmiotu](/presentation_images/student_subject.png)
![Znajdź nauczyciela](/presentation_images/student_find_teacher.png)
![Nauczyciel](/presentation_images/student_teacher.png)
![Profil](/presentation_images/student_manage_profile.png)


Widok portalu dla nauczycieli:
![Dodaj ogłoszenie](/presentation_images/teacher_annotation.png)
![Ogłoszenia](/presentation_images/teacher_annotations.png)
![Plan zajęć](/presentation_images/teacher_plan.png)
![Dodaj ocenę](/presentation_images/teacher_add_grade.png)
![profil](/presentation_images/teacher_manage_profile.png)
