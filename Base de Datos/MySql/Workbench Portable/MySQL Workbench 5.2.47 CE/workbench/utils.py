# Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

import re

def find_object_with_name(list, name):
    """Finds an object with the given name within a list of objects (such as grt.List).

    Returns the found object or None if there was no object with the given name in the collection.
    """
    for obj in list:
        if obj.name == name:
            return obj
    return None

def find_object_with_old_name(list, name):
    """Finds an object with the given oldName within a list of objects (such as grt.List).

    Returns the found object or None if there was no object with the given name in the collection.
    """
    for obj in list:
        if obj.oldName == name:
            return obj
    return None


def replace_string_parameters(template_string, params):
    if isinstance(params, dict):
        params = list( params.iteritems() )
    return reduce( lambda partial_template_string, rep_tuple: partial_template_string.replace('%'+rep_tuple[0]+'%', str(rep_tuple[1])),
                                [ template_string ] + params
                  )

def parameters_from_dsn(dsn):
    chunks = dsn.split(';')
    params = ( (name, value) for name, value in 
                    ( chunk.split('=', 1) for chunk in chunks if '=' in chunk )
                    if not (value.startswith('%') and value.endswith('%'))
             )
    return dict(params)

def dsn_parameters_to_connection_parameters(dsn_params):
    param_mapping = { 'DRIVER'  : 'driver',
                      'SERVER'  : 'hostName',
                      'UID'     : 'userName',
                      'PWD'     : 'password',
                      'PORT'    : 'port',
                      'DATABASE': 'schema',
                      'DSN'     : 'dsn',
                    }
    return dict( (param_mapping.get(dsn_key.upper(), dsn_key), dsn_value) for dsn_key, dsn_value in dsn_params.iteritems() )
    
    
def check_grt_subtree_consistency(value):
    pass

def server_version_str2tuple(version_str):
    match = re.match(r'^(\d+\.\d+(\.\d)*).*$', version_str.strip())
    if match:
        return tuple(int(x) for x in match.group(1).split('.'))
    return tuple()

def server_os_path(server_profile):
    """Returns an os.path module specific for the server OS."""
    if server_profile.target_is_windows:
        return __import__('ntpath')
    else:
        return __import__('posixpath')
