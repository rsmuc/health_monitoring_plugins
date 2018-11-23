# Some general rules for our plugins (DRAFT)

* UOMs: The units of the metrics are not written in the UOM field. We write them in the label.
The offical supported UOMs are too limites

* Each status that is processes, will be written to the long output if it is ok. If it is not OK, we
 will write it to the summary

 * Plugins will process all checks with one call. So we need usually only one service per monitored
 device. Except if the plugin will be used to execute event handlers. Then every check that
 will be done, will result in a single service. e.g. for Eaton UPS.