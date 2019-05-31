Experimental QGIS plugin to be able to see the request QGIS is firing to for example OGC services

A BIG thanks goes to Nyall Dawson!! Current Treeview is his idea and work!

Features (see screenshot below):
- Show all requests fired via QgsNetworkAccessManager in a TreeView
- Filter requests
- Show HTTP Operation, status, query, headers from Request and Reply and data/conent from Request
- Copy the request as cURL, to be able to replay the request (with all headers, data etc etc) in terminal
- Pause the logging/listening
- See from which thread the request originated
- See from which file and line in code the request originated

Current limitations:
- a lot, please add feature requests as issue :-)

To use:
- install plugin
- open the Network Activity panel (F12)
- open/edit some OGC OWS services

An Example:

![Example Log](/img/curllog.png)