import os
from dask.distributed import WorkerPlugin


def setup_rucio_and_proxy(
    x509_data=None,
    rucio_account="nihartma",
    rucio_home='/srv/conda/envs/notebook',
    proxy_path="/tmp/x509",
):
    os.environ['RUCIO_ACCOUNT']  = rucio_account
    os.environ['RUCIO_HOME'] = rucio_home
    x509_data = x509_data
    x509_proxy_path = proxy_path
    if x509_data is not None:
        if os.path.exists(x509_proxy_path):
            os.chmod(x509_proxy_path, 0o600)
        with open(x509_proxy_path, "wb") as f:
            f.write(x509_data)
        os.chmod(x509_proxy_path, 0o400)
    os.environ['X509_USER_PROXY'] = x509_proxy_path


def get_signed_url(scope, name, rse="GOOGLE_EU", ca_cert="cern_bundle.pem"):
    import rucio.client
    client = rucio.client.Client(ca_cert=ca_cert)
    return next(
        client.list_replicas([{"scope" : scope, "name" : name}], rse_expression=rse)
    )["rses"][rse][0]


class SetupRucioAndProxyWorker(WorkerPlugin):
    def __init__(
        self,
        x509_path,
        rucio_account,
        ca_path="cern_bundle.pem",
        rucio_home="/srv/conda/envs/notebook",
        proxy_path="x509"
    ):
        self.proxy_path = proxy_path
        self.rucio_account = rucio_account
        self.rucio_home = rucio_home
        self.ca_path = ca_path
        with open(x509_path, "rb") as f:
            self.x509_data = f.read()
        with open(ca_path, "rb") as f:
            self.ca_data = f.read()

    def setup(self, worker):
        if os.path.exists(self.proxy_path):
            os.chmod(self.proxy_path, 0o600)
        with open(self.proxy_path, "wb") as f:
            f.write(self.x509_data)
        os.chmod(self.proxy_path, 0o400)
        os.environ["X509_USER_PROXY"] = self.proxy_path
        os.environ['RUCIO_ACCOUNT']  = self.rucio_account
        os.environ['RUCIO_HOME'] = self.rucio_home
        with open(self.ca_path, "wb") as f:
            f.write(self.ca_data)