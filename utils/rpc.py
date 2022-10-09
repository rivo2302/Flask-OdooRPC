import xmlrpc.client


class RPC:
    def __init__(self, conf) -> None:
        self.conf = conf
        pass

    def common(self):
        return xmlrpc.client.ServerProxy(
            f"{self.conf['HOST']}/xmlrpc/2/common", allow_none=True
        )

    def login(self):
        return self.common().authenticate(
            self.conf["DB"], self.conf["USER"], self.conf["PASSWORD"], {}
        )

    def execute(self, model, method, *args):
        if not self.login():
            return False
        return xmlrpc.client.ServerProxy(
            f"{self.conf['HOST']}/xmlrpc/2/object", allow_none=True
        ).execute_kw(
            self.conf["DB"],
            self.login(),
            self.conf["PASSWORD"],
            model,
            method,
            args,
        )
