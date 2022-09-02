# Otevřená data z hlasování zastupitelstva

V tomto repozitáři se nachází jednoduchý systém pro zveřejňování
otevřených dat z hlasování zastupitelstva města Brna.

Systém zpracovává HTML protokoly z hlasování, které jsou aktuálně dostupné
také [na webu města](https://www.brno.cz/sprava-mesta/dokumenty-mesta/zapisy-ze-zastupitelstva-mesta-brna/). 
Získaná data poskytuje ve formátu JSON se schématem popsaným v souboru [output-schema.json](./output-schema.json).

## Datový endpoint

Po spuštění jsou data z hlasování dostupná na pevné url adrese. Při přístupu na tuto adresu (GET request) bez zadání
parametrů jsou vrácena veškerá data v jednom velkém JSON souboru.

Přímý přístup na adresu https://kod.brno.cz/zastupitelstvo/ tedy vrátí všechna data.

Záznamy lze také řadit a stránkovat pomocí url parametrů. K dispozici jsou tyto parametry:

- `sort`: určuje řazení záznamů ve výsledném JSONu, povolené hodnoty jsou `newest` a `oldest`
- `limit`: určuje počet záznamů na jedné stránce (tzn. maximální počet zobrazených záznamů), povolené jsou kladné celočíselné hodnoty
- `offset`: při použití parametru `limit` určuje záznam, od kterého se začíná (indexováno od nuly), povolené jsou nezáporné celočíselné hodnoty

Parametry jsou zadávány standardním způsobem přímo v url adrese - za úvodním otazníkem následují jednotlivé dvojice klíč=hodnota oddělené ampersandem.

Příklad - následující url adresa s parametry zobrazí třetí stránku záznamů stránkovaných po deseti a řazených podle data sestupně:

https://kod.brno.cz/zastupitelstvo/?sort=newest&limit=10&offset=20

offset = index stránky * limit, v tomto případě tedy 2 * 10 (index třetí stránky je 2, protože se indexuje od nuly)

## Spuštění systému

### Prerekvizity

Systém je určen pro provoz na unixových operačních systémech. Předpoklady pro fungování jsou:

- python 3.8
- pipenv
- SQLite
- flask
- cron

### Instalace

Nejdříve je potřeba vytvořit databázi:

```bash
$ sqlite3 db.sqlite < ./database/create.sql
```

Následně je potřeba zkopírovat a případně upravit vzorový konfigurační soubor:

```bash
$ cp example-config.ini config.ini
```

Poté je možné pomocí `pipenv` nainstalovat potřebné knihovny: 

```bash
$ pipenv install
```

Jestli byla instalace úspěšná lze ověřit spuštěním jednotkových testů:

```bash
$ pipenv run python -m unittest discover -s tests
```

### Nastavení automatického spouštění

Program pro zpracování protokolů ve zdrojové složce lze spustit následujícím příkazem:

```bash
$ pipenv run python ./daemon.py
```

Příklad cronu pro pravidelné spouštění každou hodinu:

```cron
0 * * * * * cd /path/to/folder/ && pipenv run python ./daemon.py
```

### Nastavení endpointu

Pro spouštění endpointu `endpoint.py` je potřeba mít nainstalovaný flask. Poté stačí 
spustit aplikační server následujícím příkazem:

```bash
$ FLASK_APP=./endpoint.py flask run
```

Tím dojde ke spuštění serveru na adrese http://127.0.0.1:5000/. Tato adresa zároveň slouží jako
jediný endpoint pro přístup k datům. Následně je možné tento endpoint vystavit veřejně např.
pomocí reverzní proxy.

