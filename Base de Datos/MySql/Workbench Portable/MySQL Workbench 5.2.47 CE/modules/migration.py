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

import grt
import mforms
from workbench import db_utils

from workbench.utils import replace_string_parameters

class MigrationTarget(object):
    def __init__(self, state, connection):
        self.state = state
        self._rdbms = None
        self.password = None
        
        self._set_connection(connection)

    def _get_rdbms(self): return self._rdbms

    def _set_rdbms(self, rdbms):
        if rdbms.name != "Mysql":
            raise ValueError("Unsupported target RDBMS \"%s\"" % rdbms.name)
        self._rdbms = rdbms

    rdbms = property(_get_rdbms, _set_rdbms)

    def _get_catalog(self): return self.state.targetCatalog
    
    def _set_catalog(self, catalog):
        self.state.targetCatalog = catalog

    catalog = property(_get_catalog, _set_catalog)

    def _get_connection(self):
        return self.state.targetConnection

    connection = property(_get_connection)

    def _set_connection(self, connection):
        if not connection.driver or not connection.driver.owner:
            raise ValueError('Invalid connection object')
        self.state.targetConnection = connection
        self._rdbms = connection.driver.owner

    def checkConnection(self):
        self.module_fe().connect(self.connection, self.password or "")
        return True

    def checkVersion(self):
        self.state.targetDBVersion = self.module_fe().getServerVersion(self.connection)
        
        self.state.targetVersion = grt.classes.GrtVersion()
        self.state.targetVersion.name = self.state.targetDBVersion.name
        self.state.targetVersion.majorNumber = self.state.targetDBVersion.majorNumber
        self.state.targetVersion.minorNumber = self.state.targetDBVersion.minorNumber
        self.state.targetVersion.releaseNumber = self.state.targetDBVersion.releaseNumber

    def connect(self):
        return grt.modules.DbMySQLFE.connect(self.connection, self.password or "")

    def disconnect(self):
        return grt.modules.DbMySQLFE.disconnect(self.connection)

    def module_fe(self):
        return grt.modules.DbMySQLFE

    def module_re(self):
        return grt.modules.DbMySQLRE
    
    def module_migration(self):
        return grt.modules.DbMySQLMigration
    
    def module_db(self):
        return grt.modules.DbMySQL


