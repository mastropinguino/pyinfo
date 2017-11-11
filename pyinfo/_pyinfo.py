# -*- coding: utf-8 -*-
import os
import platform
import socket
import sys

from . import renderers

__version__ = '1.0.0'

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


def imported(module):
    if module in sys.modules:
        return 'enabled'
    return 'disabled'


def python_info():
    data = dict()
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
    data = dict()
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
    data = dict()
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
    data = dict()
    if hasattr(os, 'getcwd'):
        data['Current Working Directory'] = os.getcwd()
    if hasattr(os, 'getegid'):
        data['Effective Group ID'] = os.getegid()
    if hasattr(os, 'geteuid'):
        data['Effective User ID'] = os.geteuid()
    if hasattr(os, 'getgid'):
        data['Group ID'] = os.getgid()
    if hasattr(os, 'getgroups'):
        data['Group Membership'] = ', '.join(map(str, os.getgroups()))
    if hasattr(os, 'linesep'):
        data['Line Seperator'] = repr(os.linesep)[1:-1]
    if hasattr(os, 'getloadavg'):
        data['Load Average'] = ', '.join(map(str, map(lambda x: round(x, 2), os.getloadavg())))
    if hasattr(os, 'pathsep'):
        data['Path Seperator'] = os.pathsep
    try:
        if hasattr(os, 'getpid') and hasattr(os, 'getppid'):
            data['Process ID'] = '{} (parent: {})'.format(os.getpid(), os.getppid())
    except:
        pass
    if hasattr(os, 'getuid'):
        data['User ID'] = os.getuid()
    return data


def collect_environ():
    """Return environment vars."""
    envvars = os.environ.keys()
    if _PYTHON_MAJOR > 2:
        envvars = list(envvars)
    envvars.sort()
    data = dict()
    for envvar in envvars:
        data[envvar] = str(os.environ[envvar])
    return data


def collect_database():
    """Return database support information."""
    data = dict()
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
    data = dict()
    data['Bzip2 Support'] = imported('bz2')
    data['Gzip Support'] = imported('gzip')
    data['Tar Support'] = imported('tarfile')
    data['Zip Support'] = imported('zipfile')
    data['Zlib Support'] = imported('zlib')
    return data


def collect_ldap():
    """Return ldap module information."""
    data = dict()
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
    data = dict()
    try:
        data['Hostname'] = socket.gethostname()
    except Exception as e:
        data['Hostname'] = 'Error: {}'.format(e)

    try:
        hostname = socket.gethostbyaddr(socket.gethostname())[0]
        data['Hostname (fully qualified)'] = hostname
    except Exception as e:
        data['Hostname (fully qualified)'] = 'Error: {}'.format(e)
    try:
        data['IP Address'] = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        data['IP Address'] = 'Error: {}'.format(e)

    data['IPv6 Support'] = getattr(socket, 'has_ipv6', False)
    data['SSL Support'] = hasattr(socket, 'ssl')
    return data


def collect_multimedia_info():
    """Return multimedia related information."""
    data = dict()
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
