# -*- coding: utf-8 -*-
import os
import platform
import socket
import sys
from collections import OrderedDict

from . import renderers

__version__ = '1.0.1'

optional_modules_list = [
    'Cookie',
    'zlib', 'gzip', 'bz2', 'zipfile', 'tarfile',
    'ldap',
    'socket',
    'audioop', 'curses', 'imageop', 'aifc', 'sunau', 'wave', 'chunk',
    'colorsys', 'rgbimg', 'imghdr', 'sndhdr', 'ossaudiodev', 'sunaudiodev',
    'adodbapi', 'cx_Oracle', 'ibm_db', 'mxODBC', 'MySQLdb', 'pgdb', 'PyDO',
    'sapdbapi', 'sqlite3'
]
for i in optional_modules_list:
    try:
        module = __import__(i)
        sys.modules[i] = module
        globals()[i] = module
    except:
        pass

_PYTHON_MAJOR = sys.version_info[0]


def try_exec(fn):
    """Execute function and handles exceptions as error."""
    try:
        return fn()
    except Exception as e:
        return "Error: {}".format(repr(e))


def imported(module):
    if module in sys.modules:
        return 'enabled'
    return 'disabled'


def python_info():
    data = OrderedDict()
    data['System information'] = collect_system_info()
    data['Python internals'] = collect_py_internals()
    data['OS internals'] = collect_os_internals()
    data['Environment variables'] = collect_environ()
    data['Database support'] = collect_database()
    data['Compression and archiving'] = collect_compression()
    if 'ldap' in sys.modules:
        data['LDAP support'] = collect_ldap()

    if 'socket' in sys.modules:
        data['Socket'] = collect_socket_info()

    data['Multimedia support'] = collect_multimedia_info()
    data['Copyright'] = sys.copyright
    return data


def collect_system_info():
    """Return system information."""
    data = OrderedDict()
    data['Python version'] = platform.python_version()
    if hasattr(sys, 'subversion'):
        data['Python Subversion'] = ', '.join(sys.subversion)

    if platform.dist()[0] != '' and platform.dist()[1] != '':
        osversion = '{} {} ({} {})'.format(platform.system(),
                                           platform.release(),
                                           platform.dist()[0].capitalize(),
                                           platform.dist()[1])
    else:
        osversion = '{} {}'.format(platform.system(), platform.release())
    data['OS Version'] = osversion

    if hasattr(sys, 'executable'):
        data['Executable'] = sys.executable
    data['Build Date'] = platform.python_build()[1]
    data['Compiler'] = platform.python_compiler()
    if hasattr(sys, 'api_version'):
        data['Python API'] = sys.api_version
    return data


def collect_py_internals():
    """Return python internal informations."""
    data = OrderedDict()
    if hasattr(sys, 'builtin_module_names'):
        data['Built-in Modules'] = ', '.join(sys.builtin_module_names)
    data['Byte Order'] = sys.byteorder + ' endian'
    if hasattr(sys, 'getcheckinterval'):
        data['Check Interval'] = sys.getcheckinterval()
    if hasattr(sys, 'getfilesystemencoding'):
        data['File System Encoding'] = sys.getfilesystemencoding()
    if _PYTHON_MAJOR < 3:
        hex_maxint = str(hex(sys.maxint)).upper().replace("X", "x")
        data['Maximum Integer Size'] = '{} ({})'.format(sys.maxint, hex_maxint)
    if hasattr(sys, 'getrecursionlimit'):
        data['Maximum Recursion Depth'] = sys.getrecursionlimit()
    if hasattr(sys, 'tracebacklimit'):
        data['Maximum Traceback Limit'] = sys.tracebacklimit
    else:
        data['Maximum Traceback Limit'] = '1000'
    data['Maximum Unicode Code Point'] = sys.maxunicode
    return data


