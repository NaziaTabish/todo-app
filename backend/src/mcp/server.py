"""MCP Server setup with tool registry.

Phase III: AI-Powered Todo Chatbot
Defines MCP tools for task operations.
"""

from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass, field


@dataclass
class MCPTool:
    """Represents an MCP tool definition."""

    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Optional[Callable] = None


class MCPToolRegistry:
    """Registry for MCP tools that can be used by the AI agent."""

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, MCPTool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Optional[Callable] = None
    ) -> None:
        """Register a new MCP tool.

        Args:
            name: Tool name (e.g., 'add_task')
            description: Human-readable description
            parameters: JSON Schema for tool parameters
            handler: Optional function to execute the tool
        """
        self._tools[name] = MCPTool(
            name=name,
            description=description,
            parameters=parameters,
            handler=handler
        )

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> List[MCPTool]:
        """Get all registered tools."""
        return list(self._tools.values())

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Get tools in OpenAI function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self._tools.values()
        ]

    async def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool by name with given arguments.

        Args:
            name: Tool name
            **kwargs: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found or has no handler
        """
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        if not tool.handler:
            raise ValueError(f"Tool '{name}' has no handler")

        # Check if handler is async
        import asyncio
        if asyncio.iscoroutinefunction(tool.handler):
            return await tool.handler(**kwargs)
        else:
            return tool.handler(**kwargs)


# Global tool registry instance
tool_registry = MCPToolRegistry()


# Tool parameter schemas (JSON Schema format)
ADD_TASK_PARAMS = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The task title"
        },
        "description": {
            "type": "string",
            "description": "Optional task description"
        }
    },
    "required": ["title"]
}

LIST_TASKS_PARAMS = {
    "type": "object",
    "properties": {
        "filter": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "description": "Filter tasks by status"
        }
    }
}

COMPLETE_TASK_PARAMS = {
    "type": "object",
    "properties": {
        "task_identifier": {
            "type": "string",
            "description": "Task title or partial match to find the task"
        }
    },
    "required": ["task_identifier"]
}

DELETE_TASK_PARAMS = {
    "type": "object",
    "properties": {
        "task_identifier": {
            "type": "string",
            "description": "Task title or partial match to find the task"
        }
    },
    "required": ["task_identifier"]
}

UPDATE_TASK_PARAMS = {
    "type": "object",
    "properties": {
        "task_identifier": {
            "type": "string",
            "description": "Current task title or partial match"
        },
        "new_title": {
            "type": "string",
            "description": "New task title"
        },
        "new_description": {
            "type": "string",
            "description": "New task description"
        }
    },
    "required": ["task_identifier"]
}


def register_all_tools():
    """Register all MCP tools. Called on module import."""
    from .tools.add_task import ADD_TASK_TOOL
    from .tools.list_tasks import LIST_TASKS_TOOL
    from .tools.complete_task import COMPLETE_TASK_TOOL
    from .tools.delete_task import DELETE_TASK_TOOL
    from .tools.update_task import UPDATE_TASK_TOOL

    tools = [
        ADD_TASK_TOOL,
        LIST_TASKS_TOOL,
        COMPLETE_TASK_TOOL,
        DELETE_TASK_TOOL,
        UPDATE_TASK_TOOL
    ]

    for tool in tools:
        tool_registry.register(
            name=tool["name"],
            description=tool["description"],
            parameters=tool["parameters"],
            handler=tool["handler"]
        )


# Auto-register tools on import
register_all_tools()
