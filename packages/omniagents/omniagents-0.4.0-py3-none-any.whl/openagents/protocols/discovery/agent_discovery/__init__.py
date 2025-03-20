"""
Agent Discovery Protocol for OmniAgents.

This protocol allows agents to announce their capabilities to the network
and for other agents to discover agents with specific capabilities.
Key features:
- Capability announcement
- Capability discovery
- Capability matching
"""

from src.omniagents.protocols.discovery.agent_discovery.adapter import AgentDiscoveryAdapter
from src.omniagents.protocols.discovery.agent_discovery.protocol import AgentDiscoveryProtocol

__all__ = ["AgentDiscoveryAdapter", "AgentDiscoveryProtocol"]
