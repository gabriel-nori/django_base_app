from django.test import SimpleTestCase
from pathlib import Path
import subprocess
import tempfile
import sys
import os

BACKEND_DIR = Path(__file__).resolve().parent.parent


def run_python(args: list[str], **env: str) -> str:
    """Run in a fresh process so settings are built from the given env."""
    process_env = {**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings", **env}
    result = subprocess.run(
        [sys.executable, *args],
        cwd=BACKEND_DIR,
        env=process_env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def run_in_django(code: str, **env: str) -> str:
    return run_python(["manage.py", "shell", "--no-imports", "-c", code], **env)


class DatabaseEngineTestCase(SimpleTestCase):
    # Only builds the settings module, so no database driver is required
    code = (
        "from config import settings; db = settings.DATABASES['default'];"
        "print(db['ENGINE'], db.get('PORT', ''))"
    )

    def run_settings(self, **env: str) -> str:
        return run_python(["-c", self.code], **env)

    def test_defaults_to_sqlite(self):
        output = self.run_settings(DB_ENGINE="")
        self.assertEqual(output, "django.db.backends.sqlite3")

    def test_postgresql(self):
        output = self.run_settings(DB_ENGINE="postgresql", DB_PORT="")
        self.assertEqual(output, "django.db.backends.postgresql 5432")

    def test_mysql_custom_port(self):
        output = self.run_settings(DB_ENGINE="MySQL", DB_PORT="3307")
        self.assertEqual(output, "django.db.backends.mysql 3307")

    def test_invalid_engine(self):
        with self.assertRaisesMessage(AssertionError, "Invalid DB_ENGINE"):
            self.run_settings(DB_ENGINE="mongodb")


class ServeSpaTestCase(SimpleTestCase):
    code = (
        "from django.test import Client; c = Client();"
        "print(c.get('/').status_code, c.get('/some/client/route').getvalue().decode(),"
        " c.get('/assets/app.js').getvalue().decode(), c.get('/api/unknown/').status_code)"
    )

    def setUp(self):
        self.spa_dir = tempfile.TemporaryDirectory()
        spa_path = Path(self.spa_dir.name)
        (spa_path / "index.html").write_text("<html>spa</html>")
        (spa_path / "assets").mkdir()
        (spa_path / "assets" / "app.js").write_text("console.log('app')")

    def tearDown(self):
        self.spa_dir.cleanup()

    def test_serves_spa(self):
        output = run_in_django(self.code, SERVE_SPA="true", SPA_DIR=self.spa_dir.name)
        self.assertEqual(output, "200 <html>spa</html> console.log('app') 404")

    def test_spa_disabled(self):
        code = "from django.test import Client; print(Client().get('/some/route').status_code)"
        output = run_in_django(code, SERVE_SPA="false", SPA_DIR=self.spa_dir.name)
        self.assertEqual(output, "404")
