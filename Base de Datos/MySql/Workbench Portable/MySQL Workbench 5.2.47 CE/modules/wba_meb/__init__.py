# Copyright (c) 2012, 2013, Oracle and/or its affiliates. All rights reserved.
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


import wb_admin_meb
import wb_admin_meb_restore

from wb_admin_meb_common import WBBackupContext

def wba_register_disabled(server_profile, ctrl_be, main_view):
    context = WBBackupContext(server_profile, ctrl_be)

    main_view.add_taskbar_section("ENTERPRISE BACKUP")
    wb_admin_meb.register(context, main_view)
    wb_admin_meb_restore.register(context, main_view)
