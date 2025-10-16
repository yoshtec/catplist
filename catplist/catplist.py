#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

"""
Print .plist files

For documentation visit: https://github.com/yoshtec/catplist
"""

import datetime
import plistlib
import pprint
import re
import shutil
import sys
import uuid
from pathlib import Path
from plistlib import InvalidFileException

import click

UUID_REGEX = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z", re.I
)

# important keys
NS_TOP = "$top"
NS_OBJ = "$objects"
NS_ARC = "$archiver"
NS_CLASS = "$class"

NS_KEYS = "NS.keys"
NS_OBJECTS = "NS.objects"
NS_TIME = "NS.time"
NS_DATA = "NS.data"
NS_STRING = "NS.string"
NS_STRING2 = "NSString"
NS_ATTRIBUTE = "NSAttributes"

KEY_TITLE = "title"
KEY_ASSETS = "assetUUIDs"
KEY_UUID = "uuid"
KEY_TRASH = "isInTrash"
KEY_ASSETUUIDS = "assetUUIDs"
KEY_ROOT = "root"

TYPE_PHMFEATUREENCODER = "PHMemoryFeatureEncoder"
TYPE_NSKEYEDARCHIVER = "NSKeyedArchiver"

HEAD_PLIST = b"bplist00"
# Encountered in some ios PhotoMetadata files
HEAD_MALFORMED_PLIST = b"\n\xd3\x04bplist00"
HEAD_XZ = b"\xfd7zXZ"


def _is_plist(b: bytes):
    return b.startswith(HEAD_PLIST)


def _is_malformed_plist(b: bytes):
    return b.startswith(HEAD_MALFORMED_PLIST)


def _is_xz(b: bytes):
    return b.startswith(HEAD_XZ)


def _unwrap_bytes(b, uuids=False):
    if _is_xz(b):
        import lzma

        return unwrap(lzma.decompress(b))

    elif _is_plist(b):
        return unwrap(plistlib.loads(b))

    elif _is_malformed_plist(b):
        return unwrap(plistlib.loads(b[3:]))

    elif uuids:
        return _unwrap_uuids(b)

    else:
        return b


def _unwrap_uuids(b: bytes):
    return [uuid.UUID(bytes=b[i:i + 16]) for i in range(0, len(b), 16)]


def _unwrap_dict(d: dict, orig: list = None):
    if d is None:
        return {}

    if NS_STRING in d:
        return d[NS_STRING]

    if NS_STRING2 in d:
        return d[NS_STRING2]

    if NS_TIME in d:
        return datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=d[NS_TIME])

    if NS_ARC in d and NS_TOP in d and NS_OBJ in d:
        if d[NS_ARC] in [TYPE_NSKEYEDARCHIVER, TYPE_PHMFEATUREENCODER]:
            result_dict: dict = {}
            for t in d[NS_TOP]:
                index = d[NS_TOP][t]

                if isinstance(index, plistlib.UID):
                    index = index.data
                    data = d[NS_OBJ][index]
                    if type(data) is bytes:
                        result_dict[t] = _unwrap_bytes(data, str(t).endswith("UUIDs"))
                    else:
                        result_dict[t] = unwrap(data, d[NS_OBJ])
                else:
                    result_dict[t] = index

            # unpack single "root" dictionaries
            if KEY_ROOT in result_dict and len(result_dict) == 1:
                return result_dict[KEY_ROOT]

            return result_dict

    if NS_DATA in d:
        return unwrap(d[NS_DATA])

    if NS_KEYS in d and NS_OBJECTS in d:
        data2 = {}
        for k, v in zip(d[NS_KEYS], d[NS_OBJECTS]):
            # print(f"k,v:{k},{v}")
            k = unwrap(k, orig)
            v = unwrap(v, orig)
            # print(f"k,v:{k},{v}")
            data2[k] = v
        return data2

    if NS_OBJECTS in d:
        return [unwrap(v, orig) for v in d[NS_OBJECTS]]

    for t in d:
        d[t] = unwrap(d[t], orig)

    return d


def _unwrap_list(l: list, orig: list = None):
    if not l:
        return []

    return [unwrap(e, orig) for e in l]


def unwrap(x, orig: list = None):
    if x is None:
        return ""

    if isinstance(x, (int, float, bool)):
        return x

    try:

        if isinstance(x, plistlib.UID):
            x = x.data
            if orig is not None and len(orig) > x:
                x = unwrap(orig[x], orig)
            return x

        if isinstance(x, str):
            return uuid.UUID(x) if UUID_REGEX.match(x) else x

        if isinstance(x, dict):
            return _unwrap_dict(x, orig)

        if isinstance(x, list):
            return _unwrap_list(x, orig)

        if type(x) is bytes:
            return _unwrap_bytes(x)

        # Fallback just return the original
        return x

    except (RuntimeError, InvalidFileException) as r:
        return f"$ERROR: {r}"


