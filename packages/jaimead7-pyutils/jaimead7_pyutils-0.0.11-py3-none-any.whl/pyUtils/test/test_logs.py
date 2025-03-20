from re import search

from pytest import LogCaptureFixture, fixture, mark

from ..src.logs import *


@fixture(autouse= True)
def setCaplogLvl(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    caplog.clear()


class TestLogs:
    @mark.parametrize('msg, expectedRe', [
        ('Debug test message', '\\x1b\[94mDEBUG -----> (3[01]|[012][0-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[10][0-9]):([0-5][0-9]):([0-5][0-9]):\\x1b\[0m Debug test message'),
    ])
    def test_debug(self, msg: str, expectedRe: str, caplog: LogCaptureFixture) -> None:
        debugLog(msg)
        assert bool(search(expectedRe, caplog.records[0].message))

    @mark.parametrize('msg, expectedRe', [
        ('Info test message', '\\x1b\[0mINFO ------> (3[01]|[012][0-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[10][0-9]):([0-5][0-9]):([0-5][0-9]):\\x1b\[0m Info test message'),
    ])
    def test_info(self, msg: str, expectedRe: str, caplog: LogCaptureFixture) -> None:
        infoLog(msg)
        assert bool(search(expectedRe, caplog.records[0].message))

    @mark.parametrize('msg, expectedRe', [
        ('Warning test message', '\\x1b\[93mWARNING ---> (3[01]|[012][0-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[10][0-9]):([0-5][0-9]):([0-5][0-9]):\\x1b\[0m Warning test message'),
    ])
    def test_warning(self, msg: str, expectedRe: str, caplog: LogCaptureFixture) -> None:
        warningLog(msg)
        assert bool(search(expectedRe, caplog.records[0].message))

    @mark.parametrize('msg, expectedRe', [
        ('Error test message', '\\x1b\[91mERROR -----> (3[01]|[012][0-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[10][0-9]):([0-5][0-9]):([0-5][0-9]):\\x1b\[0m Error test message'),
    ])
    def test_error(self, msg: str, expectedRe: str, caplog: LogCaptureFixture) -> None:
        errorLog(msg)
        assert bool(search(expectedRe, caplog.records[0].message))

    @mark.parametrize('msg, expectedRe', [
        ('Critical test message', '\\x1b\[101mCRITICAL --> (3[01]|[012][0-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[10][0-9]):([0-5][0-9]):([0-5][0-9]):\\x1b\[0m Critical test message'),
    ])
    def test_critical(self, msg: str, expectedRe: str, caplog: LogCaptureFixture) -> None:
        criticalLog(msg)
        assert bool(search(expectedRe, caplog.records[0].message))

    @mark.parametrize('lvl, nMessages', [
        (logging.DEBUG, 5),
        (logging.INFO, 4),
        (logging.WARNING, 3),
        (logging.ERROR, 2),
        (logging.CRITICAL, 1),
    ])
    def test_setLoggingLevel(self, lvl: int, nMessages: int,  caplog: LogCaptureFixture) -> None:
        setLoggingLevel(lvl)
        debugLog('Debug test message')
        infoLog('Info test message')
        warningLog('Warning test message')
        errorLog('Error test message')
        criticalLog('Critical test message')
        assert len(caplog.records) == nMessages
