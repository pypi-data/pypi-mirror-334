from pathlib import Path

from pytest import fixture, mark, warns

from ..src.config import *


def getCfgContent() -> str:
    return '[app]\n\tname = "MyPyUtils"\n\tloggingLevel = "Debug"\n\tnumber = 1.5\n\t[app.author]\n\t\tname = "Jaimead7"\n\t\turl = "https://github.com/Jaimead7"'

@fixture(autouse= True)
def configureTestFolder(tmp_path: Path) -> None:
    dist: Path = tmp_path / 'dist'
    dist.mkdir()
    config: Path = tmp_path / 'dist' / 'config'
    config.mkdir()
    configFile: Path = tmp_path / 'dist' / 'config' / 'config.toml'
    configFile.write_text(getCfgContent())

@fixture
def prjTestDict(tmp_path: Path) -> ProjectPathsDict:
    prjTestDict = ProjectPathsDict()
    prjTestDict.setAppPath(tmp_path)
    return prjTestDict

@fixture
def cfgManager(prjTestDict: ProjectPathsDict) -> ConfigFileManager:
    return ConfigFileManager(prjTestDict[ProjectPathsDict.CONFIG_FILE_PATH])


class TestProjectPaths:
    def test_defaultPaths(self, prjTestDict: ProjectPathsDict, tmp_path: Path) -> None:
        assert prjTestDict[ProjectPathsDict.APP_PATH] == tmp_path
        assert prjTestDict[ProjectPathsDict.DIST_PATH] == tmp_path / 'dist'
        assert prjTestDict[ProjectPathsDict.CONFIG_PATH] == tmp_path / 'dist' / 'config'
        assert prjTestDict[ProjectPathsDict.CONFIG_FILE_PATH] == tmp_path / 'dist' / 'config' / 'config.toml'

    def test_errors(self, prjTestDict: ProjectPathsDict) -> None:
        with warns(UserWarning):
            prjTestDict['ERROR_PATH'] = 'noPath'
        assert prjTestDict['ERROR_PATH'] == None


class TestConfigFileManager:
    def test_access(self, cfgManager: ConfigFileManager) -> None:
        assert cfgManager.app.name == 'MyPyUtils'
        assert cfgManager.app.number == 1.5
        assert type(cfgManager.app.author) == ConfigDict
        assert cfgManager.app.author == {'name': 'Jaimead7', 'url': 'https://github.com/Jaimead7'}
        assert cfgManager.app.author.name == 'Jaimead7'

    def test_routes(self, cfgManager: ConfigFileManager) -> None:
        assert cfgManager.app.author.route == ['app', 'author']

    def test_fileManager(self, cfgManager: ConfigFileManager) -> None:
        assert cfgManager.app.author.fileManager == cfgManager

    @mark.parametrize('content, expected', [
        ('[app]\n\tname = "MyPyUtils"\n\tloggingLevel = "Info"\n\t[app.author]\n\t\tname = "Jaimead7"\n\t\turl = "https://github.com/Jaimead7"',
         '[app]\n\tname = "MyPyUtils"\n\tloggingLevel = "Info"\n\t[app.author]\n\t\tname = "Jaimead7"\n\t\turl = "https://github.com/Jaimead7"'),
        ({'app': {'name': 'MyPyUtils', 'loggingLevel': 'Warning', 'author': {'name': 'Jaimead7', 'url': 'https://github.com/Jaimead7'}}},
         '[app]\nname = "MyPyUtils"\nloggingLevel = "Warning"\n\n[app.author]\nname = "Jaimead7"\nurl = "https://github.com/Jaimead7"\n'),
    ])
    def test_writeFile(self, content: str | dict, expected: str, cfgManager: ConfigFileManager) -> None:
        cfgManager.writeFile(content)
        with open(cfgManager._filePath) as f:
            assert expected == f.read()

    def test_writeVar(self, cfgManager: ConfigFileManager) -> None:
        cfgManager.writeVar(['app', 'loggingLevel'], 'critical')
        assert cfgManager.app.loggingLevel == 'critical'
        cfgManager.app.loggingLevel = 'error'
        assert cfgManager.app.loggingLevel == 'error'
        cfgManager.app.number = 2.1
        assert cfgManager.app.number == 2.1
