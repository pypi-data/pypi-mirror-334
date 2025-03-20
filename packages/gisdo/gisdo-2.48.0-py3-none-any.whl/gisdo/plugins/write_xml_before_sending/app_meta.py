from m3.plugins import (
    ExtensionHandler,
    ExtensionManager,
    ExtensionPoint,
)

from .extensions import (
    write_xml,
)


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(
        ExtensionPoint(name='write_xml', default_listener=ExtensionHandler(handler=write_xml))
    )