class MigrationSource(object):
    def __init__(self, state, connection):
        self.state = state
        self._rdbms = None
        self._rev_eng_module = None
        self._migration_module = None
        self._db_module = None
        self._catalog_name = None
        self.password = None
        self.migration = None

        self._set_connection(connection)


    def _get_rdbms(self): return self._rdbms

    def _set_rdbms(self, rdbms):
        self._rdbms = rdbms

        self._rev_eng_module = None
        self._db_module = None
        self._migration_module = None

        for mname in dir(grt.modules):
            mod = getattr(grt.modules, mname)
            if not hasattr(mod, "getTargetDBMSName") or mod.getTargetDBMSName() != rdbms.name:
                continue
            name = mod.__name__
            if name.startswith("Db") and hasattr(mod, "reverseEngineer"):
                self._rev_eng_module = mod
            if name.startswith("Db") and hasattr(mod, "migrateCatalog"):
                self._migration_module = mod

            if name.startswith("Db") and hasattr(mod, "fullyQualifiedObjectName"):
                self._db_module = mod

        if not self._rev_eng_module or not self._db_module or not self._migration_module:
            raise ValueError('Source RDBMS "%s" not supported' % rdbms.name)

        self.migration = self._migration_module
    
    rdbms = property(_get_rdbms, _set_rdbms)

    def _get_catalog(self): return self.state.sourceCatalog
    
    catalog = property(_get_catalog)

    def _get_connection(self):
        return self.state.sourceConnection

    def _set_connection(self, connection):
        if not connection.driver or not connection.driver.owner:
            raise ValueError('Invalid connection object')
        self.state.sourceConnection = connection
        self._set_rdbms(connection.driver.owner)

    connection = property(_get_connection, _set_connection)



    def _get_selected_schemata(self):
        return self.state.selectedSchemataNames

    def _set_selected_schemata(self, names):
        self.state.selectedSchemataNames.remove_all()
        for name in names:
            self.state.selectedSchemataNames.append(name)

    selectedSchemataNames = property(_get_selected_schemata, _set_selected_schemata)


    def _set_selected_catalog(self, name):
        self._catalog_name = name

    def _get_selected_catalog(self):
        return self._catalog_name
    
    selectedCatalogName = property(_get_selected_catalog, _set_selected_catalog)


    def _get_ignore_list(self):
        return self.state.ignoreList

    def _set_ignore_list(self, ilist):
        self.state.ignoreList = ilist

    ignoreList = property(_get_ignore_list, _set_ignore_list)

    def connect(self):
        return self._rev_eng_module.connect(self.connection, self.password or "")

    def disconnect(self):
        return self._rev_eng_module.disconnect(self.connection)
        
    def checkVersion(self):
        self.state.sourceDBVersion = self.module_re().getServerVersion(self.connection)

    def getCatalogNames(self):
        return self._rev_eng_module.getCatalogNames(self.connection)

    def getSchemaNames(self, catalog):
        return self._rev_eng_module.getSchemaNames(self.connection, catalog or '')

    def getTableNames(self, catalog, schema):
        return self._rev_eng_module.getTableNames(self.connection, catalog or '', schema)

    def module_re(self):
        return self._rev_eng_module
    
    def module_migration(self):
        return self._migration_module
    
    def module_db(self):
        return self._db_module


    # For Migration Workflow
    @property
    def schemaNames(self):
        return self.state.sourceSchemataNames
    

    def doFetchSchemaNames(self, only_these_catalogs=[]):
        """Fetch list of schema names in catalog.schema format and stores them in the migration.sourceSchemataNames node"""
        
        grt.send_progress(0.0, "Checking connection...")
        self.connect()
        if self.rdbms.doesSupportCatalogs:
            grt.send_progress(0.1, "Fetching catalog names...")
            self.state.sourceSchemataNames.remove_all()
            catalog_names = self.getCatalogNames()
            if only_these_catalogs:
                inexistent_catalogs = set(only_these_catalogs).difference(catalog_names)
                if inexistent_catalogs:
                    grt.send_warning('The following catalogs where not found: ' + ', '.join(list(inexistent_catalogs)))
                catalog_names = list(set(only_these_catalogs).difference(inexistent_catalogs)) or self.getCatalogNames()
            self._catalog_names = catalog_names
            grt.send_progress(0.1, "Fetching schema names...")
            i = 0.0
            accumulated_progress = 0.1
            step_progress_share = 1.0 / (len(catalog_names) + 1e-10)
            for catalog in catalog_names:
                grt.send_progress(accumulated_progress, 'Fetching schema names from %s...' % catalog)
                schema_names = self.getSchemaNames(catalog)
                for schema in schema_names:
                    self.state.sourceSchemataNames.append("%s.%s" % (catalog, schema))
                accumulated_progress += 0.9 * step_progress_share
        else:  # The rdbms doesn't support catalogs
            grt.send_progress(0.1, "Fetching schema names...")
            schema_names = self.getSchemaNames('')
            if only_these_catalogs:  # Here only_these_catalogs would rather mean only these schemata
                inexistent_schemata = set(only_these_catalogs).difference(schema_names)
                if inexistent_schemata:
                    grt.send_warning('The following schemata where not found: ' + ', '.join(list(inexistent_schemata)))
                schema_names = list(set(only_these_catalogs).difference(inexistent_schemata))  or self.getSchemaNames('')
            self._catalog_names = []
            self.state.sourceSchemataNames.remove_all()
            for schema in schema_names:
                self.state.sourceSchemataNames.append('def.%s' % schema)
        grt.send_progress(1.0, "Finished")


    @property
    def supportedObjectTypes(self):
        if hasattr(self._rev_eng_module, 'getSupportedObjectTypes'):
            allTypes = list(self._rev_eng_module.getSupportedObjectTypes())
        else:
            allTypes = [("tables", "db.Table", "Tables"), 
                        ("views", "db.View", "Views"), 
                        ("routines", "db.Routine", "Routines"), 
                        ("routineGroups", "db.RoutineGroup", "Routine Groups"),
                        ("synonyms", "db.Synonym", "Synonyms"),
                        ("structuredTypes", "db.StructuredType", "Structured Types"),
                        ("sequences", "db.Sequence", "Sequences")]
        supported = allTypes[:1] # always show table group, even if there's none
        for item in allTypes[1:]:
            t = item[0]
            for schema in self.catalog.schemata:
                objects = getattr(schema, t, False)
                if objects and len(objects) > 0:
                    supported.append(item)
                    break
        return supported


    def allObjectsOfType(self, otype):
        l = []
        for schema in self.catalog.schemata:
            objects = getattr(schema, otype)
            for obj in objects:
                l.append("%s.%s" % schema.name, obj.name)
        return l

    def availableObjectsOfType(self, otype):
        l = []
        for ignore_spec in self.ignoreList:
            t, sep, obj = ignore_spec.split(":")
            if t == otype:
                l.append(obj)
        return l

    def selectedObjectsOfType(self, otype):
        l = []
        for schema in self.catalog.schemata:
            objects = getattr(schema, otype)
            for obj in objects:
                ignore_spec = "%s:%s.%s" % (otype, schema.name, obj.name)
                if ignore_spec not in self.ignoreList:
                    l.append("%s.%s" % (schema.name, obj.name))
        return l


    def setIgnoredObjectsOfType(self, otype, iglist):
        for i in reversed(range(len(self.ignoreList))):
            if self.ignoreList[i].startswith(otype+":"):
                del self.ignoreList[i]
        for item in iglist:
            self.ignoreList.append("%s:%s" % (otype, item))


    def setIgnoreObjectType(self, otype, flag):
        for i in reversed(range(len(self.ignoreList))):
            if self.ignoreList[i].startswith(otype+":"):
                del self.ignoreList[i]
        if flag:
            self.ignoreList.append("%s:*" % otype)


    def isObjectTypeIgnored(self, otype):
        return "%s:*" % otype in self.ignoreList

    def isObjectIgnored(self, otype, obj):
        if "%s:*" % otype in self.ignoreList or "%s:%s.%s" % (otype, obj.owner.name, obj.name) in self.ignoreList:
            return True
        return False

    def reverseEngineer(self):
        """Perform reverse engineering of selected schemas into the migration.sourceCatalog node"""
        self.connect()
        
        grt.send_info("Reverse engineering %s from %s" % (", ".join(self.selectedSchemataNames), self.selectedCatalogName))
        self.state.sourceCatalog = self._rev_eng_module.reverseEngineer(self.connection, self.selectedCatalogName, self.selectedSchemataNames, self.state.applicationData)



