"""Contains all the data models used in inputs/outputs"""

from .archive_email_response import ArchiveEmailResponse
from .archive_email_response_body import ArchiveEmailResponseBody
from .archive_email_response_flag import ArchiveEmailResponseFlag
from .archive_email_response_from import ArchiveEmailResponseFrom
from .archive_email_response_from_email_address import (
    ArchiveEmailResponseFromEmailAddress,
)
from .archive_email_response_sender import ArchiveEmailResponseSender
from .archive_email_response_sender_email_address import (
    ArchiveEmailResponseSenderEmailAddress,
)
from .archive_email_response_to_recipients_array_item_ref import (
    ArchiveEmailResponseToRecipientsArrayItemRef,
)
from .archive_email_response_to_recipients_email_address import (
    ArchiveEmailResponseToRecipientsEmailAddress,
)
from .create_event_request import CreateEventRequest
from .create_event_request_body import CreateEventRequestBody
from .create_event_request_end import CreateEventRequestEnd
from .create_event_request_importance import CreateEventRequestImportance
from .create_event_request_location import CreateEventRequestLocation
from .create_event_request_sensitivity import CreateEventRequestSensitivity
from .create_event_request_show_as import CreateEventRequestShowAs
from .create_event_request_start import CreateEventRequestStart
from .create_event_response import CreateEventResponse
from .create_event_response_attendees_array_item_ref import (
    CreateEventResponseAttendeesArrayItemRef,
)
from .create_event_response_attendees_email_address import (
    CreateEventResponseAttendeesEmailAddress,
)
from .create_event_response_attendees_status import CreateEventResponseAttendeesStatus
from .create_event_response_event_type import CreateEventResponseEventType
from .create_event_response_location import CreateEventResponseLocation
from .create_event_response_locations_array_item_ref import (
    CreateEventResponseLocationsArrayItemRef,
)
from .create_event_response_online_meeting import CreateEventResponseOnlineMeeting
from .create_event_response_organizer import CreateEventResponseOrganizer
from .create_event_response_organizer_email_address import (
    CreateEventResponseOrganizerEmailAddress,
)
from .create_event_response_response_status import CreateEventResponseResponseStatus
from .default_error import DefaultError
from .forward_email_request import ForwardEmailRequest
from .forward_email_request_message import ForwardEmailRequestMessage
from .forward_event_request import ForwardEventRequest
from .get_calendars import GetCalendars
from .get_calendars_owner import GetCalendarsOwner
from .get_email_folders import GetEmailFolders
from .get_event_by_id_response import GetEventByIDResponse
from .get_event_by_id_response_attendees_array_item_ref import (
    GetEventByIDResponseAttendeesArrayItemRef,
)
from .get_event_by_id_response_attendees_email_address import (
    GetEventByIDResponseAttendeesEmailAddress,
)
from .get_event_by_id_response_attendees_status import (
    GetEventByIDResponseAttendeesStatus,
)
from .get_event_by_id_response_body import GetEventByIDResponseBody
from .get_event_by_id_response_end import GetEventByIDResponseEnd
from .get_event_by_id_response_event_type import GetEventByIDResponseEventType
from .get_event_by_id_response_importance import GetEventByIDResponseImportance
from .get_event_by_id_response_location import GetEventByIDResponseLocation
from .get_event_by_id_response_locations_array_item_ref import (
    GetEventByIDResponseLocationsArrayItemRef,
)
from .get_event_by_id_response_online_meeting import GetEventByIDResponseOnlineMeeting
from .get_event_by_id_response_organizer import GetEventByIDResponseOrganizer
from .get_event_by_id_response_organizer_email_address import (
    GetEventByIDResponseOrganizerEmailAddress,
)
from .get_event_by_id_response_recurrence import GetEventByIDResponseRecurrence
from .get_event_by_id_response_recurrence_pattern import (
    GetEventByIDResponseRecurrencePattern,
)
from .get_event_by_id_response_recurrence_range import (
    GetEventByIDResponseRecurrenceRange,
)
from .get_event_by_id_response_response_status import GetEventByIDResponseResponseStatus
from .get_event_by_id_response_sensitivity import GetEventByIDResponseSensitivity
from .get_event_by_id_response_show_as import GetEventByIDResponseShowAs
from .get_event_by_id_response_start import GetEventByIDResponseStart
from .get_event_list import GetEventList
from .get_event_list_attendees_array_item_ref import GetEventListAttendeesArrayItemRef
from .get_event_list_attendees_email_address import GetEventListAttendeesEmailAddress
from .get_event_list_attendees_status import GetEventListAttendeesStatus
from .get_event_list_body import GetEventListBody
from .get_event_list_calendar import GetEventListCalendar
from .get_event_list_calendar_owner import GetEventListCalendarOwner
from .get_event_list_calendarodata import GetEventListCalendarodata
from .get_event_list_end import GetEventListEnd
from .get_event_list_location import GetEventListLocation
from .get_event_list_organizer import GetEventListOrganizer
from .get_event_list_organizer_email_address import GetEventListOrganizerEmailAddress
from .get_event_list_response_status import GetEventListResponseStatus
from .get_event_list_start import GetEventListStart
from .get_event_listodata import GetEventListodata
from .get_newest_email_response import GetNewestEmailResponse
from .get_newest_email_response_body import GetNewestEmailResponseBody
from .get_newest_email_response_flag import GetNewestEmailResponseFlag
from .get_newest_email_response_from import GetNewestEmailResponseFrom
from .get_newest_email_response_from_email_address import (
    GetNewestEmailResponseFromEmailAddress,
)
from .get_newest_email_response_sender import GetNewestEmailResponseSender
from .get_newest_email_response_sender_email_address import (
    GetNewestEmailResponseSenderEmailAddress,
)
from .get_newest_email_response_to_recipients_array_item_ref import (
    GetNewestEmailResponseToRecipientsArrayItemRef,
)
from .get_newest_email_response_to_recipients_email_address import (
    GetNewestEmailResponseToRecipientsEmailAddress,
)
from .list_email import ListEmail
from .list_email_bcc_recipients_array_item_ref import ListEmailBccRecipientsArrayItemRef
from .list_email_bcc_recipients_email_address import ListEmailBccRecipientsEmailAddress
from .list_email_body import ListEmailBody
from .list_email_cc_recipients_array_item_ref import ListEmailCcRecipientsArrayItemRef
from .list_email_cc_recipients_email_address import ListEmailCcRecipientsEmailAddress
from .list_email_end_date_time import ListEmailEndDateTime
from .list_email_flag import ListEmailFlag
from .list_email_from import ListEmailFrom
from .list_email_from_email_address import ListEmailFromEmailAddress
from .list_email_importance import ListEmailImportance
from .list_email_inference_classification import ListEmailInferenceClassification
from .list_email_location import ListEmailLocation
from .list_email_previous_end_date_time import ListEmailPreviousEndDateTime
from .list_email_previous_location import ListEmailPreviousLocation
from .list_email_previous_start_date_time import ListEmailPreviousStartDateTime
from .list_email_recurrence import ListEmailRecurrence
from .list_email_recurrence_pattern import ListEmailRecurrencePattern
from .list_email_recurrence_range import ListEmailRecurrenceRange
from .list_email_reply_to_array_item_ref import ListEmailReplyToArrayItemRef
from .list_email_reply_to_email_address import ListEmailReplyToEmailAddress
from .list_email_sender import ListEmailSender
from .list_email_sender_email_address import ListEmailSenderEmailAddress
from .list_email_start_date_time import ListEmailStartDateTime
from .list_email_to_recipients_array_item_ref import ListEmailToRecipientsArrayItemRef
from .list_email_to_recipients_email_address import ListEmailToRecipientsEmailAddress
from .mark_email_reador_unread_request import MarkEmailReadorUnreadRequest
from .mark_email_reador_unread_request_mark_as import MarkEmailReadorUnreadRequestMarkAs
from .mark_email_reador_unread_response import MarkEmailReadorUnreadResponse
from .mark_email_reador_unread_response_body import MarkEmailReadorUnreadResponseBody
from .mark_email_reador_unread_response_flag import MarkEmailReadorUnreadResponseFlag
from .mark_email_reador_unread_response_from import MarkEmailReadorUnreadResponseFrom
from .mark_email_reador_unread_response_from_email_address import (
    MarkEmailReadorUnreadResponseFromEmailAddress,
)
from .mark_email_reador_unread_response_mark_as import (
    MarkEmailReadorUnreadResponseMarkAs,
)
from .mark_email_reador_unread_response_reply_to_array_item_ref import (
    MarkEmailReadorUnreadResponseReplyToArrayItemRef,
)
from .mark_email_reador_unread_response_reply_to_email_address import (
    MarkEmailReadorUnreadResponseReplyToEmailAddress,
)
from .mark_email_reador_unread_response_sender import (
    MarkEmailReadorUnreadResponseSender,
)
from .mark_email_reador_unread_response_sender_email_address import (
    MarkEmailReadorUnreadResponseSenderEmailAddress,
)
from .mark_email_reador_unread_response_to_recipients_array_item_ref import (
    MarkEmailReadorUnreadResponseToRecipientsArrayItemRef,
)
from .mark_email_reador_unread_response_to_recipients_email_address import (
    MarkEmailReadorUnreadResponseToRecipientsEmailAddress,
)
from .move_email_request import MoveEmailRequest
from .move_email_response import MoveEmailResponse
from .move_email_response_body import MoveEmailResponseBody
from .move_email_response_flag import MoveEmailResponseFlag
from .move_email_response_from import MoveEmailResponseFrom
from .move_email_response_from_email_address import MoveEmailResponseFromEmailAddress
from .move_email_response_sender import MoveEmailResponseSender
from .move_email_response_sender_email_address import (
    MoveEmailResponseSenderEmailAddress,
)
from .move_email_response_to_recipients_array_item_ref import (
    MoveEmailResponseToRecipientsArrayItemRef,
)
from .move_email_response_to_recipients_email_address import (
    MoveEmailResponseToRecipientsEmailAddress,
)
from .reply_to_email_request import ReplyToEmailRequest
from .reply_to_email_request_message import ReplyToEmailRequestMessage
from .reply_to_email_request_message_importance import (
    ReplyToEmailRequestMessageImportance,
)
from .respondto_event_invitation_request import RespondtoEventInvitationRequest
from .respondto_event_invitation_response import RespondtoEventInvitationResponse
from .send_email_request import SendEmailRequest
from .send_email_request_message import SendEmailRequestMessage
from .send_email_request_message_body import SendEmailRequestMessageBody
from .send_email_request_message_email_classification import (
    SendEmailRequestMessageEmailClassification,
)
from .send_email_request_message_importance import SendEmailRequestMessageImportance
from .send_email_response import SendEmailResponse
from .set_email_categories_request import SetEmailCategoriesRequest
from .set_email_categories_response import SetEmailCategoriesResponse
from .set_email_categories_response_body import SetEmailCategoriesResponseBody
from .set_email_categories_response_flag import SetEmailCategoriesResponseFlag
from .set_email_categories_response_from import SetEmailCategoriesResponseFrom
from .set_email_categories_response_from_email_address import (
    SetEmailCategoriesResponseFromEmailAddress,
)
from .set_email_categories_response_reply_to_array_item_ref import (
    SetEmailCategoriesResponseReplyToArrayItemRef,
)
from .set_email_categories_response_reply_to_email_address import (
    SetEmailCategoriesResponseReplyToEmailAddress,
)
from .set_email_categories_response_sender import SetEmailCategoriesResponseSender
from .set_email_categories_response_sender_email_address import (
    SetEmailCategoriesResponseSenderEmailAddress,
)
from .set_email_categories_response_to_recipients_array_item_ref import (
    SetEmailCategoriesResponseToRecipientsArrayItemRef,
)
from .set_email_categories_response_to_recipients_email_address import (
    SetEmailCategoriesResponseToRecipientsEmailAddress,
)
from .turn_off_automatic_replies_request import TurnOffAutomaticRepliesRequest
from .turn_off_automatic_replies_request_automatic_replies_setting import (
    TurnOffAutomaticRepliesRequestAutomaticRepliesSetting,
)
from .turn_off_automatic_replies_response import TurnOffAutomaticRepliesResponse
from .turn_off_automatic_replies_response_automatic_replies_setting import (
    TurnOffAutomaticRepliesResponseAutomaticRepliesSetting,
)
from .turn_off_automatic_replies_response_automatic_replies_setting_scheduled_end_date_time import (
    TurnOffAutomaticRepliesResponseAutomaticRepliesSettingScheduledEndDateTime,
)
from .turn_off_automatic_replies_response_automatic_replies_setting_scheduled_start_date_time import (
    TurnOffAutomaticRepliesResponseAutomaticRepliesSettingScheduledStartDateTime,
)
from .turn_on_automatic_replies_request import TurnOnAutomaticRepliesRequest
from .turn_on_automatic_replies_request_automatic_replies_setting import (
    TurnOnAutomaticRepliesRequestAutomaticRepliesSetting,
)
from .turn_on_automatic_replies_request_automatic_replies_setting_scheduled_end_date_time import (
    TurnOnAutomaticRepliesRequestAutomaticRepliesSettingScheduledEndDateTime,
)
from .turn_on_automatic_replies_request_automatic_replies_setting_scheduled_start_date_time import (
    TurnOnAutomaticRepliesRequestAutomaticRepliesSettingScheduledStartDateTime,
)
from .turn_on_automatic_replies_request_automatic_replies_setting_send_replies_outside_user_organization import (
    TurnOnAutomaticRepliesRequestAutomaticRepliesSettingSendRepliesOutsideUserOrganization,
)
from .turn_on_automatic_replies_response import TurnOnAutomaticRepliesResponse
from .turn_on_automatic_replies_response_automatic_replies_setting import (
    TurnOnAutomaticRepliesResponseAutomaticRepliesSetting,
)
from .turn_on_automatic_replies_response_automatic_replies_setting_scheduled_end_date_time import (
    TurnOnAutomaticRepliesResponseAutomaticRepliesSettingScheduledEndDateTime,
)
from .turn_on_automatic_replies_response_automatic_replies_setting_scheduled_start_date_time import (
    TurnOnAutomaticRepliesResponseAutomaticRepliesSettingScheduledStartDateTime,
)
from .turn_on_automatic_replies_response_automatic_replies_setting_send_replies_outside_user_organization import (
    TurnOnAutomaticRepliesResponseAutomaticRepliesSettingSendRepliesOutsideUserOrganization,
)
from .update_event_request import UpdateEventRequest
from .update_event_request_body import UpdateEventRequestBody
from .update_event_request_change_categories import UpdateEventRequestChangeCategories
from .update_event_request_end import UpdateEventRequestEnd
from .update_event_request_importance import UpdateEventRequestImportance
from .update_event_request_location import UpdateEventRequestLocation
from .update_event_request_show_as import UpdateEventRequestShowAs
from .update_event_request_start import UpdateEventRequestStart
from .update_event_response import UpdateEventResponse
from .update_event_response_change_attachment import UpdateEventResponseChangeAttachment
from .update_event_response_importance import UpdateEventResponseImportance
from .update_event_response_show_as import UpdateEventResponseShowAs

