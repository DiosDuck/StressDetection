Frontend:

Aplicatia cu interfata grafica pentru Android. Apesi pe "Record" pentru a incepe inregistrarea, "Stop" pentru a opri si "Send" pentru a trimite inregistrarea audio catre server. Sub butonul "Send" se va afisa propozitia spusa de catre utilizator, respectiv daca s-a detectat stres in voce

Aplicatia va inregistra audio-ul sub forma de fisier "PCM", apoi va fi convertita intr-un fisier "WAV" (nu se poate inregistra direct in "WAV", asa ca se va face o conversie manuala) inainte de a fi trimis prin API catre server.


Backend:

Serverul care primeste prin API de la client un fisier audio si va intoarce atat "Speech-to-text", cat si daca s-a detectat stres in voce

La partea de "Speech-to-text" se face cu ajutorul unor biblioteci, nu am adaugat nimic nou pe moment la el

La partea de detectare a stresului antrenez datele folosind (pe moment) fisierele audio din RAVDESS, extrag din ele MFCC, Chroma si Mel, fac scale pe date (pe moment folosind o librarie), si le antrenez cu MLPClassifier (o retea neuronala pe care o folosesc pe moment)

TODO:
1.Implementare retea neuronala
2.Implementare Scale (obligatoriu pentru retea neuronala)
3.Imbunatatire precizie (pe moment obtin 77-78%) prin modificarea atributelor retelei sau folosirea altor atribute audio