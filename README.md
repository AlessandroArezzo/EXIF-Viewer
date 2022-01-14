# EXIF-Viewer

Il progetto consiste in una semplice applicazione Python che permette di visualizzare gli EXIF di immagini selezionate in input.<br>
L'elaborato è stato realizzato come Programming Assignment del corso di Human Computer Interaction previsto dal corso di Laurea Magistrale in Ingegneria Informatica dell'Università degli Studi di Firenze.

<h2>L'applicazione</h2>
Di seguito si riporta un esempio di schermata dell'applicazione.<br>
Come si nota, la vista consente innanzitutto di gestire una coda di immagini mostrata in basso tramite i pulsanti posti sulla destra, attraverso i quali è infatti possibile aggiungerne di nuove e
rimuovere solo quella selezionata oppure tutte quelle presenti.<br>
Selezionando un'immagine presente nella coda, questa viene mostrata nella sezione ad essa dedicata al centro della finestra, dove sulla sinistra è rappresentata
l'immagine stessa mentre sulla destra sono presenti gli EXIF e le sue info (nome del file, estensione, dimensione ecc.).<br>
Attraverso gli appositi pulsanti è anche possibile modificare la rappresentazione dell'immagine ruotandola in senso orario o antiorario.<br>
Inoltre se l'immagine è stata acquisita salvando i dati relativi alla geolocalizzazione, è possibile, premendo sull'apposito link
posto sotto ad essa, aprire la posizione in cui questa è stata scattata su Google Maps.

<br><br>
<div align="center">
    <img src="screen/exif_viewer_screen.png" width="800px"></img> 
</div>
<br><br>

<h2>Tecnologie utilizzate</h2>
L'elaborato è stato implementato in linguaggio Python utilizzando le librerie PyQt5 e PIL. 
Di queste due risulta molto importante la prima, attraverso la quale è stata definita l'interfaccia dell'applicazione.

</ul>
