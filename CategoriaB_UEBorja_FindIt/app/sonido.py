"""Sonido de clic al pulsar los botones (recursos/clic.wav).
Solo librería estándar: en Windows usa winsound; en Linux, paplay o aplay; en macOS, afplay.
Si el equipo no puede reproducir sonido, la app sigue funcionando en silencio."""
import platform
import shutil
import subprocess
from pathlib import Path

RUTA_CLIC = Path(__file__).resolve().parent.parent / "recursos" / "clic.wav"
CLASES_BOTON = ("Button", "TButton", "Checkbutton")


def reproducir_clic():
    """Reproduce el clic sin detener la app (en segundo plano)."""
    if not RUTA_CLIC.exists():
        return
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.PlaySound(str(RUTA_CLIC), winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        for programa in ("paplay", "aplay", "afplay"):
            if shutil.which(programa):
                opciones = ["-q"] if programa == "aplay" else []
                subprocess.Popen([programa, *opciones, str(RUTA_CLIC)],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
    except OSError:
        pass  # Sin sonido disponible: no pasa nada


def activar(root):
    """Hace sonar el clic en todos los botones de la app (los desactivados no suenan)."""
    def al_pulsar(evento):
        try:
            if str(evento.widget.cget("state")) != "disabled":
                reproducir_clic()
        except Exception:
            pass
    for clase in CLASES_BOTON:
        root.bind_class(clase, "<ButtonPress-1>", al_pulsar, add="+")  # add="+": no quita el comportamiento normal
