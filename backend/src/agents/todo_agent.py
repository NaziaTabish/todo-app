"""
AI Task Agent using OpenAI Agents SDK
This module implements an AI agent that can manage tasks through natural language
"""

from openai import AsyncOpenAI
from ..api.mcp_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskFilterRequest
)
import os
import json

# Tool schemas for direct OpenAI-compatible tool calling
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "add_task_tool",
            "description": "Create a new task. Use this when the user wants to add, create, or make a new task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title (REQUIRED)"},
                    "description": {"type": "string", "description": "Optional details"},
                    "priority": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"], "description": "Task priority"},
                    "due_date": {"type": "string", "description": "ISO 8601 date string"},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "recurrence": {"type": "string", "description": "Recurrence rule (daily, weekly, monthly)"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks_tool",
            "description": "List all tasks. Use this when the user wants to see, show, view, or list their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status. Default: all"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task_tool",
            "description": "Mark a task as completed or pending. task_id is a UUID string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The UUID of the task"},
                    "completed": {"type": "boolean", "description": "true to complete, false to reopen. Default: true"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task_tool",
            "description": "Delete a task by its UUID string ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The UUID of the task to delete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_tool",
            "description": "Update an existing task's title, description, priority, or other fields.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The UUID of the task to update"},
                    "title": {"type": "string", "description": "New title"},
                    "description": {"type": "string", "description": "New description"},
                    "completed": {"type": "boolean", "description": "Completion status"},
                    "priority": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"], "description": "New priority"},
                    "due_date": {"type": "string", "description": "New due date (ISO 8601)"},
                    "tags": {"type": "string", "description": "Comma-separated tags"}
                },
                "required": ["task_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a highly capable Task Management AI called FlowTask AI.

CAPABILITIES:
- You can set PRIORITY (High, Medium, Low).
- You can set DUE DATES (ask for specific dates/times). If user says "tomorrow", calculate the date.
- You can add TAGS (e.g., work, personal).
- You can set RECURRENCE (daily, weekly).

CRITICAL RULE FOR TOOL USE:
- Calling tools is your PRIMARY way of helping.
- If the user implies an action ("I need to workout", "Call mom"), create a task immediately.
- If the user mentions urgency ("urgent", "support", "critical"), set Priority to HIGH.
- If the user mentions a time ("tomorrow", "at 5pm"), set the Due Date.

CORE PRINCIPLES:
1. **Autonomy**: Use `list_tasks_tool` to find task IDs if needed before completing/deleting/updating.
2. **Inference**: User: "Buy milk urgent" -> Title: "Buy milk", Priority: HIGH.
3. **Tags**: User: "coding task" -> Tags: "coding".

Always confirm what you did: "I've added 'Buy milk' with High priority."
"""


class TaskManagementAgent:
    def __init__(self):
        # Initialize Groq client
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            # Check for OPENAI_API_KEY as fallback
            self.groq_api_key = os.getenv("OPENAI_API_KEY")
            if not self.groq_api_key:
                # For development, use a dummy key if neither is set
                print("WARNING: GROQ_API_KEY or OPENAI_API_KEY environment variable is required for production use.")
                self.groq_api_key = "dummy-key-for-development"

        # Use base URL for Groq if it's a Groq key, otherwise use OpenAI default
        # Strip potential quotes/spaces from the key
        if self.groq_api_key:
            self.groq_api_key = self.groq_api_key.strip().strip('"').strip("'")

        base_url = "https://api.groq.com/openai/v1" if os.getenv("GROQ_API_KEY") else None

        # Use AsyncOpenAI for better async integration
        self.client = AsyncOpenAI(
            api_key=self.groq_api_key,
            base_url=base_url
        )

    def _execute_tool(self, tool_name: str, args: dict, user_id) -> dict:
        """Execute a tool by name with the given arguments."""
        if tool_name == "add_task_tool":
            title = args.get("title", "")
            if not title or len(title.strip()) < 1:
                return {"error": "A non-empty title is required."}

            priority = args.get("priority")
            parsed_priority = None
            if priority:
                priority = priority.upper()
                if priority in ['HIGH', 'MEDIUM', 'LOW']:
                    parsed_priority = priority

            tags = args.get("tags")
            tag_list = [t.strip() for t in tags.split(',')] if tags else []

            recurrence = args.get("recurrence")
            rrule = recurrence
            if recurrence:
                recurrence = recurrence.lower()
                if recurrence == 'daily': rrule = 'FREQ=DAILY'
                elif recurrence == 'weekly': rrule = 'FREQ=WEEKLY'
                elif recurrence == 'monthly': rrule = 'FREQ=MONTHLY'

            req = TaskCreateRequest(
                title=title,
                description=args.get("description"),
                user_id=user_id,
                priority=parsed_priority,
                due_date=args.get("due_date"),
                tags=tag_list,
                recurrence_rule=rrule
            )
            res = add_task(req).model_dump()
            return {"status": "success", "task": res}

        elif tool_name == "list_tasks_tool":
            status = args.get("status", "all")
            req = TaskFilterRequest(user_id=user_id, status=status)
            res = list_tasks(req).model_dump()
            return res

        elif tool_name == "complete_task_tool":
            task_id = args.get("task_id")
            completed = args.get("completed", True)
            res = complete_task(user_id, task_id, completed).model_dump()
            return {"status": "success", "task": res}

        elif tool_name == "delete_task_tool":
            task_id = args.get("task_id")
            res = delete_task(user_id, task_id)
            return res

        elif tool_name == "update_task_tool":
            task_id = args.get("task_id")
            tags = args.get("tags")
            tag_list = [t.strip() for t in tags.split(',')] if tags else None

            priority = args.get("priority")
            parsed_priority = None
            if priority:
                priority = priority.upper()
                if priority in ['HIGH', 'MEDIUM', 'LOW']:
                    parsed_priority = priority

            req = TaskUpdateRequest(
                title=args.get("title"),
                description=args.get("description"),
                completed=args.get("completed"),
                priority=parsed_priority,
                due_date=args.get("due_date"),
                tags=tag_list
            )
            res = update_task(user_id, task_id, req).model_dump()
            return {"status": "success", "task": res}

        return {"error": f"Unknown tool: {tool_name}"}

    async def chat(self, messages: list, user_id) -> dict:
        """
        Process a conversation with multiple messages using OpenAI-compatible tool calling
        """
        # Normalize messages to dicts
        normalized_messages = []
        for msg in messages:
            m_dict = {}
            if isinstance(msg, dict):
                m_dict = msg
            elif hasattr(msg, "model_dump"):
                m_dict = msg.model_dump()
            elif hasattr(msg, "dict"):
                m_dict = msg.dict()

            if m_dict:
                role = m_dict.get("role", "user")
                if role == "ai": role = "assistant"
                normalized_messages.append({
                    "role": role,
                    "content": m_dict.get("content", m_dict.get("text", ""))
                })

        # Keep last 10 messages
        messages = normalized_messages[-10:]

        try:
            if self.groq_api_key == "dummy-key-for-development":
                return {"response": "(Dummy Mode) I see your messages.", "action_performed": None, "task_result": None}

            # Try OpenAI Agents SDK first
            try:
                return await self._chat_with_agents_sdk(messages, user_id)
            except Exception as agents_err:
                print(f"Agents SDK failed ({agents_err}), falling back to direct tool calling")
                return await self._chat_with_direct_tools(messages, user_id)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "response": f"Error: {str(e)}",
                "action_performed": None,
                "task_result": None
            }

    async def _chat_with_agents_sdk(self, messages: list, user_id) -> dict:
        """Try using the OpenAI Agents SDK."""
        from agents import Agent, Runner, set_default_openai_client, function_tool, set_tracing_disabled

        set_tracing_disabled(True)
        set_default_openai_client(self.client)

        @function_tool
        def add_task_tool(title: str, description: str = None, priority: str = None, due_date: str = None, tags: str = None, recurrence: str = None) -> dict:
            """Create a new task. title is required."""
            return self._execute_tool("add_task_tool", {
                "title": title, "description": description, "priority": priority,
                "due_date": due_date, "tags": tags, "recurrence": recurrence
            }, user_id)

        @function_tool
        def list_tasks_tool(status: str = "all") -> dict:
            """List all tasks. status can be 'all', 'pending', or 'completed'."""
            return self._execute_tool("list_tasks_tool", {"status": status}, user_id)

        @function_tool
        def complete_task_tool(task_id: str, completed: bool = True) -> dict:
            """Mark a task as completed or pending. task_id is a UUID string."""
            return self._execute_tool("complete_task_tool", {"task_id": task_id, "completed": completed}, user_id)

        @function_tool
        def delete_task_tool(task_id: str) -> dict:
            """Delete a task by its UUID string ID."""
            return self._execute_tool("delete_task_tool", {"task_id": task_id}, user_id)

        @function_tool
        def update_task_tool(task_id: str, title: str = None, description: str = None, completed: bool = None, priority: str = None, due_date: str = None, tags: str = None) -> dict:
            """Update an existing task."""
            return self._execute_tool("update_task_tool", {
                "task_id": task_id, "title": title, "description": description,
                "completed": completed, "priority": priority, "due_date": due_date, "tags": tags
            }, user_id)

        agent = Agent(
            name="FlowTask AI",
            instructions=SYSTEM_PROMPT + f"\nYou are helping User ID: {user_id}.",
            model="llama-3.3-70b-versatile",
            tools=[add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool]
        )

        result = await Runner.run(agent, input=messages)
        final_text = str(result.final_output) if hasattr(result, 'final_output') else str(result)

        return {
            "response": final_text,
            "action_performed": "agent_action",
            "task_result": None
        }

    async def _chat_with_direct_tools(self, messages: list, user_id) -> dict:
        """Fallback: use AsyncOpenAI client directly with tool calling."""
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\nYou are helping User ID: {user_id}."}] + messages

        # First call - may include tool calls
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto"
        )

        message = response.choices[0].message
        action_performed = None

        # Process tool calls in a loop (max 5 iterations to prevent infinite loops)
        for _ in range(5):
            if not message.tool_calls:
                break

            action_performed = "agent_action"

            # Build a clean assistant message (avoid unsupported fields like 'annotations')
            assistant_msg = {"role": "assistant", "content": message.content or ""}
            if message.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in message.tool_calls
                ]
            full_messages.append(assistant_msg)
            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                try:
                    fn_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    fn_args = {}

                try:
                    result = self._execute_tool(fn_name, fn_args, user_id)
                except Exception as e:
                    result = {"error": str(e)}

                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Get next response after tool results
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto"
            )
            message = response.choices[0].message

        final_text = message.content or "I processed your request."

        return {
            "response": final_text,
            "action_performed": action_performed,
            "task_result": None
        }
