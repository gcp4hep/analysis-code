import os

def setup_proxy(x509_data, proxy_path="/tmp/x509"):
    x509_data = x509_data
    x509_proxy_path = proxy_path
    if os.path.exists(x509_proxy_path):
        os.chmod(x509_proxy_path, 0o600)
    with open(x509_proxy_path, "wb") as f:
        f.write(x509_data)
    os.chmod(x509_proxy_path, 0o400)
    os.environ['X509_USER_PROXY'] = x509_proxy_path


def setup_rucio_and_proxy(
    x509_data,
    rucio_account="nihartma",
    rucio_home='/srv/conda/envs/notebook',
    proxy_path="/tmp/x509",
):
    os.environ['RUCIO_ACCOUNT']  = rucio_account
    os.environ['RUCIO_HOME'] = rucio_home
    setup_proxy(x509_data, proxy_path)


def get_signed_url(client, scope, name, rse="GOOGLE_EU"):
    return next(
        client.list_replicas([{"scope" : scope, "name" : name}], rse_expression=rse)
    )["rses"][rse][0]


def get_signed_url_worker(proxy_data, scope, name, rucio_account="nihartma", rucio_home='/opt/conda'):
    import rucio.client
    setup_rucio_and_proxy(proxy_data, rucio_account=rucio_account, rucio_home=rucio_home, proxy_path="x509")
    rucio_client = rucio.client.Client()
    return get_signed_url(rucio_client, scope, name)