def collect_os_internals():
    data = OrderedDict()
    if hasattr(os, 'getcwd'):
        data['Current Working Directory'] = try_exec(os.getcwd)

    if hasattr(os, 'getegid'):
        data['Effective Group ID'] = try_exec(os.getegid)

    if hasattr(os, 'geteuid'):
        data['Effective User ID'] = try_exec(os.geteuid)

    if hasattr(os, 'getgid'):
        data['Group ID'] = try_exec(os.getgid)

    if hasattr(os, 'getgroups'):
        data['Group Membership'] = try_exec(lambda: ', '.join(map(str, os.getgroups())))

    if hasattr(os, 'linesep'):
        data['Line Seperator'] = repr(os.linesep)[1:-1]

    if hasattr(os, 'getloadavg'):
        data['Load Average'] = try_exec(lambda: ', '.join(map(str, map(lambda x: round(x, 2), os.getloadavg()))))

    if hasattr(os, 'pathsep'):
        data['Path Seperator'] = os.pathsep

    if hasattr(os, 'getpid') and hasattr(os, 'getppid'):
        data['Process ID'] = try_exec(lambda: '{} (parent: {})'.format(os.getpid(), os.getppid()))

    if hasattr(os, 'getuid'):
        data['User ID'] = try_exec(os.getuid)
    return data


def collect_environ():
    """Return environment vars."""
    envvars = os.environ.keys()
    if _PYTHON_MAJOR > 2:
        envvars = list(envvars)
    envvars.sort()
    data = OrderedDict()
    for envvar in envvars:
        data[envvar] = str(os.environ[envvar])
    return data


def collect_database():
    """Return database support information."""
    data = OrderedDict()
    data['DB2/Informix (ibm_db)'] = imported('ibm_db')
    data['MSSQL (adodbapi)'] = imported('adodbapi')
    data['MySQL (MySQL-Python)'] = imported('MySQLdb')
    data['ODBC (mxODBC)'] = imported('mxODBC')
    data['Oracle (cx_Oracle)'] = imported('cx_Oracle')
    data['PostgreSQL (PyGreSQL)'] = imported('pgdb')
    data['Python Data Objects (PyDO)'] = imported('PyDO')
    data['SAP DB (sapdbapi)'] = imported('sapdbapi')
    data['SQLite3'] = imported('sqlite3')
    return data


def collect_compression():
    data = OrderedDict()
    data['Bzip2 Support'] = imported('bz2')
    data['Gzip Support'] = imported('gzip')
    data['Tar Support'] = imported('tarfile')
    data['Zip Support'] = imported('zipfile')
    data['Zlib Support'] = imported('zlib')
    return data


def collect_ldap():
    """Return ldap module information."""
    data = OrderedDict()
    data['Python-LDAP Version'] = ldap.__version__
    data['API Version'] = ldap.API_VERSION
    data['Default Protocol Version'] = ldap.VERSION
    data['Minimum Protocol Version'] = ldap.VERSION_MIN
    data['Maximum Protocol Version'] = ldap.VERSION_MAX
    data['SASL Support (Cyrus-SASL)'] = ldap.SASL_AVAIL
    data['TLS Support (OpenSSL)'] = ldap.TLS_AVAIL
    data['Vendor Version'] = ldap.VENDOR_VERSION
    return data


def collect_socket_info():
    """Return information available from socket library."""
    data = OrderedDict()
    data['Hostname'] = try_exec(socket.gethostname)

    hostname = try_exec(lambda: socket.gethostbyaddr(socket.gethostname())[0])
    data['Hostname (fully qualified)'] = hostname

    ip_addr = try_exec(lambda: socket.gethostbyname(socket.gethostname()))
    data['IP Address'] = ip_addr

    data['IPv6 Support'] = getattr(socket, 'has_ipv6', False)
    data['SSL Support'] = hasattr(socket, 'ssl')
    return data


def collect_multimedia_info():
    """Return multimedia related information."""
    data = OrderedDict()
    data['AIFF Support'] = imported('aifc')
    data['Color System Conversion Support'] = ('colorsys')
    data['curses Support'] = imported('curses')
    data['IFF Chunk Support'] = imported('chunk')
    data['Image Header Support'] = imported('imghdr')
    data['OSS Audio Device Support'] = imported('ossaudiodev')
    data['Raw Audio Support'] = imported('audioop')
    data['Raw Image Support'] = imported('imageop')
    data['SGI RGB Support'] = imported('rgbimg')
    data['Sound Header Support'] = imported('sndhdr')
    data['Sun Audio Device Support'] = imported('sunaudiodev')
    data['Sun AU Support'] = imported('sunau')
    data['Wave Support'] = imported('wave')
    return data


def info_as_text():
    info = python_info()
    return renderers.render_text(info)


def info_as_html():
    info = python_info()
    return renderers.render_html(info)


def print_info():
    """Cli program main."""
    print(info_as_text())

if __name__ == '__main__':
    print_info()
