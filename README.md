# Książka telefoniczna

Projekt wykonany przy pomocy FastAPI. Dokumentacja znajduje się pod adresem http://localhost:8000/redoc

Główne założenia:

-   Aplikacja obsługuje operacje CRUD.
-   Walidacja wprowadzanych danych - sprawdzanie poprawności maila oraz numeru telefonu.
-   Dane przechowywane są w bazie danych SQLite.
-   Jeden numer telefonu należy do jednej osoby. Każdy numer telefonu musi być unikalny. Jedna osoba może mieć więcej niż jeden numer.
-   **Testy z automatycznym przełączaniem się na testową bazę danych.** Po testach z bazy są usuwane wszystkie rekordy.

Główna część projektu rozbita jest na trzy pliki:

-   main.py - gdzie znajdują się wszystkie endpointy
-   models.py - definicje klas służących do interakcji z bazą danych. Klasa **Entry** to klasa dziedzicząca po klasie Base z SQLAlchemy. Reszta klas dziedziczy po BaseModel z Pydantic.
-   database.py - plik odpowiada za konfigurację i połączenie z bazą danych. W zależności od zmiennej środowiskowej TESTING używana jest baza phone_book lub test.

## Instalacja

Projekt był uruchamiany na Ubuntu 22.04 w Pythonie 3.10.6. Instalacja i uruchomienie projektu:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
``` 
Serwer zostanie uruchomiony na localhost:8000.


