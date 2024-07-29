# Yet Another PYANG
An open source Python package that helps developers to translate YANG (RFC6020/RFC7950) data models to Python. YAPYANG mimics the functionality of YANG data structures, enforces types through annotations, and supports JSON/XML ser/des. YAPYANG is authored by [Antonio Faria](https://github.com/movedempackets), governed as a [benevolent dictatorship](CODE_OF_CONDUCT.md), and distributed under [license](LICENSE)

> [!WARNING]
> YAPYANG is in construction, during this time no effort shall be afforded to migrations and backwards compatibility. See [versioning](#versioning).

## Quick Start
For convenience we've included a basic quick start below. Ensure that a supported version of [Python](https://devguide.python.org/versions/) and the latest version of [YAPYANG](https://github.com/nomios-opensource/yapyang/releases/latest) is installed.

Start by choosing the YANG model to translate. We've simplified OpenConfig interfaces.

```text
module openconfig-interfaces {
    namespace "http://openconfig.net/yang/interfaces";
    container interfaces {
        list interface {
            key "name";
            leaf name {
                type string;
            }
        }
    }
}
```
For each YANG node (module, container, list, and leaf) in the YANG model translate it into Python with YAPYANG through subclasses of the provided node types.

```py
from yapyang import *

class Name(LeafNode):
    __identifier__ = "name"

    value: str

class Interface(ListNode):

    __identifier__ = "interface"
    __key__ = "name"

    name: Name

class Interfaces(ContainerNode):
    __identifier__ = "interfaces"

    interface: Interface

class OpenConfigInterfaces(ModuleNode):

    __identifier__ = "openconfig-interfaces"
    __namespace__ = "http://openconfig.net/yang/interfaces"

    interfaces: Interfaces
```
Create instances of the translated YANG model nodes, add interface entries, and serialize to XML. Read the full [docs]().

```py

module = OpenConfigInterfaces(Interfaces(Interface()))
module.interfaces.interface.append(Name("xe-0/0/0"))
print(module.to_xml())
...

<interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>xe-0/0/0</name></interface></interfaces>

```

## Versioning
Releases will follow semantic versioning (major.minor.patch). Before 1.0.0 breaking changes can be included in a minor release, therefore we highly recommend pinning this package.

## Contributing
Suggest a [feature]() or report a [bug](). Read our developer [guide](CONTRIBUTING.md).

## License
YAPYANG is distributed under the Apache 2.0 [license](LICENSE).