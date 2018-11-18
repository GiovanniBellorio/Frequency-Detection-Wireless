# Frequency Detection Wireless ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

[Frequency Detection Wireless](https://github.com/SfideDiProgrammazioneUniVR/PortafoglioVoti/issues/4) è un'applicazione per la rilevazione delle presenze all'interno di un'aula attraverso la connessione wifi. Verrà effettuata un'associazione univoca tra l'utente e l'indirizzo `MAC` del proprio dispositivo per registrare la presenza una volta rilevato in prossimità del master del sistema.

## Indice

* [Progetto](#Progetto)
  * [Web App](#Web-App)
    * [Flask](#Flask)
      * [Gestione delle Sessioni Cache Cookie](#Gestione-delle-Sessioni-Cache-Cookie)
    * [CouchDb](#CouchDb)
    * [Template Grafico](#Template-Grafico)
    * [Deploy Applicazione Python](#Deploy-Applicazione-Python)
  * [Wireless Detection App](#Wireless-Detection-App)
  * [Documentazione](#Documentazione)
* [Autori](#Autori)
* [Licenza](#Licenza)

## Progetto

Il progetto si basa su una `Web App` e su un applicazione che cattura la presenza nella rete del `Mac adress` del dispositivo. L'admin dopo aver eseguito l'associazione utente:mac fisicamente alla prima connessione, avvia l'applicazione di rilevazione che si interfaccia con il db. Verrà registrato il timestamp di avvio connessione e quello di fine connessione del dispositivo. La presenza sarà registrata in secondi, con un errore acnora da stabilire, e su di essa verrà costruita una funzione monotona che determinerà progressivamente il punteggio accumulato.

- [ ] Analisi dei requisiti
- [ ] Analisi di fattibilità
- [ ] Analisi dell'infrastruttura

Riassumiamo e descriviamo i passi principali per la realizzazione del nostro sistema:

### Web App

Applicazione web per la memorizzazione delle presenze in linguaggio `python3` interpretato a lato server. Costruzione di un web-server attraverso il modulo `Flask` interfacciato al database NoSQL `CouchDb` basato su `JSON`. Il sistema accetta principalmente due tipologie di persone: admin e utente normale. L'admin ha una propria view per controllare l'andamento delle presenze. L'utente è colui che utilizza questo servizio di "timbratura" digitale attraverso il proprio smartphone.

#### Flask

Installazione del modulo attraverso:

`$ pip3 install Flask`

e utilizzo del medesimo nel programma python:

```python
from flask import Flask, session, request, flash, escape
from flask.templating import render_template
from django.utils.html import strip_tags

if __name__ == '__main__':
    app.run(debug = True)
```

Altri moduli da scaricare e importare:

`$ pip3 install Django`

In questo modo possiamo attivare un web-server sul quale fare girare le nostre pagine.

- [ ] Installazione del modulo Flask
- [ ] Avvio tramite applicazione python sulla porta 5000
- [ ] Costruire un sistema modulare: controller, model e data-mapper.

##### Gestione delle Sessioni Cache Cookie (Sottoprogetto assegnato a [Davide Molinari](https://github.com/DaveMol96))

...to do

#### [CouchDb](https://github.com/GiovanniBellorio/Frequency-Detection-Bluetooth/tree/dev/dumpedDB) (Sottoprogetto assegnato a [Alessandro Cosma](https://github.com/AlessandroCosma))

Installazione del modulo attraverso:

`$ pip3 install couchdb`

e utilizzo del medesimo nel programma python:

```python
import logging
import couchdb

def __open(cls)
	cls.__db4LogCon = couchdb.Server("http://%s:%s@%s:5984/" % (cls.__user, cls.__pw, cls.__server))
	logging.info("Connection to database " + cls.__dbName + " created.")
```

Per installare il servizio abbiamo utilizzato [Apache CouchDB](http://couchdb.apache.org/), mentre per effettuare il dump:

`$ brew install gnu-sed`

Per eseguire il Backup del database:

`$ bash couchdb-backup.sh -b -H 127.0.0.1 -d db_detection -f dumpedDB.json -u admin -p admin`

Per eseguire il Restore del database:

`$ bash couchdb-backup.sh -r -H 127.0.0.1 -d db_detection -f dumpedDB.json -u admin -p admin`

Essendo un database NoSQL creiamo N documenti per N utenti dove possiamo estrarre informazioni e memorizzare i tempi di entrata e uscita.

- [ ] Installazione di apache-CouchDB in locale
- [ ] Analisi della struttura dati
- [ ] Costruzione delle view
- [ ] Interrogazione alla base di dati in python

#### Template Grafico

Realizzazione di un template dinamico basato su `html5`, `css3` e `javascript`, soprattutto responsive.

- [ ] Pagina di login
- [ ] Pagina privata per l'utente
- [ ] Pagina privata per l'admin

#### Deploy Applicazione Python

L'idea è di esportare questa applicazione per farla girare per esempio su un webserver `Apache`.

- [ ] Creare un webserver con apache
- [ ] Installare database CouchDB
- [ ] Aggiornamento del database
- [ ] Porting della web-app

### Wireless Detection App

Applicazione utilizzata dall'utente master per la rilevazione di reti Wireless basate su tecnologia Wi-Fi.
Questa applicazione, all'avvio, fornisce due modalità di funzionamento mutualmente esclusive:

- [ ] AP-only: L'applicazione apre un access point (WAP) al quale uno o più utenti (slave) possono connettersi e rimanere connessi per tutta la durata della sessione prestabilita. In questa modalità potrebbe non essere consentita la navigazione web ai dispositivi collegati, a causa dei limiti della scheda di rete del dispositivo master o delle configurazioni dell'infrastruttura di rete alla quale si è collegati.
- [*] Monitor mode: La scheda di rete viene inizialmente settata in modalità monitor. Durante questa modalità vengono rilevati tutti i dispositivi Wireless (MAC Adress e Hostname) in trasmissione nel raggio di 10-20 metri, filtrando solo quelli riconosciuti come appartenenti al corso.

Nota:
* Per i limiti del segnale fare riferimento alla propria scheda di rete.
* Per permettere all'applicazione di riconoscere/filtrare correttamente i dispositivi, è necessario che indirizzi MAC e hostname siano già presenti nel database della Web app.

### Documentazione

L'idea è di tenere traccia di tutte le nostre azioni attraverso il sistema di `GitHub`.

- [ ] Realizzazione repository
- [ ] Creazione branch (master e dev) di lavoro
- [ ] Condivisione della repository
- [ ] Realizzazione e aggiornamento del file README.MD

## Autori

Per critiche o nuove idee contattare liberamente:

* giovanni.bellorio@studenti.univr.it (GIOVANNI BELLORIO)
* simone.girardi@studenti.univr.it (SIMONE GIRARDI)

## Licenza
[GNU](https://www.gnu.org/licenses/gpl-3.0.html)
