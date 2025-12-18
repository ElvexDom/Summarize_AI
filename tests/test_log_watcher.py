import pytest
from pathlib import Path
from utils.log_watcher import LogWatcher

LOG_DIR = Path("logs")

def test_log_creation(tmp_path):
    """
    Teste que LogWatcher écrit correctement les messages dans les fichiers de log.
    Utilise tmp_path pour créer un dossier temporaire et isolé pour les logs.
    """

    # Redéfinir le dossier de logs temporaire
    LogWatcher.LOG_DIR = tmp_path
    LogWatcher.LOG_DIR.mkdir(exist_ok=True)

    # Supprimer les handlers existants et réinitialiser les fichiers de logs
    from loguru import logger
    logger.remove()
    logger.add(tmp_path / "errors.log", level="ERROR")
    logger.add(tmp_path / "warnings.log", level="WARNING")
    logger.add(tmp_path / "info.log", level="INFO")
    logger.add(tmp_path / "all.log", level="DEBUG")

    # Log sur différents niveaux
    LogWatcher.log("debug", "Message DEBUG")
    LogWatcher.log("info", "Message INFO")
    LogWatcher.log("warning", "Message WARNING")
    LogWatcher.log("error", "Message ERROR")
    LogWatcher.log("critical", "Message CRITICAL")
    LogWatcher.log("unknown_level", "Message inconnu")

    # Vérifier que les fichiers sont créés
    assert (tmp_path / "errors.log").exists()
    assert (tmp_path / "warnings.log").exists()
    assert (tmp_path / "info.log").exists()
    assert (tmp_path / "all.log").exists()

    # Vérifier que le message INFO est dans info.log
    info_content = (tmp_path / "info.log").read_text()
    assert "Message INFO" in info_content

    # Vérifier que le message ERROR est dans errors.log
    error_content = (tmp_path / "errors.log").read_text()
    assert "Message ERROR" in error_content

    # Vérifier que le message inconnu est enregistré en ERROR
    assert "Message inconnu" in error_content
