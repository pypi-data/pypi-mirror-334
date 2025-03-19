from pytest_asyncio import fixture as fixture_asyncio

from qena_shared_lib.logstash import (
    BaseLogstashSender,
    LogstashLogRecord,
    SenderResponse,
)


class MockLogstashSender(BaseLogstashSender):
    async def _send(self, _: LogstashLogRecord) -> SenderResponse:
        return SenderResponse(sent=True)


@fixture_asyncio(scope="session")
async def logstash():
    logstash = MockLogstashSender(service_name="test")

    await logstash.start()

    yield logstash

    await logstash.stop()
