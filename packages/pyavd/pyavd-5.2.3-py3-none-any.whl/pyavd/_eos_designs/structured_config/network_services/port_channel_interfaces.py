# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import re
from functools import cached_property
from typing import TYPE_CHECKING, Protocol

from pyavd._utils import append_if_not_duplicate, short_esi_to_route_target

if TYPE_CHECKING:
    from . import AvdStructuredConfigNetworkServicesProtocol


class PortChannelInterfacesMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    @cached_property
    def port_channel_interfaces(self: AvdStructuredConfigNetworkServicesProtocol) -> list | None:
        """
        Return structured config for port_channel_interfaces.

        Only used with L1 network services
        """
        if not self.shared_utils.network_services_l1:
            return None

        # Using temp variables to keep the order of interfaces from Jinja
        port_channel_interfaces = []
        subif_parent_interfaces = []

        for tenant in self.shared_utils.filtered_tenants:
            if not tenant.point_to_point_services:
                continue

            for point_to_point_service in tenant.point_to_point_services._natural_sorted():
                for endpoint in point_to_point_service.endpoints:
                    if self.shared_utils.hostname not in endpoint.nodes:
                        continue

                    node_index = endpoint.nodes.index(self.shared_utils.hostname)
                    interface_name = endpoint.interfaces[node_index]
                    if (port_channel_mode := endpoint.port_channel.mode) not in ["active", "on"]:
                        continue

                    channel_group_id = "".join(re.findall(r"\d", interface_name))
                    interface_name = f"Port-Channel{channel_group_id}"
                    if point_to_point_service.subinterfaces:
                        # This is a subinterface so we need to ensure that the parent is created
                        parent_interface = {
                            "name": interface_name,
                            "switchport": {"enabled": False},
                            "peer_type": "system",
                            "shutdown": False,
                        }
                        if (short_esi := endpoint.port_channel.short_esi) is not None and len(short_esi.split(":")) == 3:
                            parent_interface.update(
                                {
                                    "evpn_ethernet_segment": {
                                        "identifier": f"{self.inputs.evpn_short_esi_prefix}{short_esi}",
                                        "route_target": short_esi_to_route_target(short_esi),
                                    },
                                },
                            )
                            if port_channel_mode == "active":
                                parent_interface["lacp_id"] = short_esi.replace(":", ".")

                        subif_parent_interfaces.append(parent_interface)

                        for subif in point_to_point_service.subinterfaces:
                            subif_name = f"{interface_name}.{subif.number}"

                            port_channel_interface = {
                                "name": subif_name,
                                "peer_type": "point_to_point_service",
                                "encapsulation_vlan": {
                                    "client": {
                                        "encapsulation": "dot1q",
                                        "vlan": subif.number,
                                    },
                                    "network": {
                                        "encapsulation": "client",
                                    },
                                },
                                "shutdown": False,
                            }

                            append_if_not_duplicate(
                                list_of_dicts=port_channel_interfaces,
                                primary_key="name",
                                new_dict=port_channel_interface,
                                context="Port-Channel Interfaces defined under point_to_point_services",
                                context_keys=["name"],
                            )

                    else:
                        interface = {
                            "name": interface_name,
                            "switchport": {"enabled": False},
                            "peer_type": "point_to_point_service",
                            "shutdown": False,
                        }
                        if point_to_point_service.lldp_disable:
                            interface["lldp"] = {
                                "transmit": False,
                                "receive": False,
                            }

                        if (short_esi := endpoint.port_channel.short_esi) is not None and len(short_esi.split(":")) == 3:
                            interface.update(
                                {
                                    "evpn_ethernet_segment": {
                                        "identifier": f"{self.inputs.evpn_short_esi_prefix}{short_esi}",
                                        "route_target": short_esi_to_route_target(short_esi),
                                    },
                                },
                            )
                            if port_channel_mode == "active":
                                interface["lacp_id"] = short_esi.replace(":", ".")

                        append_if_not_duplicate(
                            list_of_dicts=port_channel_interfaces,
                            primary_key="name",
                            new_dict=interface,
                            context="Port-Channel Interfaces defined under point_to_point_services",
                            context_keys=["name"],
                        )

            port_channel_interfaces.extend(
                subif_parent_interface for subif_parent_interface in subif_parent_interfaces if subif_parent_interface not in port_channel_interfaces
            )

        if port_channel_interfaces:
            return port_channel_interfaces

        return None
