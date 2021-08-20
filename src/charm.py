#!/usr/bin/env python3
# Copyright 2021 Caner Derici
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
#from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class CanercharmCharm(CharmBase):
    """Charm the service."""

    #_stored = StoredState() # <- to persist data across multiple instantiations of the class
    # (which happens every time the controller emits an event)

    def __init__(self, *args):
        super().__init__(*args)

        """ some common events
        install
        config-changed
        start
        upgrade-charm
        update-status
        <container>-pebble-ready
        stop
        remove
        collect-metrics
        """

        # install our callbacks for specific events
        # self.framework.observe(self.on.httpbin_pebble_ready, self._on_httpbin_pebble_ready)
        # self.framework.observe(self.on.config_changed, self._on_config_changed)
        # self.framework.observe(self.on.fortune_action, self._on_fortune_action)

        # self._stored.set_default(things=[]) # <-- setting the default in the controller DB

        # self.framework.observe(self.on.gosherve_pebble_ready, self._on_gosherve_pebble_ready)

        self.framework.observe(self.on.config_changed, self._on_config_changed)

    """
    SOME Juju OPS TRIGGERING SOME EVENTS

Deploy	"juju deploy ./canercharm.charm"	install -> config-changed -> start -> pebble-ready
Scale	"juju add-unit -n 2 canercharm" 	install -> config-changed -> start -> pebble-ready
Configure	"juju config canercharm thing=foo" 	config-changed
Upgrade	"juju upgrade-charm canercharm"  	upgrade-charm -> config-changed -> pebble-ready
Remove	"juju remove-application canercharm"	stop -> remove

    """

    """
    _on_[WHATEVER CONTAINER YOU WRITE IN METADATA.YAML]_pebble_ready
    """
    # don't need this anymore, since it was adding a layer and autostarting the service
    #                                    v---------speficit to a container
    def _on_gosherve_pebble_ready(self, event):
        # get a reference the container attribute on the PebbleReadyEvent
        container = event.workload

        # define an initial pebble layer config
        pebble_layer = None

        # add initial pebble config layer using the pebble API
        container.add_layer("gosherve", pebble_layer, combine=True)
        container.autostart()
        self.unit.status = ActiveStatus()


    def _on_config_changed(self, event):
        # get the container so we can configure/manipulate it
        container = self.unit.get_container("gosherve")
        # get a layer going
        layer = self._gosherve_layer()
        # get the current config
        plan = container.get_plan()
        services = plan.to_dict().get("services", {})
        if services != layer["services"]:
            # there are some changes
            container.add_layer("gosherve", layer, combine=True)
            logging.info("added updated layer 'gosherve' to Pebble plan------------------------------------")
            # stop the service if it's already running
            if container.get_service("gosherve").is_running():
                container.stop("gosherve")
            # restart it to get the config going, and report the new status to Juju
            container.start("gosherve")
            logging.info("restarted the gosherve service ---------------------------------------------")
        # we're good, set an ActiveStatus
        self.unit.status = ActiveStatus("we're good")

    def _gosherve_layer(self):
        return {
            "summary" : "gosherve layer",
            "description" : "pebble config layer for gosherve",
            "services" : {
                "gosherve" : {
                    "override" : "replace",
                    "summary" : "gosherve",
                    "command" : "/gosherve",
                    "startup" : "enabled",
                    "environment" : {
                        "REDIRECT_MAP_URL" : self.config["redirect-map"]
                    },
                }
            }
        }

    # def _on_httpbin_pebble_ready(self, event):
    #     """Define and start a workload using the Pebble API.
    #     Learn more about Pebble layers at https://github.com/canonical/pebble
    #     """
    #     # Get a reference the container attribute on the PebbleReadyEvent
    #     container = event.workload
    #     # Define an initial Pebble layer configuration
    #     pebble_layer = {
    #         "summary": "httpbin layer",
    #         "description": "pebble config layer for httpbin",
    #         "services": {
    #             "httpbin": {
    #                 "override": "replace",
    #                 "summary": "httpbin",
    #                 "command": "gunicorn -b 0.0.0.0:80 httpbin:app -k gevent",
    #                 "startup": "enabled",
    #                 "environment": {"thing": self.model.config["thing"]},
    #             }
    #         },
    #     }
    #     # Add intial Pebble config layer using the Pebble API
    #     container.add_layer("httpbin", pebble_layer, combine=True)
    #     # combine=True =======> If there's already a layer with the
    #     # same name (e.g. "httpbin") running on this Pebble instance,
    #     # then override it

    #     # Autostart any services that were defined with startup: enabled
    #     container.autostart()
    #     # Learn more about statuses in the SDK docs:
    #     # https://juju.is/docs/sdk/constructs#heading--statuses
    #     self.unit.status = ActiveStatus()
    #     """Report its own status to the Juju controller. There are 6 valid
    #     types, only 4 of them are accessible from charm code.

    #     from ops.model import <the 4 below>

    #     ActiveStatus("Everything is good")  <------- setting a msg is possible
    #     WaitingStatus
    #     MaintenanceStatus("Installing application packages, doing something, and gonna go back to ActiveStatus without any intervention")
    #     BlockedStatus("I need a human to recover me from something")
    #     * UnknownStatus
    #     * ErrorStatus

    #     """

    # def _on_config_changed(self, _):
    #     """Just an example to show how to deal with changed configuration.

    #     TEMPLATE-TODO: change this example to suit your needs.
    #     If you don't need to handle config, you can remove this method,
    #     the hook created in __init__.py for it, the corresponding test,
    #     and the config.py file.

    #     Learn more about config at https://juju.is/docs/sdk/config
    #     """
    #     current = self.config["thing"]
    #     if current not in self._stored.things:
    #         logger.debug("found a new thing: %r", current)
    #         self._stored.things.append(current)

    # def _on_fortune_action(self, event):
    #     """Just an example to show how to receive actions.

    #     TEMPLATE-TODO: change this example to suit your needs.
    #     If you don't need to handle actions, you can remove this method,
    #     the hook created in __init__.py for it, the corresponding test,
    #     and the actions.py file.

    #     Learn more about actions at https://juju.is/docs/sdk/actions
    #     """
    #     fail = event.params["fail"]
    #     if fail:
    #         event.fail(fail)
    #     else:
    #         event.set_results({"fortune": "A bug in the code is worth two in the documentation."})


if __name__ == "__main__":
    main(CanercharmCharm)