__all__ = (
    "ArchiveEmailResponse",
    "ArchiveEmailResponseBody",
    "ArchiveEmailResponseFlag",
    "ArchiveEmailResponseFrom",
    "ArchiveEmailResponseFromEmailAddress",
    "ArchiveEmailResponseSender",
    "ArchiveEmailResponseSenderEmailAddress",
    "ArchiveEmailResponseToRecipientsArrayItemRef",
    "ArchiveEmailResponseToRecipientsEmailAddress",
    "CreateEventRequest",
    "CreateEventRequestBody",
    "CreateEventRequestEnd",
    "CreateEventRequestImportance",
    "CreateEventRequestLocation",
    "CreateEventRequestSensitivity",
    "CreateEventRequestShowAs",
    "CreateEventRequestStart",
    "CreateEventResponse",
    "CreateEventResponseAttendeesArrayItemRef",
    "CreateEventResponseAttendeesEmailAddress",
    "CreateEventResponseAttendeesStatus",
    "CreateEventResponseEventType",
    "CreateEventResponseLocation",
    "CreateEventResponseLocationsArrayItemRef",
    "CreateEventResponseOnlineMeeting",
    "CreateEventResponseOrganizer",
    "CreateEventResponseOrganizerEmailAddress",
    "CreateEventResponseResponseStatus",
    "DefaultError",
    "ForwardEmailRequest",
    "ForwardEmailRequestMessage",
    "ForwardEventRequest",
    "GetCalendars",
    "GetCalendarsOwner",
    "GetEmailFolders",
    "GetEventByIDResponse",
    "GetEventByIDResponseAttendeesArrayItemRef",
    "GetEventByIDResponseAttendeesEmailAddress",
    "GetEventByIDResponseAttendeesStatus",
    "GetEventByIDResponseBody",
    "GetEventByIDResponseEnd",
    "GetEventByIDResponseEventType",
    "GetEventByIDResponseImportance",
    "GetEventByIDResponseLocation",
    "GetEventByIDResponseLocationsArrayItemRef",
    "GetEventByIDResponseOnlineMeeting",
    "GetEventByIDResponseOrganizer",
    "GetEventByIDResponseOrganizerEmailAddress",
    "GetEventByIDResponseRecurrence",
    "GetEventByIDResponseRecurrencePattern",
    "GetEventByIDResponseRecurrenceRange",
    "GetEventByIDResponseResponseStatus",
    "GetEventByIDResponseSensitivity",
    "GetEventByIDResponseShowAs",
    "GetEventByIDResponseStart",
    "GetEventList",
    "GetEventListAttendeesArrayItemRef",
    "GetEventListAttendeesEmailAddress",
    "GetEventListAttendeesStatus",
    "GetEventListBody",
    "GetEventListCalendar",
    "GetEventListCalendarodata",
    "GetEventListCalendarOwner",
    "GetEventListEnd",
    "GetEventListLocation",
    "GetEventListodata",
    "GetEventListOrganizer",
    "GetEventListOrganizerEmailAddress",
    "GetEventListResponseStatus",
    "GetEventListStart",
    "GetNewestEmailResponse",
    "GetNewestEmailResponseBody",
    "GetNewestEmailResponseFlag",
    "GetNewestEmailResponseFrom",
    "GetNewestEmailResponseFromEmailAddress",
    "GetNewestEmailResponseSender",
    "GetNewestEmailResponseSenderEmailAddress",
    "GetNewestEmailResponseToRecipientsArrayItemRef",
    "GetNewestEmailResponseToRecipientsEmailAddress",
    "ListEmail",
    "ListEmailBccRecipientsArrayItemRef",
    "ListEmailBccRecipientsEmailAddress",
    "ListEmailBody",
    "ListEmailCcRecipientsArrayItemRef",
    "ListEmailCcRecipientsEmailAddress",
    "ListEmailEndDateTime",
    "ListEmailFlag",
    "ListEmailFrom",
    "ListEmailFromEmailAddress",
    "ListEmailImportance",
    "ListEmailInferenceClassification",
    "ListEmailLocation",
    "ListEmailPreviousEndDateTime",
    "ListEmailPreviousLocation",
    "ListEmailPreviousStartDateTime",
    "ListEmailRecurrence",
    "ListEmailRecurrencePattern",
    "ListEmailRecurrenceRange",
    "ListEmailReplyToArrayItemRef",
    "ListEmailReplyToEmailAddress",
    "ListEmailSender",
    "ListEmailSenderEmailAddress",
    "ListEmailStartDateTime",
    "ListEmailToRecipientsArrayItemRef",
    "ListEmailToRecipientsEmailAddress",
    "MarkEmailReadorUnreadRequest",
    "MarkEmailReadorUnreadRequestMarkAs",
    "MarkEmailReadorUnreadResponse",
    "MarkEmailReadorUnreadResponseBody",
    "MarkEmailReadorUnreadResponseFlag",
    "MarkEmailReadorUnreadResponseFrom",
    "MarkEmailReadorUnreadResponseFromEmailAddress",
    "MarkEmailReadorUnreadResponseMarkAs",
    "MarkEmailReadorUnreadResponseReplyToArrayItemRef",
    "MarkEmailReadorUnreadResponseReplyToEmailAddress",
    "MarkEmailReadorUnreadResponseSender",
    "MarkEmailReadorUnreadResponseSenderEmailAddress",
    "MarkEmailReadorUnreadResponseToRecipientsArrayItemRef",
    "MarkEmailReadorUnreadResponseToRecipientsEmailAddress",
    "MoveEmailRequest",
    "MoveEmailResponse",
    "MoveEmailResponseBody",
    "MoveEmailResponseFlag",
    "MoveEmailResponseFrom",
    "MoveEmailResponseFromEmailAddress",
    "MoveEmailResponseSender",
    "MoveEmailResponseSenderEmailAddress",
    "MoveEmailResponseToRecipientsArrayItemRef",
    "MoveEmailResponseToRecipientsEmailAddress",
    "ReplyToEmailRequest",
    "ReplyToEmailRequestMessage",
    "ReplyToEmailRequestMessageImportance",
    "RespondtoEventInvitationRequest",
    "RespondtoEventInvitationResponse",
    "SendEmailRequest",
    "SendEmailRequestMessage",
    "SendEmailRequestMessageBody",
    "SendEmailRequestMessageEmailClassification",
    "SendEmailRequestMessageImportance",
    "SendEmailResponse",
    "SetEmailCategoriesRequest",
    "SetEmailCategoriesResponse",
    "SetEmailCategoriesResponseBody",
    "SetEmailCategoriesResponseFlag",
    "SetEmailCategoriesResponseFrom",
    "SetEmailCategoriesResponseFromEmailAddress",
    "SetEmailCategoriesResponseReplyToArrayItemRef",
    "SetEmailCategoriesResponseReplyToEmailAddress",
    "SetEmailCategoriesResponseSender",
    "SetEmailCategoriesResponseSenderEmailAddress",
    "SetEmailCategoriesResponseToRecipientsArrayItemRef",
    "SetEmailCategoriesResponseToRecipientsEmailAddress",
    "TurnOffAutomaticRepliesRequest",
    "TurnOffAutomaticRepliesRequestAutomaticRepliesSetting",
    "TurnOffAutomaticRepliesResponse",
    "TurnOffAutomaticRepliesResponseAutomaticRepliesSetting",
    "TurnOffAutomaticRepliesResponseAutomaticRepliesSettingScheduledEndDateTime",
    "TurnOffAutomaticRepliesResponseAutomaticRepliesSettingScheduledStartDateTime",
    "TurnOnAutomaticRepliesRequest",
    "TurnOnAutomaticRepliesRequestAutomaticRepliesSetting",
    "TurnOnAutomaticRepliesRequestAutomaticRepliesSettingScheduledEndDateTime",
    "TurnOnAutomaticRepliesRequestAutomaticRepliesSettingScheduledStartDateTime",
    "TurnOnAutomaticRepliesRequestAutomaticRepliesSettingSendRepliesOutsideUserOrganization",
    "TurnOnAutomaticRepliesResponse",
    "TurnOnAutomaticRepliesResponseAutomaticRepliesSetting",
    "TurnOnAutomaticRepliesResponseAutomaticRepliesSettingScheduledEndDateTime",
    "TurnOnAutomaticRepliesResponseAutomaticRepliesSettingScheduledStartDateTime",
    "TurnOnAutomaticRepliesResponseAutomaticRepliesSettingSendRepliesOutsideUserOrganization",
    "UpdateEventRequest",
    "UpdateEventRequestBody",
    "UpdateEventRequestChangeCategories",
    "UpdateEventRequestEnd",
    "UpdateEventRequestImportance",
    "UpdateEventRequestLocation",
    "UpdateEventRequestShowAs",
    "UpdateEventRequestStart",
    "UpdateEventResponse",
    "UpdateEventResponseChangeAttachment",
    "UpdateEventResponseImportance",
    "UpdateEventResponseShowAs",
)
