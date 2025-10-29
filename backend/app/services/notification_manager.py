import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4
import logging
import smtplib
from email.message import EmailMessage
from contextlib import contextmanager

from ..core.settings import settings

LOG = logging.getLogger("notification_manager")


class NotificationManager:
    """Gestor simple de notificaciones en fichero (MVP sin DB).

    Persistencia: archivo JSON en el directorio del backend.
    - notifications: lista de dicts con campos mínimos.
    """

    def __init__(self, filename: Optional[str] = None):
        # Allow overriding notifications file via env var (useful for testing)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.getenv("NOTIFICATIONS_FILE")
        if filename:
            self.filepath = filename
        elif env_file:
            self.filepath = env_file
        else:
            self.filepath = os.path.join(backend_dir, "notifications.json")
        self._data: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.filepath):
                # Read with a (shared) file lock when possible to avoid race conditions
                with open(self.filepath, "r", encoding="utf-8") as f:
                    with self._file_lock(f, exclusive=False):
                        try:
                            self._data = json.load(f)
                        except json.JSONDecodeError:
                            LOG.warning("Archivo de notificaciones corrupto o vacío, reempezando con lista vacía")
                            self._data = []
            else:
                self._data = []
        except Exception:
            LOG.exception("Error cargando notificaciones, empezando con lista vacía")
            self._data = []

    def _persist(self):
        try:
            # Ensure directory exists
            dirpath = os.path.dirname(self.filepath)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)

            # Open in r+ or w+ and lock for exclusive write to avoid concurrent writes
            # Use 'w+' which truncates, but we acquire lock immediately for safety
            with open(self.filepath, "w+", encoding="utf-8") as f:
                with self._file_lock(f, exclusive=True):
                    f.seek(0)
                    json.dump(self._data, f, ensure_ascii=False, indent=2, default=str)
                    f.truncate()
                    f.flush()
        except Exception:
            LOG.exception("Error persistiendo notificaciones")

    @contextmanager
    def _file_lock(self, fileobj, exclusive: bool = True):
        """Context manager para bloqueo de fichero cross-platform.

        Intenta usar fcntl (POSIX) o msvcrt (Windows). Si falla, continúa sin bloqueo
        (útil para entornos donde locking no está disponible).
        """
        locked = False
        try:
            if os.name == "nt":
                try:
                    import msvcrt
                    mode = msvcrt.LK_LOCK if exclusive else msvcrt.LK_RLCK
                    # Lock 1 byte (works as a simple advisory lock)
                    msvcrt.locking(fileobj.fileno(), msvcrt.LK_LOCK, 1)
                    locked = True
                except Exception:
                    LOG.debug("msvcrt locking no disponible, continuando sin lock")
            else:
                try:
                    import fcntl
                    fcntl.flock(fileobj.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
                    locked = True
                except Exception:
                    LOG.debug("fcntl flock no disponible, continuando sin lock")
            yield
        finally:
            if locked:
                try:
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(fileobj.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(fileobj.fileno(), fcntl.LOCK_UN)
                except Exception:
                    LOG.debug("Error liberando lock de fichero")

    def _now(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def create(self, *, recipients: List[Dict[str, Any]], title: str, message: str, link: Optional[str] = None, payload: Optional[Dict[str, Any]] = None, event: Optional[str] = None) -> List[Dict[str, Any]]:
        """Crea notificaciones para los destinatarios.

        recipients: list of dicts: {"user_id": int} or {"role": "supervisor"}
        Returns the created notifications.
        """
        created = []
        for r in recipients:
            notif = {
                "id": str(uuid4()),
                "recipient": r,
                "title": title,
                "message": message,
                "event": event,
                "link": link,
                "payload": payload or {},
                "read": False,
                "created_at": self._now(),
            }
            self._data.append(notif)
            created.append(notif)

            # attempt email
            self._try_send_email(recipient=r, title=title, message=message, link=link)

        self._persist()
        return created

    def list_for_user(self, user_id: int, roles: List[str]) -> List[Dict[str, Any]]:
        # user-specific + role-specific
        result = []
        for n in self._data:
            rec = n.get("recipient", {})
            if rec.get("user_id") == user_id:
                result.append(n)
            elif rec.get("role") and rec.get("role") in roles:
                result.append(n)
        # newest first
        return sorted(result, key=lambda x: x.get("created_at"), reverse=True)

    def mark_read(self, notif_id: str, user_id: int) -> bool:
        for n in self._data:
            if n.get("id") == notif_id:
                # allow marking if recipient matches user or role (no strict role check here)
                n["read"] = True
                self._persist()
                return True
        return False

    def _try_send_email(self, recipient: Dict[str, Any], title: str, message: str, link: Optional[str]):
        # MVP: email disabled by default. Enable with NOTIFICATIONS_EMAIL_ENABLED=true
        enabled = os.getenv("NOTIFICATIONS_EMAIL_ENABLED", "false").lower() in ("1", "true", "yes")
        if not enabled:
            LOG.debug("Envío de email de notificación deshabilitado (MVP JSON-only). Título: %s", title)
            LOG.info("Notificación almacenada (JSON): %s - %s", title, message)
            return

        # attempt to send email if SMTP env vars are present
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT") or 25)
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        # If SMTP not configured, just log
        if not smtp_host:
            LOG.debug("SMTP no configurado: registro en log en vez de envío de email")
            LOG.info("Notificación: %s - %s", title, message)
            return

        # For MVP send a generic email to configured SMTP_USER (can't resolve recipient email without DB)
        try:
            msg = EmailMessage()
            msg["Subject"] = title
            msg["From"] = smtp_user or "no-reply@example.com"
            msg["To"] = smtp_user or "no-reply@example.com"
            body = message
            if link:
                body += f"\n\nLink: {link}"
            msg.set_content(body)

            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as s:
                if smtp_user and smtp_pass:
                    s.starttls()
                    s.login(smtp_user, smtp_pass)
                s.send_message(msg)
            LOG.info("Email enviado (MVP) para notificación: %s", title)
        except Exception:
            LOG.exception("Fallo al enviar email de notificación (se registró en log)")


notification_manager = NotificationManager()
