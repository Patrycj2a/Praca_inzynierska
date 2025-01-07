# Projekt dyplomowy - Patrycja Lewicka

## Temat pracy: Detekcja, identyfikacja oraz estymacja pozycji chwytu obiektów w scenie ramienia robotycznego z zastosowaniem zaawansowanej sieci neuronowej YOLO


<p align="center">
  <img src="https://github.com/user-attachments/assets/bca1760c-0992-4122-80c1-342506b9dcce" alt="robot" width="300">
  <img src="https://github.com/user-attachments/assets/63537a03-5a56-48de-a1d0-b424f6fa782d" alt="image_1732551891" width="300">
</p>

## Cel pracy
Celem pracy jest opracowanie efektywnego systemu detekcji z zastosowaniem modelu sieci neuronowej YOLO, który będzie mógł wspierać automatyzację procesów manipulacji obiektów z udziałem ramienia robotycznego. System ten ma umożliwić detekcję oraz identyfikację obiektów różnych kształtów geometrycznych za pomocą kamery RGB, a następnie estymację pozycji obiektu na podstawie współrzędnych detekcji.
Dodatkowym celem jest porównanie kilku wersji pre-trenowanych modeli YOLO w celu zweryfikowania hipotezy, czy wybór nowszego modelu będzie oznaczać uzyskanie lepszych dla tego problemu efektów detekcji.

## Kluczowe elementy projektu

### Przygotowanie zbioru danych
- Opracowano autorski zbiór danych obejmujący:
  - **117 obrazów** z kamery przemysłowej Basler,
  - **117 obrazów po augmentacji**,
  - Łącznie **234 zdjęcia**.
- Zbiór uwzględnia różnorodne konfiguracje, kształty oraz liczby obiektów.

### Adaptacja i ocena modeli
- Przeprowadzono adaptację trzech **pre-trenowanych modeli YOLO (YOLOv5, YOLOv8, YOLOv10) od Ultralytics** przy użyciu autorskiego zbioru danych.

### Wdrożenie na kamerze i testy
- Modele YOLOv8 i YOLOv10 wdrożono na kamerze **Luxonis OAK-D Pro** z wbudowanymi jednostkami przetwarzania SI.
- Przeprowadzono testy w warunkach **oświetlenia naturalnego i sztucznego** na podstawie **30 próbek** dla każdego modelu.

### Estymacja pozycji 2D
- Zrealizowano prosty system **estymacji pozycji 2D** wykrytych obiektów przy wykorzystaniu współrzędnych detekcji, co stanowi bazę do dalszej integracji z systemami robotycznymi.

## Zawartość repozytorium (foldery)
- **camera_files**: Wyniki detekcji na kamerze Luxonis Oak-D Pro PoE oraz pliki konfiguracyjne, użyte do implementacji na sprzęcie.
- **dataset_creating**: Zawiera podfoldery z obrazami oraz etykietami przed i po dystorsji, po augumentacji oraz materiały do kalibracji.
- **datasets**: Końcowy zbiór danych użyty do trenowania modeli.
- **docker**: Obraz kontenera stworzonego do uruchomienia środowiska trenowania modeli.
- **scripts**: skrypty w języku Python użyte podczas przetwarzania obrazów i etykiet oraz trenowania modeli.
- **training_results**: Wyniki trenowania trzech modeli YOLO przed wdrożeniem na kamerze.
- **yolov5**: submoduł repozytorium ultralytics yolov5.

## Dane projektu
**Autor**: Patrycja Lewicka  
**Promotor**: dr inż. Anna Wójcicka  
Projekt powstawał we współpracy z Maciejem Aleksandrowiczem [@macmacal](https://macmacal.github.io/)  
**Kierunek**: Automatyka i Robotyka  
**Wydział**: Elektrotechniki, Automatyki, Informatyki i Inżynierii Biomedycznej  
**Uczelnia**: Akademia Górniczo-Hutnicza im. S. Staszica w Krakowie  
