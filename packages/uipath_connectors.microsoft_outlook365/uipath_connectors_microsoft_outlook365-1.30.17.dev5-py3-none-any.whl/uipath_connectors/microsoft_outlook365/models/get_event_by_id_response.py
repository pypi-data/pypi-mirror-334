from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_event_by_id_response_event_type import GetEventByIDResponseEventType
from ..models.get_event_by_id_response_importance import GetEventByIDResponseImportance
from ..models.get_event_by_id_response_sensitivity import (
    GetEventByIDResponseSensitivity,
)
from ..models.get_event_by_id_response_show_as import GetEventByIDResponseShowAs
import datetime
from ..models.get_event_by_id_response_attendees_array_item_ref import (
    GetEventByIDResponseAttendeesArrayItemRef,
)
from ..models.get_event_by_id_response_locations_array_item_ref import (
    GetEventByIDResponseLocationsArrayItemRef,
)
from ..models.get_event_by_id_response_online_meeting import (
    GetEventByIDResponseOnlineMeeting,
)
from ..models.get_event_by_id_response_start import GetEventByIDResponseStart
from ..models.get_event_by_id_response_recurrence import GetEventByIDResponseRecurrence
from ..models.get_event_by_id_response_location import GetEventByIDResponseLocation
from ..models.get_event_by_id_response_body import GetEventByIDResponseBody
from ..models.get_event_by_id_response_organizer import GetEventByIDResponseOrganizer
from ..models.get_event_by_id_response_response_status import (
    GetEventByIDResponseResponseStatus,
)
from ..models.get_event_by_id_response_end import GetEventByIDResponseEnd


