import ssl
from pathlib import Path

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.servers.basehttp import WSGIServer


def get_default_cert_paths():
    try:
        import sslserver

        package_dir = Path(sslserver.__file__).resolve().parent
        cert_dir = package_dir / "certs"
        cert_path = cert_dir / "development.crt"
        key_path = cert_dir / "development.key"
        if cert_path.exists() and key_path.exists():
            return cert_path, key_path
    except ImportError:
        pass
    return None, None


class SecureWSGIServer(WSGIServer):
    certificate = None
    key = None

    def __init__(self, *args, certificate=None, key=None, **kwargs):
        self.certificate = certificate or self.certificate
        self.key = key or self.key
        super().__init__(*args, **kwargs)

    def server_activate(self):
        if self.certificate and self.key:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(self.certificate), str(self.key))
            self.socket = context.wrap_socket(self.socket, server_side=True)
        super().server_activate()


class Command(RunserverCommand):
    help = "Starts a lightweight web server for development over HTTPS."
    protocol = "https"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--certificate",
            default=None,
            help="Path to the SSL certificate file.",
        )
        parser.add_argument(
            "--key",
            default=None,
            help="Path to the SSL key file.",
        )

    def handle(self, *args, **options):
        self.certificate = (
            Path(options["certificate"]).expanduser()
            if options.get("certificate")
            else None
        )
        self.key = Path(options["key"]).expanduser() if options.get("key") else None

        if not self.certificate or not self.key:
            default_cert, default_key = get_default_cert_paths()
            self.certificate = self.certificate or default_cert
            self.key = self.key or default_key

        if not self.certificate or not self.key:
            raise CommandError(
                "SSL certificate and key files are required. "
                "Pass --certificate and --key, or install django-sslserver."
            )

        if not self.certificate.exists() or not self.key.exists():
            raise CommandError(
                f"SSL certificate or key file not found: {self.certificate}, {self.key}"
            )

        return super().handle(*args, **options)

    def inner_run(self, *args, **options):
        self.server_cls = type(
            "SecureWSGIServer",
            (SecureWSGIServer,),
            {"certificate": self.certificate, "key": self.key},
        )
        return super().inner_run(*args, **options)
