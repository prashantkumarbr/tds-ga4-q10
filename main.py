# main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS for all origins (for browser requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(..., description="User query")):
    """
    Match the user's natural language query to a function
    and extract parameters accordingly.
    """

    # 1️⃣ Ticket Status
    match = re.match(r".*status of ticket (\d+)", q, re.IGNORECASE)
    if match:
        ticket_id = int(match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": ticket_id})
        }

    # 2️⃣ Schedule Meeting
    match = re.match(
        r".*Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)", q, re.IGNORECASE
    )
    if match:
        date, time, meeting_room = match.groups()
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": meeting_room.strip()
            })
        }

    # 3️⃣ Expense Reimbursement
    match = re.match(r".*expense balance for employee (\d+)", q, re.IGNORECASE)
    if match:
        employee_id = int(match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": employee_id})
        }

    # 4️⃣ Performance Bonus Calculation
    match = re.match(r".*bonus for employee (\d+) for (\d{4})", q, re.IGNORECASE)
    if match:
        employee_id, current_year = match.groups()
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(employee_id),
                "current_year": int(current_year)
            })
        }

    # 5️⃣ Office Issue Reporting
    match = re.match(r".*issue (\d+) for the (.+?) department", q, re.IGNORECASE)
    if match:
        issue_code, department = match.groups()
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_code),
                "department": department.strip()
            })
        }

    # ❌ No match found
    return {
        "error": "Could not determine function from query."
    }
