import os

from newrelic_telemetry_sdk import Log, LogClient
from newrelic_telemetry_sdk.client import HTTPResponse


class Ingestion:
    def __init__(self, license_key=None):
        if license_key is None:
            license_key = os.environ["NEW_RELIC_LICENSE_KEY"]
        self.client = LogClient(license_key)

    def send(self, message) -> HTTPResponse:
        # TODO log level. check the API docs
        r = self.client.send(Log(message))
        r.raise_for_status()
        return r
