from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime
from ..models.get_event_list_response_status import GetEventListResponseStatus
from ..models.get_event_list_calendarodata import GetEventListCalendarodata
from ..models.get_event_list_body import GetEventListBody
from ..models.get_event_list_calendar import GetEventListCalendar
from ..models.get_event_list_start import GetEventListStart
from ..models.get_event_list_location import GetEventListLocation
from ..models.get_event_list_organizer import GetEventListOrganizer
from ..models.get_event_list_attendees_array_item_ref import (
    GetEventListAttendeesArrayItemRef,
)
from ..models.get_event_list_end import GetEventListEnd
from ..models.get_event_listodata import GetEventListodata


class GetEventList(BaseModel):
    """
    Attributes:
        calendar (Optional[GetEventListCalendar]):
        last_modified_date_time (Optional[datetime.datetime]): Shows the date and time when the event was last modified.
            Example: 2025-03-12T06:18:02.0863935+00:00.
        location (Optional[GetEventListLocation]):
        subject (Optional[str]): The subject or title of the event. Example: Update: Test event.
        web_link (Optional[str]): Provides a URL link to view the event details online. Example: https://outlook.office3
            65.com/owa/?itemid=AAMkADJmOGNjOTYwLWMzOWUtNGEzMC05MTViLTVmMjU3ZmRlZTQyNABGAAAAAACheKuSte%2BnRYh5zSjSpULXBwB8H2U
            %2B2gSPS6CGFwCo8hoKAAAAAAENAAB8H2U%2B2gSPS6CGFwCo8hoKAAEvmHqNAAA%3D&exvsurl=1&path=/calendar/item.
        is_draft (Optional[bool]): Indicates if the event is saved as a draft.
        body_preview (Optional[str]): Provides a short preview of the event's body content. Example: Test update.
        created_date_time (Optional[datetime.datetime]): Records the date and time when the event was created. Example:
            2025-03-12T04:26:04.9378676+00:00.
        original_end_time_zone (Optional[str]): Specifies the time zone for the event's original end time. Example: UTC.
        type_ (Optional[str]): Specifies the type of event, such as meeting or appointment. Example: singleInstance.
        allow_new_time_proposals (Optional[bool]): Indicates if attendees can propose new times for the event. Example:
            True.
        reminder_minutes_before_start (Optional[int]): Sets the number of minutes before the event to send a reminder.
            Example: 15.0.
        attendees (Optional[list['GetEventListAttendeesArrayItemRef']]):
        id (Optional[str]): Unique identifier for the event in the calendar. Example: AAMkADJmOGNjOTYwLWMzOWUtNGEzMC05MT
            ViLTVmMjU3ZmRlZTQyNABGAAAAAACheKuSte_nRYh5zSjSpULXBwB8H2U_2gSPS6CGFwCo8hoKAAAAAAENAAB8H2U_2gSPS6CGFwCo8hoKAAEvmH
            qNAAA=.
        original_start_time_zone (Optional[str]): The time zone in which the event was originally scheduled. Example:
            UTC.
        show_as (Optional[str]): Indicates how the event should appear on the calendar. Example: busy.
        odata (Optional[GetEventListodata]):
        response_status (Optional[GetEventListResponseStatus]):
        start (Optional[GetEventListStart]):
        calendarodata (Optional[GetEventListCalendarodata]):
        change_key (Optional[str]): Unique identifier for tracking changes to the event. Example:
            fB9lPtoEj0ughhcAqPIaCgABLz9fsA==.
        is_organizer (Optional[bool]): Shows whether the user is the organizer of the event. Example: True.
        sensitivity (Optional[str]): Specifies the privacy level of the event. Example: normal.
        is_online_meeting (Optional[bool]): Indicates if the event includes an online meeting.
        body (Optional[GetEventListBody]):
        importance (Optional[str]): Indicates the priority level of the event, such as low, normal, or high. Example:
            normal.
        i_cal_u_id (Optional[str]): A unique identifier for the event used in iCalendar format to ensure consistency.
            Example: 040000008200E00074C5B7101A82E00800000000D85A7DDE0693DB01000000000000000010000000A6FE5C404DB4974F8BA1A02
            5C0D78037.
        organizer (Optional[GetEventListOrganizer]):
        online_meeting_provider (Optional[str]): Specifies the service used for online meetings. Example: unknown.
        end (Optional[GetEventListEnd]):
        categories (Optional[list[str]]):  Example: newCat.
        uid (Optional[str]): A unique identifier assigned to each event for tracking purposes. Example: 040000008200E000
            74C5B7101A82E00800000000D85A7DDE0693DB01000000000000000010000000A6FE5C404DB4974F8BA1A025C0D78037.
        is_all_day (Optional[bool]): Indicates whether the event is scheduled for the entire day.
        has_attachments (Optional[bool]): Indicates whether the event includes any attachments.
        response_requested (Optional[bool]): Specifies if a response is requested from the attendees. Example: True.
        is_cancelled (Optional[bool]): Indicates whether the event has been cancelled.
        is_reminder_on (Optional[bool]): Shows if a reminder is set for the event. Example: True.
        hide_attendees (Optional[bool]): Determines if attendees are visible in the event details.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    calendar: Optional["GetEventListCalendar"] = Field(alias="calendar", default=None)
    last_modified_date_time: Optional[datetime.datetime] = Field(
        alias="lastModifiedDateTime", default=None
    )
    location: Optional["GetEventListLocation"] = Field(alias="location", default=None)
    subject: Optional[str] = Field(alias="subject", default=None)
    web_link: Optional[str] = Field(alias="webLink", default=None)
    is_draft: Optional[bool] = Field(alias="isDraft", default=None)
    body_preview: Optional[str] = Field(alias="bodyPreview", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    original_end_time_zone: Optional[str] = Field(
        alias="originalEndTimeZone", default=None
    )
    type_: Optional[str] = Field(alias="type", default=None)
    allow_new_time_proposals: Optional[bool] = Field(
        alias="allowNewTimeProposals", default=None
    )
    reminder_minutes_before_start: Optional[int] = Field(
        alias="reminderMinutesBeforeStart", default=None
    )
    attendees: Optional[list["GetEventListAttendeesArrayItemRef"]] = Field(
        alias="attendees", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    original_start_time_zone: Optional[str] = Field(
        alias="originalStartTimeZone", default=None
    )
    show_as: Optional[str] = Field(alias="showAs", default=None)
    odata: Optional["GetEventListodata"] = Field(alias="@odata", default=None)
    response_status: Optional["GetEventListResponseStatus"] = Field(
        alias="responseStatus", default=None
    )
    start: Optional["GetEventListStart"] = Field(alias="start", default=None)
    calendarodata: Optional["GetEventListCalendarodata"] = Field(
        alias="calendar@odata", default=None
    )
    change_key: Optional[str] = Field(alias="changeKey", default=None)
    is_organizer: Optional[bool] = Field(alias="isOrganizer", default=None)
    sensitivity: Optional[str] = Field(alias="sensitivity", default=None)
    is_online_meeting: Optional[bool] = Field(alias="isOnlineMeeting", default=None)
    body: Optional["GetEventListBody"] = Field(alias="body", default=None)
    importance: Optional[str] = Field(alias="importance", default=None)
    i_cal_u_id: Optional[str] = Field(alias="iCalUId", default=None)
    organizer: Optional["GetEventListOrganizer"] = Field(
        alias="organizer", default=None
    )
    online_meeting_provider: Optional[str] = Field(
        alias="onlineMeetingProvider", default=None
    )
    end: Optional["GetEventListEnd"] = Field(alias="end", default=None)
    categories: Optional[list[str]] = Field(alias="categories", default=None)
    uid: Optional[str] = Field(alias="uid", default=None)
    is_all_day: Optional[bool] = Field(alias="isAllDay", default=None)
    has_attachments: Optional[bool] = Field(alias="hasAttachments", default=None)
    response_requested: Optional[bool] = Field(alias="responseRequested", default=None)
    is_cancelled: Optional[bool] = Field(alias="isCancelled", default=None)
    is_reminder_on: Optional[bool] = Field(alias="isReminderOn", default=None)
    hide_attendees: Optional[bool] = Field(alias="hideAttendees", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEventList"], src_dict: Dict[str, Any]):
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
