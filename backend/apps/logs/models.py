from django.db import models


class AppLog(models.Model):
    """A Logger entry persisted when LOG_TO_DB is enabled. Never edited."""

    class Level(models.TextChoices):
        DEBUG = "debug"
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        CRITICAL = "critical"

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    app_name = models.CharField(max_length=150, db_index=True)
    level = models.CharField(max_length=10, choices=Level.choices, db_index=True)
    message = models.TextField()
    extra = models.JSONField(null=True, blank=True)
    trace = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["app_name", "level", "created_at"]),
        ]

    def __str__(self):
        return f"[{self.level}] {self.app_name}: {self.message[:80]}"
