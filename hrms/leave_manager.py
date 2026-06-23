from collections import defaultdict
from datetime import date
from typing import Dict

from hrms.schemas import LeaveApplyRequest


class LeaveManager:
    def __init__(self):
        self.employee_leaves: Dict[str, Dict] = defaultdict(
            lambda: {"balance": 20, "history": []}
        )

    def get_leave_balance(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            return f"{employee_id} has {data['balance']} leave days remaining."
        return "Employee ID not found."

    def apply_leave(self, req: LeaveApplyRequest) -> str:
        employee_id = req.emp_id
        leave_dates = [d.isoformat() for d in req.leave_dates]
        if employee_id not in self.employee_leaves:
            return "Employee ID not found."
        requested = len(leave_dates)
        available = self.employee_leaves[employee_id]["balance"]
        if available < requested:
            return f"Insufficient leave balance: requested {requested}, available {available}."
        self.employee_leaves[employee_id]["balance"] -= requested
        history = self.employee_leaves[employee_id]["history"]
        next_history_id = len(history) + 1
        request_id = max(
            (record.get("request_id", 0) for record in history if isinstance(record, dict)),
            default=0,
        ) + 1
        history.extend(
            {
                "history_id": next_history_id + index,
                "emp_id": employee_id,
                "leave_date": leave_date,
                "request_id": request_id,
            }
            for index, leave_date in enumerate(req.leave_dates)
        )
        return (f"Leave applied for {requested} day(s). Remaining balance: "
                f"{self.employee_leaves[employee_id]['balance']}")

    def get_leave_history(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            hist = data['history']
            dates = []
            for record in hist:
                leave_date = record.get("leave_date") if isinstance(record, dict) else record
                if isinstance(leave_date, date):
                    dates.append(leave_date.strftime("%B %d, %Y"))
                else:
                    dates.append(str(leave_date))
            return f"Leave history for {employee_id}: {', '.join(dates)}."
        return "Employee ID not found."

if __name__ == "__main__":
    lm = LeaveManager()
    print(lm.get_leave_history("E004"))
