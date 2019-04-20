# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Copyright (C) 2019 Richard Duivenvoorde, Nyall Dawson
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------


from qgis.PyQt.QtCore import (
    QCoreApplication,
    Qt
)
from qgis.PyQt.QtGui import (
    QIcon,
    QKeySequence
)
from qgis.PyQt.QtWidgets import (
    QAction,
    QMessageBox,
    QShortcut
)

from .log_dock_widget import NetworkActivityDock
from .activity_logger import NetworkActivityLogger

import os
'''
Some magic to make it possible to use code like:

log = logging.getLogger('QgisNetworkLogger')
log.debug('foo')

in all this plugin code, and it will show up in the QgsMessageLog

'''
import logging
from qgis.core import (
    Qgis,
    QgsMessageLog
)
class QgisLogHandler(logging.StreamHandler):
    def __init__(self, topic):
        logging.StreamHandler.__init__(self)
        # topic is used both as logger id and for tab
        self.topic = topic

    def emit(self, record):
        msg = self.format(record)
        # Below makes sure that logging of 'self' will show the repr of the object
        # Without this it will not be shown because it is something like
        # <qgisnetworklogger.plugin.QgisNetworkLogger object at 0x7f580dac6b38>
        # which looks like an html element so is not shown in the html panel
        msg=msg.replace('<', '&lt;').replace('>', '&gt;')
        QgsMessageLog.logMessage('{}'.format(msg), self.topic, Qgis.Info)

log = logging.getLogger('QgisNetworkLogger')
# checking below is needed, else we add this handler every time the plugin
# is reloaded (during development) so the msg is emitted several times
if not log.hasHandlers():
    log.addHandler(QgisLogHandler('QgisNetworkLogger'))


# set logging level (NOTSET = no, else: DEBUG or INFO)
log.setLevel(logging.DEBUG)

class QgisNetworkLogger:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # don't wait for GUI to start logging...
        self.logger = NetworkActivityLogger()
        self.dock = None

    def initGui(self):
        # Create action that will start the plugin
        self.action = QAction(QIcon(os.path.dirname(__file__) + '/icons/icon.png'), '&QGIS Network Logger',
                              self.iface.mainWindow())
        # connect the action to the run method
        #self.action.triggered.connect(self.show_dialog)
        self.action.triggered.connect(self.toggle_dock)
        # Add menu item
        self.iface.addPluginToMenu('QGIS Network Logger', self.action)
        self.iface.addToolBarIcon(self.action)

        # Create a shortcut (not working after reload ??)
        self.f12 = QKeySequence("F12")
        self.show_dock_shortcut = QShortcut(self.f12, self.iface.mainWindow())
        self.show_dock_shortcut.activated.connect(self.toggle_dock)

    def unload(self):
        # Remove the plugin menu item and button
        self.iface.removePluginMenu('QGIS Network Logger', self.action)
        self.iface.removeToolBarIcon(self.action)

        # trying to remove shortcut...
        self.show_dock_shortcut.activated.disconnect(self.toggle_dock)
        del self.show_dock_shortcut

        if self.dock:
            self.iface.removeDockWidget(self.dock)

    def toggle_dock(self):
        if not self.dock:
            self.dock = NetworkActivityDock(self.logger)
            self.dock.setObjectName('NetworkActivityDock')
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        else:
            self.dock.toggleUserVisible()

    def show_dialog(self):
        QMessageBox.information(
            self.iface.mainWindow(),
            QCoreApplication.translate('QGISNetworkLogger', 'QGIS Network Logger'),
            QCoreApplication.translate('QGISNetworkLogger', 'See LogMessages Panel.\n\n'
                                                            'Note that not ALL messages are seen here...\n\n'
                                                            'Only listening to the requestAboutToBeCreated and requestTimedOut signals.\n\n'
                                                            'if you want more: see code'))
        self.toggle_dock()
        return
