from mcp.server.fastmcp import FastMCP
from typing import List
from datetime import datetime
import threading

# Thread-safe lock for employee_leaves access
leaves_lock = threading.Lock()

employee_leaves = {
    "E001": {'balance': 18, 'history': ["2025-12-25", "2026-01-01"]},
    "E002": {'balance': 20, 'history': []}
}

mcp = FastMCP("LeaveManager")


@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee."""
    with leaves_lock:
        data = employee_leaves.get(employee_id)
        if data:
            return f"Employee {employee_id} has {data['balance']} leave days remaining."
        return f"Employee {employee_id} not found."


@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates for example ['2025-12-25', '2025-12-26']."""
    
    # Validate date format first (before acquiring lock)
    for date_str in leave_dates:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return f"Invalid date: {date_str}. Please use YYYY-MM-DD format."
    
    # Check for duplicates within the request itself
    seen = set()
    internal_duplicates = []
    for date_str in leave_dates:
        if date_str in seen:
            internal_duplicates.append(date_str)
        seen.add(date_str)
    if internal_duplicates:
        return f"Error: Duplicate dates in request: {', '.join(internal_duplicates)}"
    
    with leaves_lock:
        if employee_id not in employee_leaves:
            return f"Employee {employee_id} not found."

        # Check for duplicate dates against existing history
        existing_history = employee_leaves[employee_id]['history']
        duplicates = [d for d in leave_dates if d in existing_history]
        if duplicates:
            return f"Error: Leave already applied for dates: {', '.join(duplicates)}"

        requested_days = len(leave_dates)
        available_balance = employee_leaves[employee_id]['balance']

        if available_balance < requested_days:
            return f"Insufficient leave balance. You have {available_balance} days left."

        employee_leaves[employee_id]['balance'] -= requested_days
        employee_leaves[employee_id]['history'].extend(leave_dates)

        return f"Leave applied for {requested_days} days. New balance is {employee_leaves[employee_id]['balance']} days."


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get the leave history of the employee."""
    with leaves_lock:
        data = employee_leaves.get(employee_id)
        if data:
            history = data['history']
            if history:
                return f"Employee {employee_id} has taken leave on: {', '.join(history)}"
            else:
                return f"Employee {employee_id} has no leave history."
        return f"Employee {employee_id} not found."


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to the Leave Management System."


if __name__ == "__main__":
    mcp.run()