class GetEventByIDResponse(BaseModel):
    """
    Attributes:
        last_modified_date_time (Optional[datetime.datetime]): The date and time when the calendar entry was last
            updated.
        recurrence (Optional[GetEventByIDResponseRecurrence]):
        location (Optional[GetEventByIDResponseLocation]):
        locations (Optional[list['GetEventByIDResponseLocationsArrayItemRef']]):
        subject (Optional[str]): Title → e.g. Event title
        web_link (Optional[str]): A URL link to access the calendar event online.
        is_draft (Optional[bool]): Indicates if the calendar event is saved as a draft.
        body_preview (Optional[str]): A short preview of the event's description or content.
        created_date_time (Optional[datetime.datetime]): The date and time when the calendar event was created.
        type_ (Optional[GetEventByIDResponseEventType]): Specifies the type of calendar event or action.
        original_end_time_zone (Optional[str]): The time zone in which the event originally ends.
        allow_new_time_proposals (Optional[bool]): Indicates if attendees can propose new times for the event. Example:
            True.
        reminder_minutes_before_start (Optional[int]): The number of minutes before the event to send a reminder.
        attendees (Optional[list['GetEventByIDResponseAttendeesArrayItemRef']]):
        id (Optional[str]): A unique identifier for the calendar event.
        original_start_time_zone (Optional[str]): The time zone in which the event was originally scheduled.
        show_as (Optional[GetEventByIDResponseShowAs]): Indicates how the event appears on the calendar, like busy or
            free.
        response_status (Optional[GetEventByIDResponseResponseStatus]):
        transaction_id (Optional[str]): A unique identifier for tracking the calendar action transaction. Example:
            7E163156-7762-4BEB-A1C6-729EA81755A7.
        start (Optional[GetEventByIDResponseStart]):
        change_key (Optional[str]): A unique identifier for tracking changes to the event.
        is_organizer (Optional[bool]): Indicates whether the user is the organizer of the event.
        sensitivity (Optional[GetEventByIDResponseSensitivity]): Indicates the privacy level of the calendar event.
        online_meeting (Optional[GetEventByIDResponseOnlineMeeting]):
        is_online_meeting (Optional[bool]): Indicates if the meeting is set as an online meeting. Should only be marked
            as true for Teams meeting. Example: True.
        body (Optional[GetEventByIDResponseBody]):
        importance (Optional[GetEventByIDResponseImportance]): Defines the priority level of the calendar event.
        i_cal_u_id (Optional[str]): A unique identifier for the calendar event in iCalendar format.
        organizer (Optional[GetEventByIDResponseOrganizer]):
        online_meeting_provider (Optional[str]): The service used for hosting the online meeting.
        end (Optional[GetEventByIDResponseEnd]):
        is_all_day (Optional[bool]): Indicates if the event lasts the entire day.
        has_attachments (Optional[bool]): Indicates whether the calendar event includes attachments.
        response_requested (Optional[bool]): Indicates if a response is requested from attendees.
        is_cancelled (Optional[bool]): Shows whether the event has been cancelled.
        is_reminder_on (Optional[bool]): Indicates if a reminder is set for the event.
        hide_attendees (Optional[bool]): Indicates if attendees are hidden from the calendar event. Example: True.
        online_meeting_url (Optional[str]): The web link to join the online meeting associated with the event.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    last_modified_date_time: Optional[datetime.datetime] = Field(
        alias="lastModifiedDateTime", default=None
    )
    recurrence: Optional["GetEventByIDResponseRecurrence"] = Field(
        alias="recurrence", default=None
    )
    location: Optional["GetEventByIDResponseLocation"] = Field(
        alias="location", default=None
    )
    locations: Optional[list["GetEventByIDResponseLocationsArrayItemRef"]] = Field(
        alias="locations", default=None
    )
    subject: Optional[str] = Field(alias="subject", default=None)
    web_link: Optional[str] = Field(alias="webLink", default=None)
    is_draft: Optional[bool] = Field(alias="isDraft", default=None)
    body_preview: Optional[str] = Field(alias="bodyPreview", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    type_: Optional[GetEventByIDResponseEventType] = Field(alias="type", default=None)
    original_end_time_zone: Optional[str] = Field(
        alias="originalEndTimeZone", default=None
    )
    allow_new_time_proposals: Optional[bool] = Field(
        alias="allowNewTimeProposals", default=None
    )
    reminder_minutes_before_start: Optional[int] = Field(
        alias="reminderMinutesBeforeStart", default=None
    )
    attendees: Optional[list["GetEventByIDResponseAttendeesArrayItemRef"]] = Field(
        alias="attendees", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    original_start_time_zone: Optional[str] = Field(
        alias="originalStartTimeZone", default=None
    )
    show_as: Optional[GetEventByIDResponseShowAs] = Field(alias="showAs", default=None)
    response_status: Optional["GetEventByIDResponseResponseStatus"] = Field(
        alias="responseStatus", default=None
    )
    transaction_id: Optional[str] = Field(alias="transactionId", default=None)
    start: Optional["GetEventByIDResponseStart"] = Field(alias="start", default=None)
    change_key: Optional[str] = Field(alias="changeKey", default=None)
    is_organizer: Optional[bool] = Field(alias="isOrganizer", default=None)
    sensitivity: Optional[GetEventByIDResponseSensitivity] = Field(
        alias="sensitivity", default=None
    )
    online_meeting: Optional["GetEventByIDResponseOnlineMeeting"] = Field(
        alias="onlineMeeting", default=None
    )
    is_online_meeting: Optional[bool] = Field(alias="isOnlineMeeting", default=None)
    body: Optional["GetEventByIDResponseBody"] = Field(alias="body", default=None)
    importance: Optional[GetEventByIDResponseImportance] = Field(
        alias="importance", default=None
    )
    i_cal_u_id: Optional[str] = Field(alias="iCalUId", default=None)
    organizer: Optional["GetEventByIDResponseOrganizer"] = Field(
        alias="organizer", default=None
    )
    online_meeting_provider: Optional[str] = Field(
        alias="onlineMeetingProvider", default=None
    )
    end: Optional["GetEventByIDResponseEnd"] = Field(alias="end", default=None)
    is_all_day: Optional[bool] = Field(alias="isAllDay", default=None)
    has_attachments: Optional[bool] = Field(alias="hasAttachments", default=None)
    response_requested: Optional[bool] = Field(alias="responseRequested", default=None)
    is_cancelled: Optional[bool] = Field(alias="isCancelled", default=None)
    is_reminder_on: Optional[bool] = Field(alias="isReminderOn", default=None)
    hide_attendees: Optional[bool] = Field(alias="hideAttendees", default=None)
    online_meeting_url: Optional[str] = Field(alias="onlineMeetingUrl", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEventByIDResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