class MigrationPlan(object):

    def __init__(self):
        self.state = grt.root.wb.migration
        if not self.state:
            self.state = grt.classes.db_migration_Migration()
            self.state.owner = grt.root.wb
            grt.root.wb.migration = self.state

            datadir = mforms.App.get().get_user_data_folder()
            path = datadir + "/migration_generic_typemap.xml"
            import os
            if os.path.exists(path):
                self.state.genericDatatypeMappings.extend(grt.unserialize(path))
            else:
                global_path = mforms.App.get().get_resource_path("")
                global_path += "/modules/data/migration_generic_typemap.xml"
                if os.path.exists(global_path):
                    self.state.genericDatatypeMappings.extend(grt.unserialize(global_path))

        self.migrationSource = None
        self.migrationTarget = None
        
        import sys
        if sys.platform == "win32":
            self.wbcopytables_path = mforms.App.get().get_executable_path("wbcopytables.exe")
        elif sys.platform == "darwin":
            self.wbcopytables_path = mforms.App.get().get_executable_path("wbcopytables")
        else:
            self.wbcopytables_path = mforms.App.get().get_executable_path("wbcopytables")
            if not os.path.exists(self.wbcopytables_path):
                self.wbcopytables_path = os.path.join(os.path.dirname(grt.root.wb.registry.appExecutablePath), "wbcopytables")
            if not os.path.exists(self.wbcopytables_path):
                self.wbcopytables_path = "wbcopytables"
        if type(self.wbcopytables_path) == unicode:
            self.wbcopytables_path = self.wbcopytables_path.encode("UTF-8")

    def close(self):
        self.state.owner = None
        grt.root.wb.migration = None
        self.state = None
        self.migrationSource = None
        self.migrationTarget = None

        
    @staticmethod
    def is_rdbms_migratable(rdbms):
        rev_eng_module = None
        migration_module = None
        db_module = None
        for mname in dir(grt.modules):
            mod = getattr(grt.modules, mname)
            if not hasattr(mod, "getTargetDBMSName") or mod.getTargetDBMSName() != rdbms.name:
                continue
            name = mod.__name__
            if name.startswith("Db") and hasattr(mod, "reverseEngineer"):
                rev_eng_module = mod
            if name.startswith("Db") and hasattr(mod, "migrateCatalog"):
                migration_module = mod

            if name.startswith("Db") and hasattr(mod, "fullyQualifiedObjectName"):
                db_module = mod
        
        if not rev_eng_module:
            grt.log_debug2("Migration", "RDBMS %s cannot be a migration source because it's missing a RE module\n" % rdbms.name)
        if not migration_module:
            grt.log_debug2("Migration", "RDBMS %s cannot be a migration source because it's missing a Migration module\n" % rdbms.name)
        if not db_module:
            grt.log_debug2("Migration", "RDBMS %s cannot be a migration source because it's missing a Db information module\n" % rdbms.name)
        
        return rev_eng_module and migration_module and db_module


    @staticmethod
    def supportedSources():
        sources = []
        for rdbms in grt.root.wb.rdbmsMgmt.rdbms:
            if MigrationPlan.is_rdbms_migratable(rdbms):
                sources.append(rdbms)
        return sources


    @staticmethod
    def supportedTargets():
        return grt.root.wb.rdbmsMgmt.rdbms[0]


    def setSourceConnection(self, connection):
        if self.migrationSource:
            self.migrationSource.connection = connection
        else:
            self.migrationSource = MigrationSource(self.state, connection)

    def setTargetConnection(self, connection):
        self.migrationTarget = MigrationTarget(self.state, connection)
        self.migrationTarget.rdbms = connection.driver.owner

    @property
    def targetCatalog(self):
        return self.state.targetCatalog

    @property
    def sourceCatalog(self):
        return self.state.sourceCatalog

    def migrate(self):
        # clear the migration log
        self.state.migrationLog.remove_all()

        self.migrationTarget.catalog = self.migrationSource.migration.migrateCatalog(self.state, self.migrationSource.catalog)
        
        report = {
        }
        return report


    def generateSQL(self):
        grt.modules.DbMySQLFE.generateSQLCreateStatements(self.migrationTarget.catalog, self.state.targetVersion, self.state.objectCreationParams)
        
        report = {
        "schemata": 0
        }
        return report


    def createTargetScript(self, path):
        grt.modules.DbMySQLFE.createScriptForCatalogObjects(path, self.migrationTarget.catalog, self.state.objectCreationParams)


    def createTarget(self):
        self.state.creationLog.remove_all()
        return grt.modules.DbMySQLFE.createCatalogObjects(self.migrationTarget.connection, self.migrationTarget.catalog, self.state.objectCreationParams, self.state.creationLog)


