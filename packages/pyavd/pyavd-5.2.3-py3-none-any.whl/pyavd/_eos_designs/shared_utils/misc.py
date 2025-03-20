# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Protocol

from pyavd._eos_designs.schema import EosDesigns
from pyavd._errors import AristaAvdError, AristaAvdInvalidInputsError, AristaAvdMissingVariableError
from pyavd._utils import default, get
from pyavd.api.interface_descriptions import InterfaceDescriptionData
from pyavd.j2filters import range_expand

if TYPE_CHECKING:
    from pyavd._eos_designs.eos_designs_facts import EosDesignsFacts

    from . import SharedUtilsProtocol


class MiscMixin(Protocol):
    """
    Mixin Class providing a subset of SharedUtils.

    Class should only be used as Mixin to the SharedUtils class.
    Using type-hint on self to get proper type-hints on attributes across all Mixins.
    """

    @cached_property
    def all_fabric_devices(self: SharedUtilsProtocol) -> list[str]:
        avd_switch_facts: dict = get(self.hostvars, "avd_switch_facts", required=True)
        return list(avd_switch_facts.keys())

    @cached_property
    def hostname(self: SharedUtilsProtocol) -> str:
        """Hostname set based on inventory_hostname variable. TODO: Get a proper attribute on the class instead of gleaning from the regular inputs."""
        return get(self.hostvars, "inventory_hostname", required=True)

    @cached_property
    def id(self: SharedUtilsProtocol) -> int | None:
        return self.node_config.id

    @cached_property
    def filter_tags(self: SharedUtilsProtocol) -> list:
        """Return filter.tags + group if defined."""
        filter_tags = self.node_config.filter.tags
        if self.group is not None:
            filter_tags.append(self.group)
        return filter_tags

    @cached_property
    def igmp_snooping_enabled(self: SharedUtilsProtocol) -> bool:
        return default(self.node_config.igmp_snooping_enabled, self.inputs.default_igmp_snooping_enabled)

    @cached_property
    def only_local_vlan_trunk_groups(self: SharedUtilsProtocol) -> bool:
        return self.inputs.enable_trunk_groups and self.inputs.only_local_vlan_trunk_groups

    @cached_property
    def system_mac_address(self: SharedUtilsProtocol) -> str | None:
        """
        system_mac_address.

        system_mac_address is inherited from
        Fabric Topology data model system_mac_address ->
            Host variable var system_mac_address ->.
        """
        return default(self.node_config.system_mac_address, self.inputs.system_mac_address)

    @cached_property
    def uplink_switches(self: SharedUtilsProtocol) -> list[str]:
        return self.node_config.uplink_switches._as_list() or get(self.cv_topology_config, "uplink_switches") or []

    @cached_property
    def uplink_interfaces(self: SharedUtilsProtocol) -> list[str]:
        return range_expand(
            self.node_config.uplink_interfaces or get(self.cv_topology_config, "uplink_interfaces") or self.default_interfaces.uplink_interfaces,
        )

    @cached_property
    def uplink_switch_interfaces(self: SharedUtilsProtocol) -> list[str]:
        uplink_switch_interfaces = self.node_config.uplink_switch_interfaces or get(self.cv_topology_config, "uplink_switch_interfaces") or []
        if uplink_switch_interfaces:
            return range_expand(uplink_switch_interfaces)

        if not self.uplink_switches:
            return []

        if self.id is None:
            msg = f"'id' is not set on '{self.hostname}'"
            raise AristaAvdInvalidInputsError(msg)

        uplink_switch_interfaces = []
        uplink_switch_counter = {}
        for uplink_switch in self.uplink_switches:
            uplink_switch_facts: EosDesignsFacts = self.get_peer_facts(uplink_switch, required=True)

            # Count the number of instances the current switch was processed
            uplink_switch_counter[uplink_switch] = uplink_switch_counter.get(uplink_switch, 0) + 1
            index_of_parallel_uplinks = uplink_switch_counter[uplink_switch] - 1

            # Add uplink_switch_interface based on this switch's ID (-1 for 0-based) * max_parallel_uplinks + index_of_parallel_uplinks.
            # For max_parallel_uplinks: 2 this would assign downlink interfaces like this:
            # spine1 downlink-interface mapping: [ leaf-id1, leaf-id1, leaf-id2, leaf-id2, leaf-id3, leaf-id3, ... ]
            downlink_index = (self.id - 1) * self.node_config.max_parallel_uplinks + index_of_parallel_uplinks
            if len(uplink_switch_facts._default_downlink_interfaces) > downlink_index:
                uplink_switch_interfaces.append(uplink_switch_facts._default_downlink_interfaces[downlink_index])
            else:
                msg = (
                    f"'uplink_switch_interfaces' is not set on '{self.hostname}' and 'uplink_switch' '{uplink_switch}' "
                    f"does not have 'downlink_interfaces[{downlink_index}]' set under 'default_interfaces'"
                )
                raise AristaAvdError(msg)

        return uplink_switch_interfaces

    @cached_property
    def serial_number(self: SharedUtilsProtocol) -> str | None:
        """
        serial_number.

        serial_number is inherited from
        Fabric Topology data model serial_number ->
            Host variable var serial_number.
        """
        return default(self.node_config.serial_number, self.inputs.serial_number)

    @cached_property
    def max_uplink_switches(self: SharedUtilsProtocol) -> int:
        """max_uplink_switches will default to the length of uplink_switches."""
        return default(self.node_config.max_uplink_switches, len(self.uplink_switches))

    @cached_property
    def p2p_uplinks_mtu(self: SharedUtilsProtocol) -> int | None:
        if not self.platform_settings.feature_support.per_interface_mtu:
            return None
        p2p_uplinks_mtu = default(self.platform_settings.p2p_uplinks_mtu, self.inputs.p2p_uplinks_mtu)
        return default(self.node_config.uplink_mtu, p2p_uplinks_mtu)

    @cached_property
    def fabric_name(self: SharedUtilsProtocol) -> str:
        if not self.inputs.fabric_name:
            msg = "fabric_name"
            raise AristaAvdMissingVariableError(msg)

        return self.inputs.fabric_name

    @cached_property
    def uplink_interface_speed(self: SharedUtilsProtocol) -> str | None:
        return default(self.node_config.uplink_interface_speed, self.default_interfaces.uplink_interface_speed)

    @cached_property
    def uplink_switch_interface_speed(self: SharedUtilsProtocol) -> str | None:
        # Keeping since we will need it when adding speed support under default interfaces.
        return self.node_config.uplink_switch_interface_speed

    @cached_property
    def default_interface_mtu(self: SharedUtilsProtocol) -> int | None:
        return default(self.platform_settings.default_interface_mtu, self.inputs.default_interface_mtu)

    def get_switch_fact(self: SharedUtilsProtocol, key: str, required: bool = True) -> Any:
        """
        Return facts from EosDesignsFacts.

        We need to go via avd_switch_facts since PyAVD does not expose "switch.*" in get_avdfacts.
        """
        return get(self.hostvars, f"avd_switch_facts..{self.hostname}..switch..{key}", required=required, org_key=f"switch.{key}", separator="..")

    @cached_property
    def evpn_multicast(self: SharedUtilsProtocol) -> bool:
        return self.get_switch_fact("evpn_multicast", required=False) is True

    def get_ipv4_acl(
        self: SharedUtilsProtocol, name: str, interface_name: str, *, interface_ip: str | None = None, peer_ip: str | None = None
    ) -> EosDesigns.Ipv4AclsItem:
        """
        Get one IPv4 ACL from "ipv4_acls" where fields have been substituted.

        If any substitution is done, the ACL name will get "_<interface_name>" appended.
        """
        if name not in self.inputs.ipv4_acls:
            msg = f"ipv4_acls[name={name}]"
            raise AristaAvdMissingVariableError(msg)
        org_ipv4_acl = self.inputs.ipv4_acls[name]
        # deepcopy to avoid inplace updates below from modifying the original.
        ipv4_acl = org_ipv4_acl._deepcopy()
        ip_replacements = {
            "interface_ip": interface_ip,
            "peer_ip": peer_ip,
        }
        changed = False
        for index, entry in enumerate(ipv4_acl.entries):
            if entry._get("remark"):
                continue

            err_context = f"ipv4_acls[name={name}].entries[{index}]"
            if not entry.source:
                msg = f"{err_context}.source"
                raise AristaAvdMissingVariableError(msg)
            if not entry.destination:
                msg = f"{err_context}.destination"
                raise AristaAvdMissingVariableError(msg)

            entry.source = self._get_ipv4_acl_field_with_substitution(entry.source, ip_replacements, f"{err_context}.source", interface_name)
            entry.destination = self._get_ipv4_acl_field_with_substitution(entry.destination, ip_replacements, f"{err_context}.destination", interface_name)
            if entry.source != org_ipv4_acl.entries[index].source or entry.destination != org_ipv4_acl.entries[index].destination:
                changed = True

        if changed:
            ipv4_acl.name += f"_{self.sanitize_interface_name(interface_name)}"
        return ipv4_acl

    @staticmethod
    def _get_ipv4_acl_field_with_substitution(field_value: str, replacements: dict[str, str | None], field_context: str, interface_name: str) -> str:
        """
        Checks one field if the value can be substituted.

        The given "replacements" dict will be parsed as:
          key: substitution field to look for
          value: replacement value to set.

        If a replacement is done, but the value is None, an error will be raised.
        """
        if field_value not in replacements:
            return field_value

        if (replacement_value := replacements[field_value]) is None:
            msg = (
                f"Unable to perform substitution of the value '{field_value}' defined under '{field_context}', "
                f"since no substitution value was found for interface '{interface_name}'. "
                "Make sure to set the appropriate fields on the interface."
            )
            raise AristaAvdError(msg)

        return replacement_value

    def get_l3_generic_interface_bgp_neighbors(
        self: SharedUtilsProtocol,
        l3_generic_interfaces: (
            EosDesigns._DynamicKeys.DynamicNodeTypesItem.NodeTypes.NodesItem.L3Interfaces
            | EosDesigns._DynamicKeys.DynamicNodeTypesItem.NodeTypes.NodesItem.L3PortChannels
        ),
    ) -> list:
        """
        Fetches bgp neighbors for given L3 interface placeholder.

        Fetches bgp neighbors (list of dict) for all interfaces under given interface type.
        'l3_generic_interfaces' is expected to be set to either property - self.l3_interfaces or self.l3_port_channels.
        """
        neighbors = []
        is_l3_interface = False
        if isinstance(l3_generic_interfaces, EosDesigns._DynamicKeys.DynamicNodeTypesItem.NodeTypes.NodesItem.L3Interfaces):
            is_l3_interface = True
            schema_key = "l3_interfaces"
        else:
            # implies we intend to query all L3 Port-Channels
            schema_key = "l3_port_channels"

        for interface in l3_generic_interfaces:
            if not (interface.peer_ip and interface.bgp):
                continue

            if interface.bgp.peer_as is None:
                msg = f"'{schema_key}[{interface.name}].bgp.peer_as' needs to be set to enable BGP."
                raise AristaAvdInvalidInputsError(msg)

            is_intf_wan = bool(interface.wan_carrier)

            if not interface.bgp.ipv4_prefix_list_in and is_intf_wan:
                msg = f"BGP is enabled but 'bgp.ipv4_prefix_list_in' is not configured for {schema_key}[{interface.name}]"
                raise AristaAvdInvalidInputsError(msg)

            description = interface.description
            if not description:
                if is_l3_interface:
                    description = self.interface_descriptions.underlay_ethernet_interface(
                        InterfaceDescriptionData(
                            shared_utils=self,
                            interface=interface.name,
                            peer=interface.peer,
                            peer_interface=interface.peer_interface,
                            wan_carrier=interface.wan_carrier,
                            wan_circuit_id=interface.wan_circuit_id,
                        ),
                    )
                else:
                    # build description for L3 Port-Channel interface
                    description = self.interface_descriptions.underlay_port_channel_interface(
                        InterfaceDescriptionData(
                            shared_utils=self,
                            interface=interface.name,
                            peer=interface.peer,
                            peer_interface=interface.peer_port_channel,
                            wan_carrier=interface.wan_carrier,
                            wan_circuit_id=interface.wan_circuit_id,
                        ),
                    )

            neighbor = {
                "ip_address": interface.peer_ip,
                "remote_as": interface.bgp.peer_as,
                "description": description,
            }

            neighbor["ipv4_prefix_list_in"] = interface.bgp.ipv4_prefix_list_in
            neighbor["ipv4_prefix_list_out"] = interface.bgp.ipv4_prefix_list_out
            if is_intf_wan:
                neighbor["set_no_advertise"] = True

            # The inbound route-map is only used if there is a prefix list or no-advertise
            if neighbor["ipv4_prefix_list_in"] or neighbor.get("set_no_advertise") is True:
                neighbor["route_map_in"] = f"RM-BGP-{neighbor['ip_address']}-IN"
            neighbor["route_map_out"] = f"RM-BGP-{neighbor['ip_address']}-OUT"

            neighbors.append(neighbor)

        return neighbors

    @cached_property
    def l3_bgp_neighbors(self: SharedUtilsProtocol) -> list:
        """Returns the consolidated list of L3 bgp neighbors referenced by L3 Interfaces and L3 Port-Channels."""
        l3_bgp_neighbors = self.get_l3_generic_interface_bgp_neighbors(self.l3_interfaces)
        l3_bgp_neighbors.extend(self.get_l3_generic_interface_bgp_neighbors(self.node_config.l3_port_channels))
        return l3_bgp_neighbors
