# Otevřená data z hlasování zastupitelstva

V tomto repozitáři se nachází jednoduchý systém pro zveřejňování
otevřených dat z hlasování zastupitelstva města Brna.

Systém zpracovává HTML protokoly z hlasování, které jsou aktuálně dostupné
také [na webu města](https://www.brno.cz/sprava-mesta/dokumenty-mesta/zapisy-ze-zastupitelstva-mesta-brna/). Získaná data poskytuje ve formátu JSON.

## Spuštění systému

### Prerekvizity

Systém je určen pro provoz na unixových operačních systémech. Předpoklady pro fungování jsou:

- python 3.8
- pipenv
- SQLite
- Apache HTTP server
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
0 * * * * * pipenv run python ./daemon.py
```

### Nastavení endpointu

Pro spouštění endpointu `endpoint.py` je potřeba nejdříve aktivovat v Apache
modul `cgid`:

```bash
a2enmod cgid
```

Následně je nutné konfigurovat pro Apache složku, kde se soubor `endpoint.py` 
nachází, nebo využít již nastavené složky `/usr/lib/cgi-bin`.
