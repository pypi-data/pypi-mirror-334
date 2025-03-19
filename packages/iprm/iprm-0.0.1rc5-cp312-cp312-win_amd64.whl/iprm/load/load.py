from abc import ABC, abstractmethod
from iprm.util.sink import ConsoleLogSink
from iprm.util.platform import PLAT_CONTEXT_TYPE
from iprm.core.object import Object


# TODO: TO keep underlying API focused on our Native objects specifications,
#  non-native loaders (e.g. SCons and MSBuild .vcxproj) main purpose will be translating
#  from their format into iprm.api.obj.* instances directly, which means we bypass adding things
#  to the Session that aren't native Objects. These objects once in their native format SHOULD be
#  added to the Session. This way our native API only ever has to understand
#  the single format, keeping things clean and centralized. So for the SCons loader,
#  it will execute its file and collect the objects WITHOUT adding those objects to the
#  Session (for itself, it can inject capture of object creation in the Namespace setup), then perform "in memory"
#  generation of naive API objects, add them to the session, then if they want to save the session out (e.g. configure,
#  build, and test all works), they have now officially converted their project to IPRM!
class Loader(ABC):
    def __init__(self, project_dir: str, platform: str):
        super().__init__()
        self._project_dir = project_dir
        self._platform = platform
        self._platform_ctx = PLAT_CONTEXT_TYPE[platform]
        self._log_sink = ConsoleLogSink()

    @abstractmethod
    def load_project(self) -> dict[str, list[Object]]:
        pass

    @abstractmethod
    def load_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def file_name(self) -> str:
        pass

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def platform(self):
        return self._platform

    @property
    def log_sink(self):
        return self._log_sink
