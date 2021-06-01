Frontend:

Aplicatia cu interfata grafica pentru Android. Apesi pe "Record" pentru a incepe inregistrarea, "Stop" pentru a opri si "Send" pentru a trimite inregistrarea audio catre server. Sub butonul "Send" se va afisa propozitia spusa de catre utilizator, respectiv daca s-a detectat stres in voce

Aplicatia va inregistra audio-ul sub forma de fisier "PCM", apoi va fi convertita intr-un fisier "WAV" (nu se poate inregistra direct in "WAV", asa ca se va face o conversie manuala) inainte de a fi trimis prin API catre server.

Aplicatia permite sa selectezi tipul de output: daca "Speech-to-text" se face in romana sau engleza, respectiv cum se va detecta stresul (daca vrem doar sa detectam stresul, sau sa afisam si emotia care este un posibil simptom al stresului)

Backend:

Serverul care primeste prin API de la client un fisier audio si va intoarce o lista de perechi continand "Speech-to-text" si detectia stresului in voce. Fisierul audio se imparte in mai multe chunk-uri, fiecare chunk reprezentand o propozitie, apoi pe acea propozitie se detecteaza stresul si se face "Speech-to-text"

La partea de "Speech-to-text" se face cu ajutorul SpeechRecognition, folosind google recognition.

La partea de detectare a stresului antrenez datele folosind fisierele audio din RAVDESS, SAVEE si TESS (in total fiind peste 3000 de fisiere audio), extrag din ele MFCC si Chroma (nu mai trebuie Mel), fac scale pe date creata de mine, si le antrenez cu Pytorch, o retea neuronala modelata de mine.

La Pytorch folosesc 4 straturi, stratul de intrare continand 64 de noduri (pentru fiecare input extras), cele intermediare folosesc 34 de noduri, trecerea de la un strat la altul se face cu o apelare de functie liniara, urmata de Relu, apoi stratul final contine 2 sau 4 noduri (depinzand de modul de afisare a stresului), in care trecerea se face cu o functie liniara, urmata de un softmax.


