# SensorySafe

Kartapp som visar sensoriskt belastande platser för autistiska personer.

## Funktioner

- **Platslista** med sensorisk betygsättning (ljud, ljus, trängsel)
- **Lägg till platser** med betyg 1-10 per kategori
- **Varningar** för högt belastande miljöer
- **Filter** för att visa bara platser under viss belastningsnivå
- **JSON-databas** som sparas lokalt

## Installation

### Beroenden

- Python 3.8+
- GTK4
- libadwaita
- PyGObject

#### Ubuntu/Debian

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

#### Fedora

```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

#### Arch Linux

```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

### Installera appen

```bash
pip install .
sensorysafe
```

### Kör utan installation

```bash
python -m sensorysafe.main
```

## Användning

1. Starta appen - exempelplatser visas direkt
2. Tryck **+** för att lägga till en ny plats
3. Betygsätt ljud, ljus och trängsel (1-10)
4. Använd **filtret** för att dölja högt belastande platser
5. Tryck på en plats för att se detaljer och varningar

## Datalagring

Platsdata sparas i `~/.local/share/sensorysafe/platser.json`.

## Licens

GPL-3.0
