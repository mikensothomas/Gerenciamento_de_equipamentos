from sshtunnel import SSHTunnelForwarder
from config.Config import Settings
from sqlmodel import create_engine, Session

class Database:
    def __init__(self):
        self._engine = None
        self._tunel = None

    def starTunnel(self):
        self._tunel = SSHTunnelForwarder(
            (Settings.ssh_host, Settings.ssh_port),
            ssh_username=Settings.ssh_user,
            ssh_password=Settings.ssh_password,
            remote_bind_address=(Settings.db_host, Settings.db_port)
        )
        self._tunel.start()

        local_port = self._tunel.local_bind_port
        url = f"mysql+pymysql://{Settings.db_user}:{Settings.db_password}@127.0.0.1:{local_port}/{Settings.db_name}"
        
        self._engine = create_engine(url, echo=True)

    def get_db(self):
        if not self._engine:
            raise RuntimeError("Engine não foi inicializada!")
        with Session(self._engine) as s:
            yield s