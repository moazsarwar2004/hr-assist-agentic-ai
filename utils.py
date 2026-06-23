from datetime import date, timedelta
import random
from hrms import *

def seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager, seed: int = 42):
    """
    Seeds all service classes with coherent dummy data.

    Args:
        employee_manager: Instance of EmployeeManager
        leave_manager: Instance of LeaveManager
        meeting_manager: Instance of MeetingManager
        ticket_manager: Instance of TicketManager

    Returns:
        None - services are modified in-place
    """

    rng = random.Random(seed)

    employees_data = [
        {"emp_id": "E001", "name": "Moaz Sarwar", "manager_id": None, "email": "moaz.sarwar@atliq.com"},
        {"emp_id": "E002", "name": "Anas Sarwar", "manager_id": "E001", "email": "anas.sarwar@atliq.com"},
        {"emp_id": "E003", "name": "Ahmed Sarwar", "manager_id": "E001", "email": "ahmed.sarwar@atliq.com"},
        {"emp_id": "E004", "name": "Umer Sarwar", "manager_id": "E003", "email": "umer.sarwar@atliq.com"},
        {"emp_id": "E005", "name": "Muhammad Sarwar", "manager_id": "E003", "email": "muhammad.sarwar@atliq.com"},
        {"emp_id": "E006", "name": "Ali Sarwar", "manager_id": "E002", "email": "ali.sarwar@atliq.com"},
        {"emp_id": "E007", "name": "Carlos Mendez", "manager_id": "E006", "email": "carlos.mendez@atliq.com"},
        {"emp_id": "E008", "name": "Lisa Wong", "manager_id": "E006", "email": "lisa.wong@atliq.com"},
    ]

    for employee in employees_data:
        employee_manager.add_employee(EmployeeCreate(**employee))

    # Create leave data
    # Set up some leave history for each employee
    current_date = date.today()
    request_id_counter = 1

    for employee in employees_data:
        emp_id = employee["emp_id"]

        # Set a random leave balance between 5 and 20 days
        leave_manager.employee_leaves[emp_id]["balance"] = rng.randint(5, 20)

        # Create some leave history entries
        num_leaves = rng.randint(1, 5)  # Random number of leave entries

        for i in range(num_leaves):
            # Generate a leave date in the past (1-90 days ago)
            days_ago = rng.randint(1, 90)
            leave_date = current_date - timedelta(days=days_ago)

            # Add to leave history
            history_entry = {
                "history_id": len(leave_manager.employee_leaves[emp_id]["history"]) + 1,
                "emp_id": emp_id,
                "leave_date": leave_date,
                "request_id": request_id_counter
            }
            leave_manager.employee_leaves[emp_id]["history"].append(history_entry)

            # Sometimes add consecutive days for the same request
            if rng.random() > 0.7:  # 30% chance of multi-day leave
                for j in range(1, rng.randint(2, 5)):  # 1-4 additional days
                    consecutive_date = leave_date + timedelta(days=j)
                    consecutive_entry = {
                        "history_id": len(leave_manager.employee_leaves[emp_id]["history"]) + 1,
                        "emp_id": emp_id,
                        "leave_date": consecutive_date,
                        "request_id": request_id_counter
                    }
                    leave_manager.employee_leaves[emp_id]["history"].append(consecutive_entry)

            request_id_counter += 1

    # Create meeting data
    meeting_types = ["Team Sync", "Project Review", "Client Meeting", "1:1", "Planning"]

    # Generate meetings for each employee
    for employee in employees_data:
        emp_id = employee["emp_id"]
        num_meetings = rng.randint(2, 6)

        for i in range(num_meetings):
            # Create a meeting in the next 10 days
            meeting_date = current_date + timedelta(days=rng.randint(0, 10))
            meeting_hour = rng.randint(9, 16)  # 9 AM to 4 PM

            meeting = {
                "date": f"{meeting_date.isoformat()}T{meeting_hour:02d}:00:00",
                "topic": rng.choice(meeting_types),
            }

            meeting_manager.meetings[emp_id].append(meeting)

    # Create ticket data
    ticket_items = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headset", "Office Chair", "Software License"]
    ticket_reasons = ["New hire setup", "Replacement for broken item", "Upgrade request", "Project requirement",
                      "Ergonomic needs"]

    # Generate some tickets
    num_tickets = rng.randint(8, 15)
    for _ in range(num_tickets):
        employee = rng.choice(employees_data)
        ticket_id = f"T{ticket_manager._next_id:04d}"
        timestamp = current_date.isoformat()

        ticket = {
            "ticket_id": ticket_id,
            "emp_id": employee["emp_id"],
            "item": rng.choice(ticket_items),
            "reason": rng.choice(ticket_reasons),
            "status": rng.choice(["Open", "In Progress", "Closed"]),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        ticket_manager.tickets.append(ticket)
        ticket_manager._next_id += 1

    return {
        "employees": len(employee_manager.employees),
        "leave_records": sum(len(data["history"]) for data in leave_manager.employee_leaves.values()),
        "meetings": sum(len(meetings) for meetings in meeting_manager.meetings.values()),
        "tickets": len(ticket_manager.tickets)
    }

if __name__ == "__main__":
    # Initialize services
    employee_manager = EmployeeManager()
    leave_manager = LeaveManager()
    meeting_manager = MeetingManager()
    ticket_manager = TicketManager()

    # Seed the services with data
    result = seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

    print(f"Seeded {result['employees']} employees")
    print(f"Seeded {result['leave_records']} leave records")
    print(f"Seeded {result['meetings']} meetings")
    print(f"Seeded {result['tickets']} tickets")

    # employee_manager.add_employee(EmployeeCreate(name="John Doe", manager_id="E001"))
    # print(f"Manager of E004 {employee_manager.get_manager('E004')}")
    # print(f"Direct reports of E004 {employee_manager.get_direct_reports('E001')}")

    print(leave_manager.get_leave_history("E004"))
