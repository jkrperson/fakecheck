class SiteNotFound(Exception):
    pass


class BaseHTTPError(Exception):
    pass

class ServiceTemporaryUnavailable(Exception):
    pass