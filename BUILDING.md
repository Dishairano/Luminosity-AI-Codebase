# Luminosity OS — Bouwen & testen (BUILDING)

Dit document beschrijft reproduceerbaar hoe je de engine test, de schil draait
en de bootbare ISO bouwt.

## 1. Engine testen (pytest)

```bash
python -m venv .venv && . .venv/bin/activate
pip install pytest pytest-cov
pytest                       # alle tests
pytest --cov=luminosity_engine --cov=modules --cov-report=term-missing
```

De pytest-configuratie staat in `pyproject.toml` (`pythonpath = ["."]`), zodat
zowel `luminosity_engine` als `modules` importeerbaar zijn zonder installatie.

## 2. Engine handmatig proberen

```bash
python -m luminosity_engine.cli "installeer firefox"      # mens-vriendelijk
python -m luminosity_engine.cli --json "wifi status"      # zoals de schil het ziet
python -m luminosity_engine.cli --logboek                 # logboek (JSON)
```

## 3. De schil (Quickshell)

De schil draait op Hyprland (Wayland) met Quickshell uit de AUR. Headless
testen kan met het demo-harnas, dat exact de JSON-CLI aanroept die de QML-schil
gebruikt:

```bash
python luminosity-shell/demo_shell.py
```

Dit toont de drie verplichte scenario's (simpel, fout, geannuleerd) en het
logboek.

## 4. De bootbare ISO bouwen (via Docker)

De buildhost hoeft geen Arch te zijn; we bouwen in een `archlinux:latest`
container met `archiso`.

```bash
cd iso
./build-docker.sh                 # ISO zonder quickshell (snel, betrouwbaar)
./build-docker.sh --with-quickshell   # probeert quickshell uit de AUR te bouwen
```

- Resultaat: `iso/out/luminosity-*.iso` en `iso/out/build.log`.
- Vereist Docker met `--privileged` (mkarchiso heeft loop-devices nodig).

### Over quickshell (eerlijk)

`quickshell` zit niet in de officiële Arch-repos, alleen in de AUR. `build.sh`
bouwt het apart in een lokale repo. Lukt dat niet, dan bouwt de ISO door
**zonder** quickshell; het OS start dan via een nette terminal-terugval
(`/usr/local/bin/luminosity-shell`) in plaats van de grafische schil.

## 5. De ISO testen in QEMU

```bash
cd iso
./test-qemu.sh                    # zoekt iso/out/*.iso
HEADLESS=1 ./test-qemu.sh         # zonder venster
```

> **Let op (eerlijk):** dit project genereert geen echte boot-testresultaten op
> fysieke hardware. `test-qemu.sh` is de reproduceerbare teststap; build-logs en
> dit script vervangen een echte boottest.
