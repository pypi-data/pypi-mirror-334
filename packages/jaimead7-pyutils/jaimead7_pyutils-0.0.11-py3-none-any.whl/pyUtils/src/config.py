from __future__ import annotations

import inspect
import operator
import sys
import warnings
from datetime import datetime
from functools import reduce
from pathlib import Path
from typing import Any, Optional

import tomli
import tomli_w

warnings.formatwarning = lambda msg, *args, **kwargs: f'\033[93mWARNING ---> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:\033[0m {msg}'


# PATHS
class ProjectPathsDict(dict):
    APP_PATH = 'APPPATH'
    DIST_PATH = 'DISTPATH'
    CONFIG_PATH = 'CONFIGPATH'
    CONFIG_FILE_PATH = 'CONFIGFILEPATH'
    
    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            return None

    def __setitem__(self, key, value) -> None:
        if value is not None:
            if Path(value).exists():
                return super().__setitem__(key, Path(value))
        warnings.warn(f'{value} is not a valid path\n')
        return super().__setitem__(key, None)

    def setAppPath(self, newAppPath: str) -> None:
        self[self.APP_PATH] = Path(newAppPath).resolve()
        try:
            self[self.DIST_PATH] = self[self.APP_PATH] / 'dist'
        except TypeError:
            self[self.DIST_PATH] = None
        try:
            self[self.CONFIG_PATH] = self[self.APP_PATH] / 'dist' / 'config'
        except TypeError:
            self[self.CONFIG_PATH] = None
        try:
            self[self.CONFIG_FILE_PATH] = self[self.APP_PATH] / 'dist' / 'config' / 'config.toml'
        except TypeError:
            self[self.CONFIG_FILE_PATH] = None
            

ppaths = ProjectPathsDict()
if getattr(sys, 'frozen', False):
    ppaths.setAppPath(Path(sys.executable).parents[1])  #CHECK
    #ppaths.setAppPath(path.abspath(path.join(path.dirname(sys.executable),'..')))
elif __file__:
    try:
        ppaths.setAppPath(Path(inspect.stack()[-1].filename).parents[1])  #CHECK
    except IndexError:
        ppaths.setAppPath('None')


# CONFIG
class ConfigDict(dict):
    def __init__(self,
                 *args,
                 route: Optional[list] = None,
                 fileManager: Optional[ConfigFileManager] = None,
                 **kwargs) -> None:
        self.route: Optional[list] = route
        self.fileManager: Optional[ConfigFileManager] = fileManager
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(route: {self.route}, fileManager: {self.fileManager})'

    def __str__(self) -> str:
        return str(self._data)

    def __getattr__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            try:
                result: Any = self[str(name)]
            except KeyError:
                raise AttributeError(f'"{name}" not found in the route {self.route} of file "{self.fileManager}"')
            if isinstance(result, dict):
                newRoute: list | None = self.route
                try:
                    newRoute.append(str(name))
                except AttributeError:
                    newRoute = [str(name)]
                return ConfigDict(result,
                                  route= newRoute,
                                  fileManager= self.fileManager)
            return result

    def __setattr__(self, name, value) -> None:
        if name in self.keys() and self.fileManager is not None:
            self.fileManager.writeVar(self.route + [name], value)
        return super().__setattr__(name, value)


class ConfigFileManager:
    def __init__(self, filePath: str | Path) -> None:
        self._setFilePath(filePath)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(filePath: {self._filePath}, data: {self._data})'

    def __str__(self) -> str:
        return str(self._data)

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__dict__[str(name)]
        except KeyError:
            result: Any = self._data[str(name)]
            if isinstance(result, dict):
                result = ConfigDict(result,
                                    route= [str(name)],
                                    fileManager= self,)
            return result

    @property
    def filePath(self) -> Path:
        return self._filePath

    @filePath.setter
    def filePath(self, value: str | Path) -> None:
        self._setFilePath(value)

    @property
    def _data(self) -> dict:
        try:
            with open(self._filePath, 'rb') as f:
                data: dict = tomli.load(f)
        except tomli.TOMLDecodeError:
            raise tomli.TOMLDecodeError(f'{self._filePath} is not a valid .toml file')
        return data

    def _setFilePath(self, value: str | Path) -> None:
        value = Path(value).with_suffix('.toml')
        if value.is_file():
            self._filePath: Path = value.resolve()
        else:
            raise FileExistsError(f'{value} is not a config file')

    def writeFile(self, fileContent: str | dict) -> None:
        if isinstance(fileContent, str):
            self._filePath.write_text(fileContent)
        if isinstance(fileContent, dict):
            self._filePath.write_text(tomli_w.dumps(fileContent))

    def writeVar(self, route: list, value: Any) -> None:
        data: dict = self._data
        operator.setitem(reduce(operator.getitem, route[:-1], data), route[-1], value)
        self.writeFile(data)


if ppaths[ProjectPathsDict.CONFIG_FILE_PATH] is not None:
    with open(ppaths[ProjectPathsDict.CONFIG_FILE_PATH], 'a'):
        ...
    cfg = ConfigFileManager(ppaths[ProjectPathsDict.CONFIG_FILE_PATH])
else:
    warnings.warn(f'There is no default config file\n')
    cfg = None
