import logging
from datetime import datetime, timedelta
from dateutil.parser import parse as date_parse
from typing import List, Dict, Any, Optional

from services.calendar_service import CalendarService

logging.basicConfig(level=logging.INFO)

def schedule_appointment(summary: str, date: str, time: str, duration_minutes: int, notes: str = "", attendees: List[str] = []) -> Dict[str, Any]:
    """
    Schedules a new appointment using the CalendarService.
    """
    try:
        combined_datetime_str = f"{date} {time}"
        start_datetime = date_parse(combined_datetime_str, fuzzy=True)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        
        start_time_iso = start_datetime.isoformat()
        end_time_iso = end_datetime.isoformat()

        calendar_service = CalendarService()
        result = calendar_service.create_event(
            summary=summary,
            start_time=start_time_iso,
            end_time=end_time_iso,
            attendees=attendees,
            description=notes
        )
        return {"status": "success", "message": f"Appointment scheduled: {summary} on {start_datetime.strftime('%Y-%m-%d %H:%M')}. {result.get('message', '')}", "event_id": result.get('event_id')}
    except Exception as e:
        logging.error(f"Error scheduling appointment: {e}", exc_info=True)
        return {"status": "error", "message": f"Failed to schedule appointment: {str(e)}"}

def reschedule_appointment(event_id: str, new_date: str, new_time: str, new_duration_minutes: int) -> Dict[str, Any]:
    """
    Reschedules an existing appointment using the CalendarService.
    """
    try:
        combined_datetime_str = f"{new_date} {new_time}"
        new_start_datetime = date_parse(combined_datetime_str, fuzzy=True)
        new_end_datetime = new_start_datetime + timedelta(minutes=new_duration_minutes)

        new_start_time_iso = new_start_datetime.isoformat()
        new_end_time_iso = new_end_datetime.isoformat()

        calendar_service = CalendarService()
        result = calendar_service.reschedule_event(
            event_id=event_id,
            new_start_time=new_start_time_iso,
            new_end_time=new_end_time_iso
        )
        return {"status": "success", "message": f"Appointment {event_id} rescheduled to {new_start_datetime.strftime('%Y-%m-%d %H:%M')}. {result.get('message', '')}"}
    except Exception as e:
        logging.error(f"Error rescheduling appointment: {e}", exc_info=True)
        return {"status": "error", "message": f"Failed to reschedule appointment: {str(e)}"}

def report_construction_issue(urgency: str, description: str, location: str, reported_by: str, action_required: str) -> Dict[str, Any]:
    """
    Reports a construction site issue.
    """
    logging.info(f"Received construction issue report: Urgency={urgency}, Description={description}, Location={location}, Reported by={reported_by}, Action required={action_required}")
    # In a real implementation, this would interact with an issue tracking system or notification service.
    return {"status": "success", "message": "Construction issue reported successfully. I will proceed with the necessary actions."}

# List of tools available to the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "schedule_appointment",
            "description": "Schedules a new appointment on the calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "A brief description of the appointment."},
                    "date": {"type": "string", "description": "The date of the appointment (e.g., 'tomorrow', 'July 25th', 'next Monday')."},
                    "time": {"type": "string", "description": "The time of the appointment (e.g., '9 AM', '14:30', 'lunchtime')."},
                    "duration_minutes": {"type": "integer", "description": "The duration of the appointment in minutes (default to 60 if not specified)."},
                    "notes": {"type": "string", "description": "Any additional notes or details about the appointment."},
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string", "format": "email"},
                        "description": "A list of attendees' email addresses."
                    }
                },
                "required": ["summary", "date", "time", "duration_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reschedule_appointment",
            "description": "Reschedules an existing appointment on the calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "The ID of the event to reschedule."},
                    "new_date": {"type": "string", "description": "The new date for the appointment."},
                    "new_time": {"type": "string", "description": "The new time for the appointment."},
                    "new_duration_minutes": {"type": "integer", "description": "The new duration of the appointment in minutes."},
                },
                "required": ["event_id", "new_date", "new_time", "new_duration_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_construction_issue",
            "description": "Reports a construction site issue with its details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "urgency": {"type": "string", "enum": ["urgent", "routine"], "description": "The urgency of the issue."},
                    "description": {"type": "string", "description": "A detailed description of the issue."},
                    "location": {"type": "string", "description": "The specific location of the issue."},
                    "reported_by": {"type": "string", "description": "The name or email of the person reporting the issue."},
                    "action_required": {"type": "string", "description": "The immediate action required for the issue."}
                },
                "required": ["urgency", "description", "location", "reported_by", "action_required"]
            }
        }
    }
]

# Map of tool names to their corresponding functions
TOOL_MAP = {
    "schedule_appointment": schedule_appointment,
    "reschedule_appointment": reschedule_appointment,
    "report_construction_issue": report_construction_issue,
}
