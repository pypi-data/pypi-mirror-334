# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Protocol

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen
from pyavd._errors import AristaAvdInvalidInputsError
from pyavd._utils import append_if_not_duplicate, get, short_esi_to_route_target, strip_null_from_data
from pyavd.api.interface_descriptions import InterfaceDescriptionData
from pyavd.j2filters import natural_sort

if TYPE_CHECKING:
    from . import AvdStructuredConfigUnderlayProtocol


class PortChannelInterfacesMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    @cached_property
    def port_channel_interfaces(self: AvdStructuredConfigUnderlayProtocol) -> list | None:
        """Return structured config for port_channel_interfaces."""
        port_channel_interfaces = []
        port_channel_list = []
        for link in self._underlay_links:
            if link["type"] != "underlay_l2" or link.get("channel_group_id") is None:
                continue

            if (channel_group_id := link.get("channel_group_id")) in port_channel_list:
                continue

            port_channel_list.append(channel_group_id)

            port_channel_name = f"Port-Channel{link['channel_group_id']}"

            port_channel_interface = {
                "name": port_channel_name,
                "description": self.shared_utils.interface_descriptions.underlay_port_channel_interface(
                    InterfaceDescriptionData(
                        shared_utils=self.shared_utils,
                        interface=port_channel_name,
                        link_type="underlay_l2",
                        peer=link["peer"],
                        peer_interface=f"Port-Channel{link['peer_channel_group_id']}",
                        peer_channel_group_id=link["peer_channel_group_id"],
                        port_channel_id=link["channel_group_id"],
                        peer_node_group=link.get("peer_node_group"),
                    ),
                ),
                "switchport": {
                    "enabled": True,
                    "mode": "trunk",
                    "trunk": {
                        "native_vlan": link.get("native_vlan"),
                    },
                },
                "shutdown": False,
                "service_profile": self.inputs.p2p_uplinks_qos_profile,
                "link_tracking_groups": link.get("link_tracking_groups"),
                "sflow": link.get("sflow"),
                "flow_tracker": link.get("flow_tracker"),
                "spanning_tree_portfast": link.get("spanning_tree_portfast"),
            }

            if (trunk_groups := link.get("trunk_groups")) is not None:
                port_channel_interface["switchport"]["trunk"]["groups"] = trunk_groups
            elif (vlans := link.get("vlans")) is not None:
                port_channel_interface["switchport"]["trunk"]["allowed_vlan"] = vlans

            # Configure MLAG on MLAG switches if either 'mlag_on_orphan_port_channel_downlink' or 'link.mlag' is True
            if self.shared_utils.mlag is True and any([self.inputs.mlag_on_orphan_port_channel_downlink, link.get("mlag", True)]):
                port_channel_interface["mlag"] = int(link.get("channel_group_id"))

            if (short_esi := link.get("short_esi")) is not None:
                port_channel_interface["evpn_ethernet_segment"] = {
                    "identifier": f"{self.inputs.evpn_short_esi_prefix}{short_esi}",
                    "route_target": short_esi_to_route_target(short_esi),
                }
                port_channel_interface["lacp_id"] = short_esi.replace(":", ".")

            # PTP
            if get(link, "ptp.enable") is True:
                ptp_config = {}

                # Apply PTP profile config if using the new ptp config style
                if self.shared_utils.ptp_enabled:
                    ptp_config.update(self.shared_utils.ptp_profile._as_dict(include_default_values=True))

                ptp_config["enable"] = True
                ptp_config.pop("profile", None)

                port_channel_interface["ptp"] = ptp_config

            # Inband ZTP Port-Channel LACP Fallback
            if get(link, "inband_ztp_vlan"):
                port_channel_interface["lacp_fallback_mode"] = "individual"
                port_channel_interface["lacp_fallback_timeout"] = get(link, "inband_ztp_lacp_fallback_delay")

            # Structured Config
            if structured_config := link.get("structured_config"):
                self.custom_structured_configs.nested.port_channel_interfaces.obtain(port_channel_name)._deepmerge(
                    EosCliConfigGen.PortChannelInterfacesItem._from_dict(structured_config), list_merge=self.custom_structured_configs.list_merge_strategy
                )

            # Remove None values
            port_channel_interface = strip_null_from_data(port_channel_interface, strip_values_tuple=(None, "", {}))

            port_channel_interfaces.append(port_channel_interface)

        # Support l3_port_channels including sub-interfaces
        subif_parent_port_channel_names = set()
        regular_l3_port_channel_names = set()
        for l3_port_channel in self.shared_utils.node_config.l3_port_channels:
            interface_name = l3_port_channel.name
            is_subinterface = "." in interface_name
            if not is_subinterface:
                # This is a regular Port-Channel (not sub-interface)
                regular_l3_port_channel_names.add(interface_name)
                continue
            # This is a subinterface for a port-channel interface.
            # We need to ensure that parent port-channel interface is also included explicitly
            # within list of Port-Channel interfaces.
            parent_port_channel_name = interface_name.split(".", maxsplit=1)[0]
            subif_parent_port_channel_names.add(parent_port_channel_name)
            if l3_port_channel.member_interfaces:
                msg = f"L3 Port-Channel sub-interface '{interface_name}' has 'member_interfaces' set. This is not a valid setting."
                raise AristaAvdInvalidInputsError(msg)
            if l3_port_channel._get("mode"):
                # implies 'mode' is set when not applicable for a sub-interface
                msg = f"L3 Port-Channel sub-interface '{interface_name}' has 'mode' set. This is not a valid setting."
                raise AristaAvdInvalidInputsError(msg)

        # Sanity check if there are any sub-interfaces for which parent Port-channel is not explicitly specified
        if missing_parent_port_channels := subif_parent_port_channel_names.difference(regular_l3_port_channel_names):
            msg = (
                f"One or more L3 Port-Channels '{', '.join(natural_sort(missing_parent_port_channels))}' "
                "need to be specified as they have sub-interfaces referencing them."
            )
            raise AristaAvdInvalidInputsError(msg)

        # Now that validation is complete, we can make another pass at all l3_port_channels
        # (subinterfaces or otherwise) and generate their structured config.
        for l3_port_channel in self.shared_utils.node_config.l3_port_channels:
            port_channel_interface = self._get_l3_port_channel_cfg(l3_port_channel)
            append_if_not_duplicate(
                list_of_dicts=port_channel_interfaces,
                primary_key="name",
                new_dict=port_channel_interface,
                context=f"L3 Port-Channel interfaces defined under {self.shared_utils.node_type_key_data.key} l3_port_channels",
                context_keys=["name", "peer", "peer_port_channel"],
            )

        # WAN HA interface for direct connection
        if (port_channel_interface := self._get_direct_ha_port_channel_interface()) is not None:
            append_if_not_duplicate(
                list_of_dicts=port_channel_interfaces,
                primary_key="name",
                new_dict=port_channel_interface,
                context="Port-Channel interface for WAN direct HA.",
                context_keys=["name", "peer", "peer_interface"],
            )

        if port_channel_interfaces:
            return port_channel_interfaces

        return None

    def _get_direct_ha_port_channel_interface(self: AvdStructuredConfigUnderlayProtocol) -> dict | None:
        """Return a dict containing the port-channel interface for direct HA."""
        if not self.shared_utils.use_port_channel_for_direct_ha:
            return None

        direct_wan_ha_links_flow_tracker = self.shared_utils.get_flow_tracker(self.shared_utils.node_config.wan_ha.flow_tracking)
        port_channel_name = f"Port-Channel{self.shared_utils.wan_ha_port_channel_id}"
        description = self.shared_utils.interface_descriptions.wan_ha_port_channel_interface(
            InterfaceDescriptionData(
                shared_utils=self.shared_utils,
                interface=port_channel_name,
                peer=self.shared_utils.wan_ha_peer,
                peer_interface=port_channel_name,
            ),
        )

        return {
            "name": port_channel_name,
            "switchport": {"enabled": False},
            "peer_type": "l3_interface",
            # TODO: if different interfaces used across nodes it will fail just like for mlag.
            "peer_interface": port_channel_name,
            "peer": self.shared_utils.wan_ha_peer,
            "shutdown": False,
            "description": description,
            "ip_address": self.shared_utils.wan_ha_ip_addresses[0],
            "flow_tracker": direct_wan_ha_links_flow_tracker,
            "mtu": self.shared_utils.node_config.wan_ha.mtu,
        }