def read_ns_archiver(plist=None):
    return unwrap(plist)


def read_plist(plist=None):

    if not plist:
        return {}

    return unwrap(plist)


class BaseMetadataFile:
    def __init__(self, file: Path = None, bytez: bytes = None):
        self.file = file
        self.raw_metadata = {}
        self.metadata = {}

        if file:
            if not self.file.is_file():
                raise RuntimeError(f"Path '{self.file}' is not a regular file)")

            with open(self.file, "rb") as f:
                self.raw_metadata = plistlib.load(f)

        # ``bytes`` is the built-in type and will always evaluate to ``True``.
        # The original code accidentally used it instead of the ``bytez``
        # argument which resulted in attempting to parse ``None`` and raising
        # an ``AttributeError`` when no file was supplied.  Use the parameter
        # instead so callers can initialise the class with raw plist bytes.
        elif bytez and _is_plist(bytez):
            self.raw_metadata = plistlib.loads(bytez)
        else:
            raise RuntimeError(
                f"Supplied file '{file}' is invalid and supplied bytes is not a plist"
            )

        self.metadata = unwrap(self.raw_metadata)

    def dump(self, raw=False):
        width, lines = shutil.get_terminal_size()
        md = self.raw_metadata if raw else self.metadata
        pprint.pp(md, width=width)

    def dump_json(self, raw=False):
        import json

        class UUIDEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, uuid.UUID):
                    # encode UUIDs using their standard string representation
                    return str(obj)
                return json.JSONEncoder.default(self, obj)

        md = self.raw_metadata if raw else self.metadata
        click.echo(json.dumps(md, cls=UUIDEncoder))

    def dump_yaml(self, raw=False):
        """Write a very small subset of YAML.

        The original project depended on ``ruamel.yaml`` for serialising output
        but the dependency is fairly heavy.  The tests only require dumping
        simple dictionaries so we implement a tiny serializer here to avoid the
        extra requirement while still producing human‑readable YAML.  It handles
        nested dictionaries and lists and falls back to ``str()`` for other
        objects such as :class:`uuid.UUID`.
        """

        md = self.raw_metadata if raw else self.metadata

        def _to_yaml(obj, indent=0):
            space = " " * indent
            if isinstance(obj, dict):
                lines = []
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        lines.append(f"{space}{key}:")
                        lines.append(_to_yaml(value, indent + 2))
                    else:
                        lines.append(f"{space}{key}: {value}")
                return "\n".join(lines)
            if isinstance(obj, list):
                lines = []
                for item in obj:
                    if isinstance(item, (dict, list)):
                        lines.append(f"{space}-")
                        lines.append(_to_yaml(item, indent + 2))
                    else:
                        lines.append(f"{space}- {item}")
                return "\n".join(lines)
            return f"{space}{obj}"

        click.echo(_to_yaml(md))


@click.command()
@click.argument(
    "file", nargs=-1, type=click.Path(exists=True, file_okay=True, readable=True)
)
@click.option(
    "--raw",
    "-R",
    default=False,
    is_flag=True,
    help="print raw plist contents, will not unpack nested data & plists",
)
@click.option(
    "--recurse",
    "-r",
    default=False,
    is_flag=True,
    help="recurse into subdirs, reads all files ignores non plist files",
)
@click.option(
    "--format",
    "-f",
    "fmt",
    default="python",
    type=click.Choice(["python", "json", "yaml"], case_sensitive=False),
    help="format output in ...",
)
def catplist(file, raw, recurse, fmt):
    """
    This is catplist: print plists for human reading and easy grepping.
    """

    stack: list = []
    if not file:
        click.echo(" - No file given! Usage: ", err=True)
        click.echo(" catplist file", err=True)
        return 1

    stack.extend(file)

    while len(stack) > 0:
        p = Path(stack.pop())
        if p.is_dir() and recurse:
            stack.extend(p.iterdir())
        elif p.is_file():
            try:
                pm = BaseMetadataFile(p)
                if fmt == "json":
                    pm.dump_json(raw)
                elif fmt == "yaml":
                    pm.dump_yaml(raw)
                else:
                    pm.dump(raw)
            except InvalidFileException as i:
                click.echo(f" - is not a valid plist. Skipping over Error '{i}'.", err=True)
    sys.exit(0)


if "__main__" == __name__:
    sys.exit(catplist())
