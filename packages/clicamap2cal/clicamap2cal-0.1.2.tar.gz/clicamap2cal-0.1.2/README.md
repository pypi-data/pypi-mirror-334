# Générateur de fichier calendrier ICS à partir de ClicAMAP

![doc/logo.png](doc/logo.png)

## Description

Je ne suis jamais parvenu à exporter proprement mes livraisons AMAP dans un calendrier standardisé `.ics` importable dans n'importe quel logiciel de calendrier.

Ce logiciel est là pour combler ce manque.

## Installation

```
$ pip install clicamap2cal

```
## Utilisation

Soient:
* `VOTRE_ADRESSE_EMAIL` l'adresse email que vous utilisez pour vous connecter au site https://www.clicamap.org
* `VOTRE_MOTDEPASSE_CLICAMAP` le mot de passe que vous utilisez pour vous connecter au site https://www.clicamap.org

```
$ export CLICAMAP2CAL_PASSWORD="VOTRE_MOTDEPASSE_CLICAMAP"
$ clicamap2cal --username "VOTRE_ADRESSE_EMAIL" > amap.ics
```

Cela génèrera le fichier local `amap.ics` qui pourra alors être importé directement dans vos calendriers.
