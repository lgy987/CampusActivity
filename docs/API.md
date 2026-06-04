# Table of Contents

* [models](#models)
  * [Integer](#models.Integer)
  * [String](#models.String)
  * [DateTime](#models.DateTime)
  * [Boolean](#models.Boolean)
  * [User](#models.User)
    * [id](#models.User.id)
    * [student\_id](#models.User.student_id)
    * [email](#models.User.email)
    * [username](#models.User.username)
    * [password](#models.User.password)
    * [gender](#models.User.gender)
    * [college](#models.User.college)
    * [major](#models.User.major)
    * [grade](#models.User.grade)
    * [phone](#models.User.phone)
    * [avatar](#models.User.avatar)
    * [status](#models.User.status)
  * [Organizer](#models.Organizer)
    * [id](#models.Organizer.id)
    * [email](#models.Organizer.email)
    * [org\_name](#models.Organizer.org_name)
    * [password](#models.Organizer.password)
    * [org\_proof\_text](#models.Organizer.org_proof_text)
    * [org\_proof\_image](#models.Organizer.org_proof_image)
    * [avatar](#models.Organizer.avatar)
    * [status](#models.Organizer.status)
    * [reject\_reason](#models.Organizer.reject_reason)
  * [Admin](#models.Admin)
    * [id](#models.Admin.id)
    * [admin\_no](#models.Admin.admin_no)
    * [email](#models.Admin.email)
    * [password](#models.Admin.password)
    * [username](#models.Admin.username)
    * [avatar](#models.Admin.avatar)
    * [role](#models.Admin.role)
    * [status](#models.Admin.status)
  * [Category](#models.Category)
    * [id](#models.Category.id)
    * [name](#models.Category.name)
    * [parent\_id](#models.Category.parent_id)
    * [level](#models.Category.level)
    * [sort\_order](#models.Category.sort_order)
  * [Activity](#models.Activity)
    * [id](#models.Activity.id)
    * [organizer\_id](#models.Activity.organizer_id)
    * [category\_id](#models.Activity.category_id)
    * [name](#models.Activity.name)
    * [start\_time](#models.Activity.start_time)
    * [end\_time](#models.Activity.end_time)
    * [campus](#models.Activity.campus)
    * [location](#models.Activity.location)
    * [max\_participants](#models.Activity.max_participants)
    * [current\_participants](#models.Activity.current_participants)
    * [registration\_deadline](#models.Activity.registration_deadline)
    * [cancel\_deadline](#models.Activity.cancel_deadline)
    * [description](#models.Activity.description)
    * [status](#models.Activity.status)
    * [reject\_reason](#models.Activity.reject_reason)
    * [organizer](#models.Activity.organizer)
    * [category](#models.Activity.category)
  * [ActivityRevision](#models.ActivityRevision)
    * [id](#models.ActivityRevision.id)
    * [activity\_id](#models.ActivityRevision.activity_id)
    * [organizer\_id](#models.ActivityRevision.organizer_id)
    * [category\_id](#models.ActivityRevision.category_id)
    * [name](#models.ActivityRevision.name)
    * [start\_time](#models.ActivityRevision.start_time)
    * [end\_time](#models.ActivityRevision.end_time)
    * [campus](#models.ActivityRevision.campus)
    * [location](#models.ActivityRevision.location)
    * [max\_participants](#models.ActivityRevision.max_participants)
    * [registration\_deadline](#models.ActivityRevision.registration_deadline)
    * [cancel\_deadline](#models.ActivityRevision.cancel_deadline)
    * [description](#models.ActivityRevision.description)
    * [reject\_reason](#models.ActivityRevision.reject_reason)
  * [Registration](#models.Registration)
    * [id](#models.Registration.id)
    * [activity\_id](#models.Registration.activity_id)
    * [user\_id](#models.Registration.user_id)
    * [registration\_time](#models.Registration.registration_time)
    * [status](#models.Registration.status)
    * [reject\_count](#models.Registration.reject_count)
    * [last\_reject\_time](#models.Registration.last_reject_time)
    * [reject\_reason](#models.Registration.reject_reason)
    * [slot\_release\_at](#models.Registration.slot_release_at)
    * [activity](#models.Registration.activity)
    * [user](#models.Registration.user)
  * [Checkin](#models.Checkin)
    * [id](#models.Checkin.id)
    * [activity\_id](#models.Checkin.activity_id)
    * [user\_id](#models.Checkin.user_id)
    * [checkin\_time](#models.Checkin.checkin_time)
    * [checkin\_method](#models.Checkin.checkin_method)
    * [operator\_id](#models.Checkin.operator_id)
    * [activity](#models.Checkin.activity)
    * [user](#models.Checkin.user)
  * [ActivityCheckinCode](#models.ActivityCheckinCode)
    * [id](#models.ActivityCheckinCode.id)
    * [activity\_id](#models.ActivityCheckinCode.activity_id)
    * [checkin\_code](#models.ActivityCheckinCode.checkin_code)
    * [created\_at](#models.ActivityCheckinCode.created_at)
    * [activity](#models.ActivityCheckinCode.activity)
  * [Announcement](#models.Announcement)
    * [id](#models.Announcement.id)
    * [admin\_id](#models.Announcement.admin_id)
    * [title](#models.Announcement.title)
    * [content](#models.Announcement.content)
    * [start\_time](#models.Announcement.start_time)
    * [end\_time](#models.Announcement.end_time)
    * [created\_at](#models.Announcement.created_at)
  * [Notification](#models.Notification)
    * [id](#models.Notification.id)
    * [receiver\_type](#models.Notification.receiver_type)
    * [receiver\_id](#models.Notification.receiver_id)
    * [title](#models.Notification.title)
    * [content](#models.Notification.content)
    * [type](#models.Notification.type)
    * [related\_id](#models.Notification.related_id)
    * [is\_read](#models.Notification.is_read)
    * [created\_at](#models.Notification.created_at)
* [app.services.auth\_service](#app.services.auth_service)
  * [BusinessError](#app.services.auth_service.BusinessError)
  * [create\_token](#app.services.auth_service.create_token)
  * [User](#app.services.auth_service.User)
  * [Organizer](#app.services.auth_service.Organizer)
  * [Admin](#app.services.auth_service.Admin)
  * [AuthService](#app.services.auth_service.AuthService)
    * [register\_user](#app.services.auth_service.AuthService.register_user)
    * [register\_organizer](#app.services.auth_service.AuthService.register_organizer)
    * [login](#app.services.auth_service.AuthService.login)
    * [upload\_organizer\_proof](#app.services.auth_service.AuthService.upload_organizer_proof)
* [app.services.user\_service](#app.services.user_service)
  * [BusinessError](#app.services.user_service.BusinessError)
  * [User](#app.services.user_service.User)
  * [Organizer](#app.services.user_service.Organizer)
  * [Admin](#app.services.user_service.Admin)
  * [Checkin](#app.services.user_service.Checkin)
  * [UserService](#app.services.user_service.UserService)
    * [ACHIEVEMENT\_LEVELS](#app.services.user_service.UserService.ACHIEVEMENT_LEVELS)
    * [get\_profile](#app.services.user_service.UserService.get_profile)
    * [update\_profile](#app.services.user_service.UserService.update_profile)
    * [update\_avatar\_url](#app.services.user_service.UserService.update_avatar_url)
    * [upload\_avatar](#app.services.user_service.UserService.upload_avatar)
    * [reset\_password](#app.services.user_service.UserService.reset_password)
    * [delete\_account](#app.services.user_service.UserService.delete_account)
    * [list\_users](#app.services.user_service.UserService.list_users)
    * [get\_user\_detail](#app.services.user_service.UserService.get_user_detail)
    * [list\_organizers](#app.services.user_service.UserService.list_organizers)
    * [get\_organizer\_detail](#app.services.user_service.UserService.get_organizer_detail)
    * [review\_organizer](#app.services.user_service.UserService.review_organizer)
    * [create\_admin](#app.services.user_service.UserService.create_admin)
    * [list\_admins](#app.services.user_service.UserService.list_admins)
    * [delete\_admin](#app.services.user_service.UserService.delete_admin)
* [app.services.activity\_service](#app.services.activity_service)
  * [BusinessError](#app.services.activity_service.BusinessError)
  * [dt](#app.services.activity_service.dt)
  * [NotificationService](#app.services.activity_service.NotificationService)
  * [Activity](#app.services.activity_service.Activity)
  * [ActivityRevision](#app.services.activity_service.ActivityRevision)
  * [Category](#app.services.activity_service.Category)
  * [Organizer](#app.services.activity_service.Organizer)
  * [Registration](#app.services.activity_service.Registration)
  * [ActivityService](#app.services.activity_service.ActivityService)
    * [ACTIVE\_STATUSES](#app.services.activity_service.ActivityService.ACTIVE_STATUSES)
    * [EDITABLE\_DIRECT\_STATUSES](#app.services.activity_service.ActivityService.EDITABLE_DIRECT_STATUSES)
    * [create\_activity](#app.services.activity_service.ActivityService.create_activity)
    * [submit\_activity](#app.services.activity_service.ActivityService.submit_activity)
    * [list\_activities](#app.services.activity_service.ActivityService.list_activities)
    * [get\_detail](#app.services.activity_service.ActivityService.get_detail)
    * [update\_activity](#app.services.activity_service.ActivityService.update_activity)
    * [delete\_activity](#app.services.activity_service.ActivityService.delete_activity)
    * [get\_my\_activities](#app.services.activity_service.ActivityService.get_my_activities)
    * [list\_review\_activities](#app.services.activity_service.ActivityService.list_review_activities)
    * [review\_activity](#app.services.activity_service.ActivityService.review_activity)
    * [remove\_activity](#app.services.activity_service.ActivityService.remove_activity)
* [app.services.registration\_service](#app.services.registration_service)
  * [BusinessError](#app.services.registration_service.BusinessError)
  * [dt](#app.services.registration_service.dt)
  * [NotificationService](#app.services.registration_service.NotificationService)
  * [Activity](#app.services.registration_service.Activity)
  * [Registration](#app.services.registration_service.Registration)
  * [User](#app.services.registration_service.User)
  * [Checkin](#app.services.registration_service.Checkin)
  * [RegistrationService](#app.services.registration_service.RegistrationService)
    * [ACTIVE\_STATUSES](#app.services.registration_service.RegistrationService.ACTIVE_STATUSES)
    * [register](#app.services.registration_service.RegistrationService.register)
    * [cancel](#app.services.registration_service.RegistrationService.cancel)
    * [get\_my\_registrations](#app.services.registration_service.RegistrationService.get_my_registrations)
    * [get\_activity\_registrations](#app.services.registration_service.RegistrationService.get_activity_registrations)
    * [reject\_registration](#app.services.registration_service.RegistrationService.reject_registration)
    * [get\_registration\_stats](#app.services.registration_service.RegistrationService.get_registration_stats)
* [app.services.checkin\_service](#app.services.checkin_service)
  * [BusinessError](#app.services.checkin_service.BusinessError)
  * [dt](#app.services.checkin_service.dt)
  * [NotificationService](#app.services.checkin_service.NotificationService)
  * [Activity](#app.services.checkin_service.Activity)
  * [ActivityCheckinCode](#app.services.checkin_service.ActivityCheckinCode)
  * [Registration](#app.services.checkin_service.Registration)
  * [Checkin](#app.services.checkin_service.Checkin)
  * [User](#app.services.checkin_service.User)
  * [CheckinService](#app.services.checkin_service.CheckinService)
    * [ACTIVE\_STATUSES](#app.services.checkin_service.CheckinService.ACTIVE_STATUSES)
    * [get\_checkin\_code](#app.services.checkin_service.CheckinService.get_checkin_code)
    * [checkin](#app.services.checkin_service.CheckinService.checkin)
    * [manual\_checkin](#app.services.checkin_service.CheckinService.manual_checkin)
    * [get\_my\_checkins](#app.services.checkin_service.CheckinService.get_my_checkins)
    * [get\_checkin\_stats](#app.services.checkin_service.CheckinService.get_checkin_stats)
* [app.services.notification\_service](#app.services.notification_service)
  * [BusinessError](#app.services.notification_service.BusinessError)
  * [dt](#app.services.notification_service.dt)
  * [Notification](#app.services.notification_service.Notification)
  * [Announcement](#app.services.notification_service.Announcement)
  * [NotificationService](#app.services.notification_service.NotificationService)
    * [create\_notification](#app.services.notification_service.NotificationService.create_notification)
    * [list\_notifications](#app.services.notification_service.NotificationService.list_notifications)
    * [mark\_notification\_read](#app.services.notification_service.NotificationService.mark_notification_read)
    * [create\_announcement](#app.services.notification_service.NotificationService.create_announcement)
    * [list\_announcements](#app.services.notification_service.NotificationService.list_announcements)
    * [list\_valid\_announcements](#app.services.notification_service.NotificationService.list_valid_announcements)
    * [delete\_announcement](#app.services.notification_service.NotificationService.delete_announcement)
* [app.services.category\_service](#app.services.category_service)
  * [Category](#app.services.category_service.Category)
  * [CategoryService](#app.services.category_service.CategoryService)
    * [get\_category\_tree](#app.services.category_service.CategoryService.get_category_tree)
* [app.services.stats\_service](#app.services.stats_service)
  * [BusinessError](#app.services.stats_service.BusinessError)
  * [Activity](#app.services.stats_service.Activity)
  * [User](#app.services.stats_service.User)
  * [Organizer](#app.services.stats_service.Organizer)
  * [Admin](#app.services.stats_service.Admin)
  * [Registration](#app.services.stats_service.Registration)
  * [Checkin](#app.services.stats_service.Checkin)
  * [Category](#app.services.stats_service.Category)
  * [StatsService](#app.services.stats_service.StatsService)
    * [ACTIVE\_STATUSES](#app.services.stats_service.StatsService.ACTIVE_STATUSES)
    * [PLATFORM\_ACTIVITY\_STATUSES](#app.services.stats_service.StatsService.PLATFORM_ACTIVITY_STATUSES)
    * [get\_platform\_stats](#app.services.stats_service.StatsService.get_platform_stats)
    * [get\_leaderboard](#app.services.stats_service.StatsService.get_leaderboard)
* [app.task.scheduler](#app.task.scheduler)
  * [BackgroundScheduler](#app.task.scheduler.BackgroundScheduler)
  * [IntervalTrigger](#app.task.scheduler.IntervalTrigger)
  * [Activity](#app.task.scheduler.Activity)
  * [Registration](#app.task.scheduler.Registration)
  * [NotificationService](#app.task.scheduler.NotificationService)
  * [update\_activity\_statuses](#app.task.scheduler.update_activity_statuses)
  * [send\_activity\_reminders](#app.task.scheduler.send_activity_reminders)
  * [start\_scheduler](#app.task.scheduler.start_scheduler)
  * [stop\_scheduler](#app.task.scheduler.stop_scheduler)
* [app.common.auth](#app.common.auth)
  * [create\_token](#app.common.auth.create_token)
  * [decode\_token](#app.common.auth.decode_token)
* [app.common.database](#app.common.database)
  * [contextmanager](#app.common.database.contextmanager)
  * [create\_engine](#app.common.database.create_engine)
  * [sessionmaker](#app.common.database.sessionmaker)
  * [scoped\_session](#app.common.database.scoped_session)
  * [get\_config](#app.common.database.get_config)
  * [config](#app.common.database.config)
* [app.common.errors](#app.common.errors)
  * [BusinessError](#app.common.errors.BusinessError)
    * [to\_response](#app.common.errors.BusinessError.to_response)
  * [register\_error\_handlers](#app.common.errors.register_error_handlers)
* [app.common.response](#app.common.response)
  * [success](#app.common.response.success)
* [app.common.serializers](#app.common.serializers)
  * [timezone](#app.common.serializers.timezone)
  * [dt](#app.common.serializers.dt)
* [app.api.deps](#app.api.deps)
  * [wraps](#app.api.deps.wraps)
  * [decode\_token](#app.api.deps.decode_token)
  * [BusinessError](#app.api.deps.BusinessError)
  * [get\_json\_data](#app.api.deps.get_json_data)
  * [get\_current\_user](#app.api.deps.get_current_user)
  * [require\_auth](#app.api.deps.require_auth)
  * [require\_role](#app.api.deps.require_role)
* [app.api.auth](#app.api.auth)
  * [get\_json\_data](#app.api.auth.get_json_data)
  * [success](#app.api.auth.success)
  * [BusinessError](#app.api.auth.BusinessError)
  * [AuthService](#app.api.auth.AuthService)
  * [bp](#app.api.auth.bp)
  * [register\_user](#app.api.auth.register_user)
  * [register\_organizer](#app.api.auth.register_organizer)
  * [login](#app.api.auth.login)
  * [logout](#app.api.auth.logout)
  * [upload\_organizer\_proof](#app.api.auth.upload_organizer_proof)
* [app.api.user](#app.api.user)
  * [get\_json\_data](#app.api.user.get_json_data)
  * [require\_auth](#app.api.user.require_auth)
  * [get\_current\_user](#app.api.user.get_current_user)
  * [success](#app.api.user.success)
  * [BusinessError](#app.api.user.BusinessError)
  * [UserService](#app.api.user.UserService)
  * [bp](#app.api.user.bp)
  * [get\_profile](#app.api.user.get_profile)
  * [update\_profile](#app.api.user.update_profile)
  * [update\_avatar](#app.api.user.update_avatar)
  * [reset\_password](#app.api.user.reset_password)
  * [delete\_account](#app.api.user.delete_account)
* [app.api.admin\_users](#app.api.admin_users)
  * [get\_json\_data](#app.api.admin_users.get_json_data)
  * [require\_auth](#app.api.admin_users.require_auth)
  * [require\_role](#app.api.admin_users.require_role)
  * [success](#app.api.admin_users.success)
  * [BusinessError](#app.api.admin_users.BusinessError)
  * [UserService](#app.api.admin_users.UserService)
  * [bp](#app.api.admin_users.bp)
  * [list\_users](#app.api.admin_users.list_users)
  * [get\_user\_detail](#app.api.admin_users.get_user_detail)
  * [list\_organizers](#app.api.admin_users.list_organizers)
  * [get\_organizer\_detail](#app.api.admin_users.get_organizer_detail)
  * [review\_organizer](#app.api.admin_users.review_organizer)
  * [create\_admin](#app.api.admin_users.create_admin)
  * [list\_admins](#app.api.admin_users.list_admins)
  * [delete\_admin](#app.api.admin_users.delete_admin)
* [app.api.categories](#app.api.categories)
  * [success](#app.api.categories.success)
  * [CategoryService](#app.api.categories.CategoryService)
  * [bp](#app.api.categories.bp)
  * [get\_categories](#app.api.categories.get_categories)
* [app.api.activities](#app.api.activities)
  * [get\_json\_data](#app.api.activities.get_json_data)
  * [require\_auth](#app.api.activities.require_auth)
  * [require\_role](#app.api.activities.require_role)
  * [success](#app.api.activities.success)
  * [BusinessError](#app.api.activities.BusinessError)
  * [ActivityService](#app.api.activities.ActivityService)
  * [bp](#app.api.activities.bp)
  * [create\_activity](#app.api.activities.create_activity)
  * [submit\_activity](#app.api.activities.submit_activity)
  * [list\_activities](#app.api.activities.list_activities)
  * [get\_activity\_detail](#app.api.activities.get_activity_detail)
  * [update\_activity](#app.api.activities.update_activity)
  * [delete\_activity](#app.api.activities.delete_activity)
  * [get\_my\_activities](#app.api.activities.get_my_activities)
* [app.api.admin\_activities](#app.api.admin_activities)
  * [get\_json\_data](#app.api.admin_activities.get_json_data)
  * [require\_auth](#app.api.admin_activities.require_auth)
  * [require\_role](#app.api.admin_activities.require_role)
  * [success](#app.api.admin_activities.success)
  * [BusinessError](#app.api.admin_activities.BusinessError)
  * [ActivityService](#app.api.admin_activities.ActivityService)
  * [bp](#app.api.admin_activities.bp)
  * [list\_review\_activities](#app.api.admin_activities.list_review_activities)
  * [get\_admin\_activity\_detail](#app.api.admin_activities.get_admin_activity_detail)
  * [review\_activity](#app.api.admin_activities.review_activity)
  * [remove\_activity](#app.api.admin_activities.remove_activity)
* [app.api.registrations](#app.api.registrations)
  * [get\_json\_data](#app.api.registrations.get_json_data)
  * [require\_auth](#app.api.registrations.require_auth)
  * [require\_role](#app.api.registrations.require_role)
  * [success](#app.api.registrations.success)
  * [BusinessError](#app.api.registrations.BusinessError)
  * [RegistrationService](#app.api.registrations.RegistrationService)
  * [bp](#app.api.registrations.bp)
  * [register\_activity](#app.api.registrations.register_activity)
  * [cancel\_registration](#app.api.registrations.cancel_registration)
  * [get\_my\_registrations](#app.api.registrations.get_my_registrations)
  * [get\_activity\_registrations](#app.api.registrations.get_activity_registrations)
  * [reject\_registration](#app.api.registrations.reject_registration)
  * [get\_registration\_stats](#app.api.registrations.get_registration_stats)
* [app.api.checkin](#app.api.checkin)
  * [get\_json\_data](#app.api.checkin.get_json_data)
  * [require\_auth](#app.api.checkin.require_auth)
  * [require\_role](#app.api.checkin.require_role)
  * [success](#app.api.checkin.success)
  * [BusinessError](#app.api.checkin.BusinessError)
  * [CheckinService](#app.api.checkin.CheckinService)
  * [bp](#app.api.checkin.bp)
  * [get\_checkin\_code](#app.api.checkin.get_checkin_code)
  * [checkin](#app.api.checkin.checkin)
  * [manual\_checkin](#app.api.checkin.manual_checkin)
  * [get\_my\_checkins](#app.api.checkin.get_my_checkins)
  * [get\_checkin\_stats](#app.api.checkin.get_checkin_stats)
* [app.api.notifications](#app.api.notifications)
  * [get\_json\_data](#app.api.notifications.get_json_data)
  * [require\_auth](#app.api.notifications.require_auth)
  * [require\_role](#app.api.notifications.require_role)
  * [success](#app.api.notifications.success)
  * [BusinessError](#app.api.notifications.BusinessError)
  * [NotificationService](#app.api.notifications.NotificationService)
  * [bp](#app.api.notifications.bp)
  * [list\_notifications](#app.api.notifications.list_notifications)
  * [mark\_notification\_read](#app.api.notifications.mark_notification_read)
  * [create\_announcement](#app.api.notifications.create_announcement)
  * [list\_announcements](#app.api.notifications.list_announcements)
  * [delete\_announcement](#app.api.notifications.delete_announcement)
* [app.api.statistics](#app.api.statistics)
  * [require\_auth](#app.api.statistics.require_auth)
  * [require\_role](#app.api.statistics.require_role)
  * [success](#app.api.statistics.success)
  * [StatsService](#app.api.statistics.StatsService)
  * [bp](#app.api.statistics.bp)
  * [admin\_statistics](#app.api.statistics.admin_statistics)
  * [leaderboard](#app.api.statistics.leaderboard)

<a id="models"></a>

# models

<a id="models.Integer"></a>

## Integer

<a id="models.String"></a>

## String

<a id="models.DateTime"></a>

## DateTime

<a id="models.Boolean"></a>

## Boolean

<a id="models.User"></a>

## User Objects

```python
class User(Base)
```

用户表 - 存储普通用户账号信息

<a id="models.User.id"></a>

#### id

用户ID，主键

<a id="models.User.student_id"></a>

#### student\_id

学号，10位数字，唯一索引，用于登录

<a id="models.User.email"></a>

#### email

邮箱，唯一索引，用于登录

<a id="models.User.username"></a>

#### username

用户名/昵称

<a id="models.User.password"></a>

#### password

密码（哈希+盐值）

<a id="models.User.gender"></a>

#### gender

性别：男/女

<a id="models.User.college"></a>

#### college

学院

<a id="models.User.major"></a>

#### major

专业

<a id="models.User.grade"></a>

#### grade

年级，如：2023级

<a id="models.User.phone"></a>

#### phone

联系方式，11位手机号

<a id="models.User.avatar"></a>

#### avatar

头像URL

<a id="models.User.status"></a>

#### status

状态 状态：active-活跃，deleted-注销

<a id="models.Organizer"></a>

## Organizer Objects

```python
class Organizer(Base)
```

组织者表 - 存储活动组织者/社团账号信息

<a id="models.Organizer.id"></a>

#### id

组织者ID，主键

<a id="models.Organizer.email"></a>

#### email

邮箱，唯一索引，用于登录

<a id="models.Organizer.org_name"></a>

#### org\_name

组织名称

<a id="models.Organizer.password"></a>

#### password

密码（哈希+盐值）

<a id="models.Organizer.org_proof_text"></a>

#### org\_proof\_text

组织证明文本

<a id="models.Organizer.org_proof_image"></a>

#### org\_proof\_image

组织证明图片URL

<a id="models.Organizer.avatar"></a>

#### avatar

头像URL

<a id="models.Organizer.status"></a>

#### status

状态：pending-待审核，approved-已通过，rejected-已拒绝，deleted-注销

<a id="models.Organizer.reject_reason"></a>

#### reject\_reason

审核不通过原因

<a id="models.Admin"></a>

## Admin Objects

```python
class Admin(Base)
```

管理员表 - 存储管理员账号信息

<a id="models.Admin.id"></a>

#### id

管理员ID，主键

<a id="models.Admin.admin_no"></a>

#### admin\_no

管理员编号，6位数字，唯一索引

<a id="models.Admin.email"></a>

#### email

邮箱

<a id="models.Admin.password"></a>

#### password

密码（哈希+盐值）

<a id="models.Admin.username"></a>

#### username

管理员名称

<a id="models.Admin.avatar"></a>

#### avatar

头像URL

<a id="models.Admin.role"></a>

#### role

角色：admin-管理员，super_admin-超级管理员

<a id="models.Admin.status"></a>

#### status

状态：active-活跃，deleted-注销

<a id="models.Category"></a>

## Category Objects

```python
class Category(Base)
```

活动分类表 - 存储活动的多级分类

<a id="models.Category.id"></a>

#### id

分类ID，主键

<a id="models.Category.name"></a>

#### name

分类名称

<a id="models.Category.parent_id"></a>

#### parent\_id

父分类ID，0表示一级分类

<a id="models.Category.level"></a>

#### level

层级：1-一级分类，2-二级分类

<a id="models.Category.sort_order"></a>

#### sort\_order

排序序号，数字越小越靠前

<a id="models.Activity"></a>

## Activity Objects

```python
class Activity(Base)
```

活动表 - 存储活动详细信息

<a id="models.Activity.id"></a>

#### id

活动ID，主键

<a id="models.Activity.organizer_id"></a>

#### organizer\_id

发布者ID，关联organizer表

<a id="models.Activity.category_id"></a>

#### category\_id

分类ID，关联category表

<a id="models.Activity.name"></a>

#### name

活动名称

<a id="models.Activity.start_time"></a>

#### start\_time

活动开始时间

<a id="models.Activity.end_time"></a>

#### end\_time

活动结束时间

<a id="models.Activity.campus"></a>

#### campus

校区：良乡/中关村

<a id="models.Activity.location"></a>

#### location

具体地点

<a id="models.Activity.max_participants"></a>

#### max\_participants

人数限制，最小为1

<a id="models.Activity.current_participants"></a>

#### current\_participants

当前报名人数

<a id="models.Activity.registration_deadline"></a>

#### registration\_deadline

报名截止时间

<a id="models.Activity.cancel_deadline"></a>

#### cancel\_deadline

取消报名截止时间

<a id="models.Activity.description"></a>

#### description

活动简介/详情

<a id="models.Activity.status"></a>

#### status

状态：draft-草稿，pending-审核中，rejected-审核未通过，edit_pending-修改审核中，open-报名中，ongoing-进行中，ended-已结束，removed-下架

<a id="models.Activity.reject_reason"></a>

#### reject\_reason

审核不通过原因

<a id="models.Activity.organizer"></a>

#### organizer

关联的组织者信息

<a id="models.Activity.category"></a>

#### category

关联的分类信息

<a id="models.ActivityRevision"></a>

## ActivityRevision Objects

```python
class ActivityRevision(Base)
```

活动修改记录表 - 存储活动修改待审核的版本

<a id="models.ActivityRevision.id"></a>

#### id

修改记录ID，主键

<a id="models.ActivityRevision.activity_id"></a>

#### activity\_id

原活动ID，关联activity表

<a id="models.ActivityRevision.organizer_id"></a>

#### organizer\_id

发布者ID

<a id="models.ActivityRevision.category_id"></a>

#### category\_id

分类ID

<a id="models.ActivityRevision.name"></a>

#### name

活动名称

<a id="models.ActivityRevision.start_time"></a>

#### start\_time

活动开始时间

<a id="models.ActivityRevision.end_time"></a>

#### end\_time

活动结束时间

<a id="models.ActivityRevision.campus"></a>

#### campus

校区：良乡/中关村

<a id="models.ActivityRevision.location"></a>

#### location

具体地点

<a id="models.ActivityRevision.max_participants"></a>

#### max\_participants

人数限制，最小为1

<a id="models.ActivityRevision.registration_deadline"></a>

#### registration\_deadline

报名截止时间

<a id="models.ActivityRevision.cancel_deadline"></a>

#### cancel\_deadline

取消报名截止时间

<a id="models.ActivityRevision.description"></a>

#### description

活动简介

<a id="models.ActivityRevision.reject_reason"></a>

#### reject\_reason

修改审核不通过原因

<a id="models.Registration"></a>

## Registration Objects

```python
class Registration(Base)
```

报名记录表 - 存储用户对活动的报名记录

<a id="models.Registration.id"></a>

#### id

报名记录ID，主键

<a id="models.Registration.activity_id"></a>

#### activity\_id

活动ID

<a id="models.Registration.user_id"></a>

#### user\_id

用户ID

<a id="models.Registration.registration_time"></a>

#### registration\_time

报名时间

<a id="models.Registration.status"></a>

#### status

状态：registered-已报名，cancelled-已取消，rejected-已拒绝，re_registered-再次报名，blocked-不允许报名

<a id="models.Registration.reject_count"></a>

#### reject\_count

被拒绝次数（针对本活动）

<a id="models.Registration.last_reject_time"></a>

#### last\_reject\_time

最后一次被拒绝时间

<a id="models.Registration.reject_reason"></a>

#### reject\_reason

被拒绝原因

<a id="models.Registration.slot_release_at"></a>

#### slot\_release\_at

名额释放时间（当用户取消报名或被拒绝时，记录名额释放的时间点，用于计算冷却期）

<a id="models.Registration.activity"></a>

#### activity

关联的活动信息

<a id="models.Registration.user"></a>

#### user

关联的用户信息

<a id="models.Checkin"></a>

## Checkin Objects

```python
class Checkin(Base)
```

签到记录表 - 存储用户签到记录

<a id="models.Checkin.id"></a>

#### id

签到记录ID，主键

<a id="models.Checkin.activity_id"></a>

#### activity\_id

活动ID

<a id="models.Checkin.user_id"></a>

#### user\_id

用户ID

<a id="models.Checkin.checkin_time"></a>

#### checkin\_time

签到时间

<a id="models.Checkin.checkin_method"></a>

#### checkin\_method

签到方式：code-签到码签到，manual-手动签到

<a id="models.Checkin.operator_id"></a>

#### operator\_id

手动签到操作人ID（组织者ID）

<a id="models.Checkin.activity"></a>

#### activity

关联的活动信息

<a id="models.Checkin.user"></a>

#### user

关联的用户信息

<a id="models.ActivityCheckinCode"></a>

## ActivityCheckinCode Objects

```python
class ActivityCheckinCode(Base)
```

活动签到码表 - 存储活动的签到码

<a id="models.ActivityCheckinCode.id"></a>

#### id

签到码ID，主键

<a id="models.ActivityCheckinCode.activity_id"></a>

#### activity\_id

活动ID，一个活动只有一个签到码

<a id="models.ActivityCheckinCode.checkin_code"></a>

#### checkin\_code

6位签到码

<a id="models.ActivityCheckinCode.created_at"></a>

#### created\_at

签到码生成时间

<a id="models.ActivityCheckinCode.activity"></a>

#### activity

关联的活动信息

<a id="models.Announcement"></a>

## Announcement Objects

```python
class Announcement(Base)
```

系统公告表 - 存储管理员发布的系统公告

<a id="models.Announcement.id"></a>

#### id

公告ID，主键

<a id="models.Announcement.admin_id"></a>

#### admin\_id

发布管理员ID

<a id="models.Announcement.title"></a>

#### title

公告标题

<a id="models.Announcement.content"></a>

#### content

公告正文

<a id="models.Announcement.start_time"></a>

#### start\_time

公告生效时间

<a id="models.Announcement.end_time"></a>

#### end\_time

公告失效时间

<a id="models.Announcement.created_at"></a>

#### created\_at

发布时间

<a id="models.Notification"></a>

## Notification Objects

```python
class Notification(Base)
```

消息通知表 - 存储用户/组织者的系统通知

<a id="models.Notification.id"></a>

#### id

通知ID，主键

<a id="models.Notification.receiver_type"></a>

#### receiver\_type

接收者类型：user-普通用户，organizer-组织者

<a id="models.Notification.receiver_id"></a>

#### receiver\_id

接收者ID

<a id="models.Notification.title"></a>

#### title

通知标题

<a id="models.Notification.content"></a>

#### content

通知内容

<a id="models.Notification.type"></a>

#### type

通知类型：registration_result-报名结果，activity_audit_result-活动审核结果，activity_change-活动变更，violation_result-违规处理，activity_reminder-活动提醒，organizer_audit_result-组织者审核结果

<a id="models.Notification.related_id"></a>

#### related\_id

关联业务ID（如活动ID、报名ID等）

<a id="models.Notification.is_read"></a>

#### is\_read

是否已读：False-未读，True-已读

<a id="models.Notification.created_at"></a>

#### created\_at

通知发送时间

<a id="app.services.auth_service"></a>

# app.services.auth\_service

认证服务模块

提供用户注册、登录、组织者注册、文件上传等功能

<a id="app.services.auth_service.BusinessError"></a>

## BusinessError

<a id="app.services.auth_service.create_token"></a>

## create\_token

<a id="app.services.auth_service.User"></a>

## User

<a id="app.services.auth_service.Organizer"></a>

## Organizer

<a id="app.services.auth_service.Admin"></a>

## Admin

<a id="app.services.auth_service.AuthService"></a>

## AuthService Objects

```python
class AuthService()
```

认证服务类

提供用户认证相关的业务逻辑：
- 普通用户注册
- 组织者注册
- 用户登录（支持三种角色）
- 组织者证明图片上传

<a id="app.services.auth_service.AuthService.register_user"></a>

#### register\_user

```python
@staticmethod
def register_user(data)
```

普通用户注册

流程：
1. 提取并验证用户输入数据
2. 检查学号/邮箱是否已存在
3. 创建用户记录
4. 生成 JWT Token

**Arguments**:

- `data` _dict_ - 用户注册信息，包含以下字段：
  - student_id: 学号（10位数字）
  - email: 邮箱地址
  - username: 用户名
  - password: 密码
  - confirm_password: 确认密码
  - gender: 性别（男/女）
  - college: 学院
  - major: 专业
  - grade: 年级
  - phone: 手机号（可选）
  

**Returns**:

- `dict` - 包含 userId, user_id, role, token 的字典
  

**Raises**:

- `BusinessError` - 学号格式错误、密码不一致、学号/邮箱已存在等

<a id="app.services.auth_service.AuthService.register_organizer"></a>

#### register\_organizer

```python
@staticmethod
def register_organizer(data)
```

组织者注册

流程：
1. 验证密码一致性
2. 检查邮箱是否已存在
3. 如果邮箱对应的账号已注销，则重新激活
4. 否则创建新的组织者账号（状态为 pending 待审核）

**Arguments**:

- `data` _dict_ - 组织者注册信息，包含以下字段：
  - email: 邮箱
  - org_name: 组织名称
  - password: 密码
  - confirm_password: 确认密码
  - org_proof_text: 组织证明文本
  - org_proof_image: 组织证明图片URL（可选）
  

**Returns**:

- `dict` - 包含 userId, organizer_id, role, token 的字典
  

**Raises**:

- `BusinessError` - 密码不一致、邮箱已注册等

<a id="app.services.auth_service.AuthService.login"></a>

#### login

```python
@staticmethod
def login(role, account, password)
```

用户登录（支持三种角色）

流程：
1. 根据角色查询对应的数据表
2. 验证账号是否存在且未被注销
3. 验证密码是否正确
4. 生成并返回 JWT Token

**Arguments**:

- `role` _str_ - 角色类型，可选值：'user' / 'organizer' / 'admin'
- `account` _str_ - 账号
  - user: 学号或邮箱
  - organizer: 邮箱
  - admin: 管理员编号
- `password` _str_ - 密码
  

**Returns**:

- `dict` - 包含 token, user_id, role, expires_in 的字典
  

**Raises**:

- `BusinessError` - 账号不存在、密码错误、角色类型无效

<a id="app.services.auth_service.AuthService.upload_organizer_proof"></a>

#### upload\_organizer\_proof

```python
@staticmethod
def upload_organizer_proof(file)
```

上传组织者证明图片

用于组织者注册时上传资质证明文件。
此接口无需认证，因为用户尚未注册。

流程：
1. 校验文件是否存在
2. 校验文件格式（仅支持 jpg/png）
3. 校验文件大小（不超过 2MB）
4. 保存文件到临时目录
5. 返回文件访问 URL

**Arguments**:

- `file` - 上传的图片文件（Flask file 对象）
  

**Returns**:

- `dict` - 包含 image_url 的字典
  

**Raises**:

- `BusinessError` - 文件格式错误、大小超限等

<a id="app.services.user_service"></a>

# app.services.user\_service

用户服务模块

提供用户资料管理、头像上传、密码重置、账号注销等功能
以及管理员对用户/组织者/管理员的管理功能

<a id="app.services.user_service.BusinessError"></a>

## BusinessError

<a id="app.services.user_service.User"></a>

## User

<a id="app.services.user_service.Organizer"></a>

## Organizer

<a id="app.services.user_service.Admin"></a>

## Admin

<a id="app.services.user_service.Checkin"></a>

## Checkin

<a id="app.services.user_service.UserService"></a>

## UserService Objects

```python
class UserService()
```

用户服务类

提供用户相关的业务逻辑：
- 用户/组织者/管理员的资料获取和修改
- 头像上传
- 密码重置
- 账号注销
- 管理员管理用户/组织者/管理员

<a id="app.services.user_service.UserService.ACHIEVEMENT_LEVELS"></a>

#### ACHIEVEMENT\_LEVELS

<a id="app.services.user_service.UserService.get_profile"></a>

#### get\_profile

```python
@staticmethod
def get_profile(role, user_id)
```

获取当前用户信息

根据用户角色返回对应的资料信息，普通用户还会计算成就等级

**Arguments**:

- `role` _str_ - 用户角色：user / organizer / admin
- `user_id` _int_ - 用户ID
  

**Returns**:

- `dict` - 用户资料信息，包含角色特定的字段
  

**Raises**:

- `BusinessError` - 用户不存在或角色无效

<a id="app.services.user_service.UserService.update_profile"></a>

#### update\_profile

```python
@staticmethod
def update_profile(role, user_id, data)
```

修改用户信息

支持修改的字段因角色而异：
- 普通用户：username, gender, college, major, grade, phone, avatar
- 组织者/管理员：avatar

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
- `data` _dict_ - 要更新的字段字典
  

**Raises**:

- `BusinessError` - 用户不存在、手机号格式错误等

<a id="app.services.user_service.UserService.update_avatar_url"></a>

#### update\_avatar\_url

```python
@staticmethod
def update_avatar_url(role, user_id, avatar_url)
```

更新头像URL（内部方法）

将上传后的头像文件URL保存到数据库

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
- `avatar_url` _str_ - 头像文件访问URL

<a id="app.services.user_service.UserService.upload_avatar"></a>

#### upload\_avatar

```python
@staticmethod
def upload_avatar(role, user_id, file)
```

上传头像文件

流程：
1. 校验文件格式（jpg/png）
2. 删除旧头像文件（如果存在）
3. 保存新头像文件
4. 更新数据库中的头像URL

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
- `file` - 上传的头像文件
  

**Returns**:

- `str` - 头像文件的访问URL
  

**Raises**:

- `BusinessError` - 文件格式错误

<a id="app.services.user_service.UserService.reset_password"></a>

#### reset\_password

```python
@staticmethod
def reset_password(role, user_id, old_password, new_password)
```

重置密码

需要验证旧密码正确性

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
- `old_password` _str_ - 旧密码
- `new_password` _str_ - 新密码
  

**Raises**:

- `BusinessError` - 账号不存在、旧密码错误

<a id="app.services.user_service.UserService.delete_account"></a>

#### delete\_account

```python
@staticmethod
def delete_account(role, user_id)
```

注销账号

将账号状态设为 deleted，不物理删除数据

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
  

**Raises**:

- `BusinessError` - 账号不存在、超级管理员不可注销

<a id="app.services.user_service.UserService.list_users"></a>

#### list\_users

```python
@staticmethod
def list_users(params)
```

获取用户列表（管理员用）

**Arguments**:

- `params` _dict_ - 查询参数
  - page: 页码（默认1）
  - page_size: 每页数量（默认20，最大100）
  - student_id: 学号筛选（模糊匹配）
  - college: 学院筛选（模糊匹配）
  

**Returns**:

- `dict` - 分页的用户列表

<a id="app.services.user_service.UserService.get_user_detail"></a>

#### get\_user\_detail

```python
@staticmethod
def get_user_detail(user_id)
```

获取单个普通用户详细信息（管理员用）

**Arguments**:

- `user_id` _int_ - 用户ID
  

**Returns**:

- `dict` - 用户详细信息
  

**Raises**:

- `BusinessError` - 用户不存在

<a id="app.services.user_service.UserService.list_organizers"></a>

#### list\_organizers

```python
@staticmethod
def list_organizers(params)
```

获取组织者列表（管理员用）

**Arguments**:

- `params` _dict_ - 查询参数
  - page: 页码（默认1）
  - page_size: 每页数量（默认20，最大100）
  - org_name: 组织名称筛选（模糊匹配）
  - status: 状态筛选
  

**Returns**:

- `dict` - 分页的组织者列表

<a id="app.services.user_service.UserService.get_organizer_detail"></a>

#### get\_organizer\_detail

```python
@staticmethod
def get_organizer_detail(organizer_id)
```

获取单个组织者详细信息（管理员用）

**Arguments**:

- `organizer_id` _int_ - 组织者ID
  

**Returns**:

- `dict` - 组织者详细信息
  

**Raises**:

- `BusinessError` - 组织者不存在

<a id="app.services.user_service.UserService.review_organizer"></a>

#### review\_organizer

```python
@staticmethod
def review_organizer(organizer_id, action, reject_reason)
```

审核组织者（管理员用）

审核结果会通过通知系统发送给组织者

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `action` _str_ - 审核动作：approve-通过，reject-拒绝
- `reject_reason` _str_ - 拒绝原因（action为reject时必填）
  

**Returns**:

- `dict` - 审核结果
  

**Raises**:

- `BusinessError` - 组织者不存在

<a id="app.services.user_service.UserService.create_admin"></a>

#### create\_admin

```python
@staticmethod
def create_admin(current_admin_id, data)
```

创建管理员（需要超级管理员权限）

自动生成6位管理员编号

**Arguments**:

- `current_admin_id` _int_ - 当前操作的管理员ID
- `data` _dict_ - 管理员信息
  - email: 邮箱
  - password: 密码
  - username: 用户名
  - role: 角色（admin/super_admin）
  

**Returns**:

- `dict` - 创建的管理员信息
  

**Raises**:

- `BusinessError` - 权限不足、邮箱已存在、参数无效

<a id="app.services.user_service.UserService.list_admins"></a>

#### list\_admins

```python
@staticmethod
def list_admins()
```

获取管理员列表

**Returns**:

- `list` - 管理员列表

<a id="app.services.user_service.UserService.delete_admin"></a>

#### delete\_admin

```python
@staticmethod
def delete_admin(current_admin_id, admin_id)
```

删除管理员（需要超级管理员权限）

软删除，将状态设为 deleted

**Arguments**:

- `current_admin_id` _int_ - 当前操作的管理员ID
- `admin_id` _int_ - 要删除的管理员ID
  

**Raises**:

- `BusinessError` - 权限不足、管理员不存在、不能删除超级管理员

<a id="app.services.activity_service"></a>

# app.services.activity\_service

活动服务模块

提供活动的完整生命周期管理：
- 活动创建、编辑、删除
- 活动审核（提交审核、审核通过/拒绝）
- 活动查询（列表、详情、我的活动、审核列表）
- 活动状态管理（草稿、审核中、报名中、进行中、已结束、下架）
- 活动修改审核（已有报名时的修改需要二次审核）

<a id="app.services.activity_service.BusinessError"></a>

## BusinessError

<a id="app.services.activity_service.dt"></a>

## dt

<a id="app.services.activity_service.NotificationService"></a>

## NotificationService

<a id="app.services.activity_service.Activity"></a>

## Activity

<a id="app.services.activity_service.ActivityRevision"></a>

## ActivityRevision

<a id="app.services.activity_service.Category"></a>

## Category

<a id="app.services.activity_service.Organizer"></a>

## Organizer

<a id="app.services.activity_service.Registration"></a>

## Registration

<a id="app.services.activity_service.ActivityService"></a>

## ActivityService Objects

```python
class ActivityService()
```

活动服务类

提供活动相关的所有业务逻辑：
- 活动 CRUD 操作
- 活动审核流程
- 活动状态自动计算
- 活动修改的二次审核机制

<a id="app.services.activity_service.ActivityService.ACTIVE_STATUSES"></a>

#### ACTIVE\_STATUSES

<a id="app.services.activity_service.ActivityService.EDITABLE_DIRECT_STATUSES"></a>

#### EDITABLE\_DIRECT\_STATUSES

<a id="app.services.activity_service.ActivityService.create_activity"></a>

#### create\_activity

```python
@staticmethod
def create_activity(organizer_id, data)
```

创建活动（草稿状态）

只有审核通过的组织者才能创建活动

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `data` _dict_ - 活动数据
  

**Returns**:

- `dict` - 包含 activity_id 和 status 的字典
  

**Raises**:

- `BusinessError` - 组织者未审核通过、分类不存在、数据无效

<a id="app.services.activity_service.ActivityService.submit_activity"></a>

#### submit\_activity

```python
@staticmethod
def submit_activity(organizer_id, activity_id)
```

提交活动审核

草稿状态 -> pending（待审核）
已发布状态 -> edit_pending（修改待审核）

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 包含 activity_id 和 status 的字典
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作

<a id="app.services.activity_service.ActivityService.list_activities"></a>

#### list\_activities

```python
@staticmethod
def list_activities(params)
```

获取活动列表（对普通用户可见）

支持筛选：
- 关键词搜索（活动名称）
- 分类筛选（支持一级/二级分类）
- 校区筛选
- 状态筛选
- 日期筛选
- 分页

**Arguments**:

- `params` _dict_ - 查询参数
  - page: 页码
  - page_size: 每页数量
  - keyword: 关键词
  - category_id: 分类ID
  - campus: 校区
  - status: 状态（逗号分隔）
  - start_date: 开始日期
  

**Returns**:

- `dict` - 分页的活动列表

<a id="app.services.activity_service.ActivityService.get_detail"></a>

#### get\_detail

```python
@staticmethod
def get_detail(activity_id, role, user_id)
```

获取活动详情

根据角色返回不同内容：
- 管理员/组织者：edit_pending 状态时显示修改内容
- 普通用户：显示报名状态和签到状态

**Arguments**:

- `activity_id` _int_ - 活动ID
- `role` _str_ - 当前用户角色
- `user_id` _int_ - 当前用户ID
  

**Returns**:

- `dict` - 活动详细信息

<a id="app.services.activity_service.ActivityService.update_activity"></a>

#### update\_activity

```python
@staticmethod
def update_activity(organizer_id, activity_id, data)
```

更新活动

根据活动状态决定更新方式：
- 草稿/待审核/已拒绝：直接更新
- 已发布状态：创建修改记录，进入二次审核

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
- `data` _dict_ - 更新数据
  

**Returns**:

- `dict` - 包含 activity_id 和 status 的字典
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作、时间冲突等

<a id="app.services.activity_service.ActivityService.delete_activity"></a>

#### delete\_activity

```python
@staticmethod
def delete_activity(organizer_id, activity_id)
```

删除活动（组织者）

彻底删除活动及其所有相关数据（报名、签到、签到码、修改记录）
删除前会发送通知给所有已报名用户和组织者

限制：
- 活动已开始不可删除
- 活动开始前1小时内不可删除

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作、不可删除

<a id="app.services.activity_service.ActivityService.get_my_activities"></a>

#### get\_my\_activities

```python
@staticmethod
def get_my_activities(organizer_id, params)
```

获取我发布的活动（组织者用）

支持筛选：关键词、分类、校区、状态、日期

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `params` _dict_ - 查询参数
  

**Returns**:

- `dict` - 分页的活动列表

<a id="app.services.activity_service.ActivityService.list_review_activities"></a>

#### list\_review\_activities

```python
@staticmethod
def list_review_activities(params)
```

获取审核活动列表（管理员用）

默认显示 pending 和 edit_pending 状态的活动

**Arguments**:

- `params` _dict_ - 查询参数
  - page: 页码
  - page_size: 每页数量
  - status: 状态筛选
  - keyword: 关键词
  - organizer_id: 组织者ID筛选
  - category_id: 分类ID筛选
  - start_date: 开始日期
  

**Returns**:

- `dict` - 分页的审核活动列表

<a id="app.services.activity_service.ActivityService.review_activity"></a>

#### review\_activity

```python
@staticmethod
def review_activity(activity_id, action, reject_reason)
```

审核活动（管理员用）

审核流程：
- approve: 审核通过，活动状态变为 open 或 ongoing（根据时间）
- reject: 审核拒绝，活动状态变为 rejected

会发送通知给组织者
如果是 edit_pending 状态通过，还会通知已报名用户活动已变更

**Arguments**:

- `activity_id` _int_ - 活动ID
- `action` _str_ - 审核动作：approve/reject
- `reject_reason` _str_ - 拒绝原因（action为reject时必填）
  

**Returns**:

- `dict` - 包含 activity_id 和 new_status 的字典
  

**Raises**:

- `BusinessError` - 活动不存在、状态不可审核

<a id="app.services.activity_service.ActivityService.remove_activity"></a>

#### remove\_activity

```python
@staticmethod
def remove_activity(activity_id, reason)
```

下架活动（管理员用）

将活动状态改为 removed，删除所有报名和签到数据
会发送通知给组织者和所有已报名用户

限制：活动开始后不可下架

**Arguments**:

- `activity_id` _int_ - 活动ID
- `reason` _str_ - 下架原因
  

**Raises**:

- `BusinessError` - 活动不存在、活动已开始

<a id="app.services.registration_service"></a>

# app.services.registration\_service

报名服务模块

提供活动报名相关的完整功能：
- 报名活动（名额控制、重复报名检查、被拒绝后的冷却时间）
- 取消报名（延迟释放名额机制）
- 我的报名列表
- 活动报名人员列表（组织者视角）
- 拒绝报名（支持累计拒绝次数，两次后禁止报名）
- 报名数据统计

<a id="app.services.registration_service.BusinessError"></a>

## BusinessError

<a id="app.services.registration_service.dt"></a>

## dt

<a id="app.services.registration_service.NotificationService"></a>

## NotificationService

<a id="app.services.registration_service.Activity"></a>

## Activity

<a id="app.services.registration_service.Registration"></a>

## Registration

<a id="app.services.registration_service.User"></a>

## User

<a id="app.services.registration_service.Checkin"></a>

## Checkin

<a id="app.services.registration_service.RegistrationService"></a>

## RegistrationService Objects

```python
class RegistrationService()
```

报名服务类

提供活动报名相关的业务逻辑：
- 报名/取消报名
- 名额管理（延迟释放机制）
- 拒绝报名（累计次数，两次禁止）
- 报名数据统计

<a id="app.services.registration_service.RegistrationService.ACTIVE_STATUSES"></a>

#### ACTIVE\_STATUSES

<a id="app.services.registration_service.RegistrationService.register"></a>

#### register

```python
@staticmethod
def register(user_id, activity_id)
```

报名活动

流程：
1. 验证活动状态和报名截止时间
2. 检查是否还有剩余名额
3. 检查用户报名状态：
- 已报名：拒绝重复报名
- 被拒绝两次：禁止再次报名
- 被拒绝一次：检查10分钟冷却期
- 已取消：重新激活报名
- 新用户：创建报名记录
4. 发送报名成功通知

**Arguments**:

- `user_id` _int_ - 用户ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 包含 registration_id, status, remaining_slots
  

**Raises**:

- `BusinessError` - 活动不存在、不可报名、名额已满、重复报名等

<a id="app.services.registration_service.RegistrationService.cancel"></a>

#### cancel

```python
@staticmethod
def cancel(user_id, activity_id)
```

取消报名

取消后名额不会立即释放，而是有2分钟延迟释放

流程：
1. 验证活动是否存在
2. 验证取消截止时间
3. 验证用户是否已报名
4. 设置状态为 cancelled，设置延迟释放时间
5. 发送取消通知

**Arguments**:

- `user_id` _int_ - 用户ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 包含 release_time 的字典
  

**Raises**:

- `BusinessError` - 活动不存在、取消已截止、尚未报名

<a id="app.services.registration_service.RegistrationService.get_my_registrations"></a>

#### get\_my\_registrations

```python
@staticmethod
def get_my_registrations(user_id, params)
```

获取我的报名列表

只显示有效报名（registered/re_registered）
支持筛选：活动名称、活动ID、分类、开始日期、校区

**Arguments**:

- `user_id` _int_ - 用户ID
- `params` _dict_ - 查询参数
  - page: 页码
  - page_size: 每页数量
  - name: 活动名称（模糊匹配）
  - activity_id: 活动ID
  - category_id: 分类ID
  - start_date: 开始日期
  - campus: 校区
  

**Returns**:

- `dict` - 分页的报名列表，包含签到状态

<a id="app.services.registration_service.RegistrationService.get_activity_registrations"></a>

#### get\_activity\_registrations

```python
@staticmethod
def get_activity_registrations(organizer_id, activity_id, params)
```

获取活动报名人员列表（组织者视角）

返回报名人员信息、签到情况、统计数据

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
- `params` _dict_ - 查询参数
  - page: 页码
  - page_size: 每页数量
  - gender: 性别筛选
  - college: 学院筛选
  - grade: 年级筛选
  - major: 专业筛选
  

**Returns**:

- `dict` - 分页的报名人员列表和统计数据

<a id="app.services.registration_service.RegistrationService.reject_registration"></a>

#### reject\_registration

```python
@staticmethod
def reject_registration(organizer_id, registration_id, reason)
```

拒绝报名（组织者）

拒绝逻辑：
- 第1次拒绝：状态变为 rejected
- 第2次拒绝：状态变为 blocked（永久禁止报名）
- 每次拒绝增加 reject_count

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `registration_id` _int_ - 报名记录ID
- `reason` _str_ - 拒绝原因
  

**Returns**:

- `dict` - 包含 new_status 和 reject_count
  

**Raises**:

- `BusinessError` - 报名记录不存在、无权操作、没有有效报名

<a id="app.services.registration_service.RegistrationService.get_registration_stats"></a>

#### get\_registration\_stats

```python
@staticmethod
def get_registration_stats(organizer_id, activity_id)
```

获取活动数据统计（组织者）

返回报名人数统计、签到人数、按性别/学院/年级/专业分布

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 统计数据

<a id="app.services.checkin_service"></a>

# app.services.checkin\_service

签到服务模块

提供活动签到相关的完整功能：
- 签到码生成（组织者）
- 扫码签到（普通用户）
- 手动签到（组织者）
- 签到记录查询
- 签到统计

<a id="app.services.checkin_service.BusinessError"></a>

## BusinessError

<a id="app.services.checkin_service.dt"></a>

## dt

<a id="app.services.checkin_service.NotificationService"></a>

## NotificationService

<a id="app.services.checkin_service.Activity"></a>

## Activity

<a id="app.services.checkin_service.ActivityCheckinCode"></a>

## ActivityCheckinCode

<a id="app.services.checkin_service.Registration"></a>

## Registration

<a id="app.services.checkin_service.Checkin"></a>

## Checkin

<a id="app.services.checkin_service.User"></a>

## User

<a id="app.services.checkin_service.CheckinService"></a>

## CheckinService Objects

```python
class CheckinService()
```

签到服务类

提供活动签到相关的业务逻辑：
- 签到码生成与管理
- 扫码签到（用户自助）
- 手动签到（组织者辅助）
- 签到数据统计

<a id="app.services.checkin_service.CheckinService.ACTIVE_STATUSES"></a>

#### ACTIVE\_STATUSES

<a id="app.services.checkin_service.CheckinService.get_checkin_code"></a>

#### get\_checkin\_code

```python
@staticmethod
def get_checkin_code(organizer_id, activity_id)
```

获取签到码（组织者）

如果活动没有签到码，会自动生成一个

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 包含 checkin_code 的字典
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作

<a id="app.services.checkin_service.CheckinService.checkin"></a>

#### checkin

```python
@staticmethod
def checkin(user_id, activity_id, checkin_code)
```

签到码签到（普通用户）

用户通过输入签到码自助签到

流程：
1. 验证活动存在
2. 验证签到码正确
3. 验证签到时间窗口（开始前30分钟到结束后）
4. 验证用户已报名
5. 验证未重复签到
6. 创建签到记录
7. 发送签到成功通知

**Arguments**:

- `user_id` _int_ - 用户ID
- `activity_id` _int_ - 活动ID
- `checkin_code` _str_ - 签到码
  

**Returns**:

- `dict` - 包含 checkin_id 和 checkin_time
  

**Raises**:

- `BusinessError` - 活动不存在、签到码错误、时间窗口无效、未报名、重复签到

<a id="app.services.checkin_service.CheckinService.manual_checkin"></a>

#### manual\_checkin

```python
@staticmethod
def manual_checkin(organizer_id, activity_id, student_id)
```

手动签到（组织者）

组织者通过学号帮助用户完成签到

流程：
1. 验证活动存在且有权限
2. 验证用户存在
3. 验证用户已报名
4. 验证未重复签到
5. 创建手动签到记录
6. 发送签到成功通知

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
- `student_id` _str_ - 用户学号
  

**Returns**:

- `dict` - 包含 user_id 和 checkin_time
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作、用户不存在、未报名、重复签到

<a id="app.services.checkin_service.CheckinService.get_my_checkins"></a>

#### get\_my\_checkins

```python
@staticmethod
def get_my_checkins(user_id, params)
```

获取我的签到记录

返回用户的历史签到记录，按签到时间倒序

**Arguments**:

- `user_id` _int_ - 用户ID
- `params` _dict_ - 查询参数
  - page: 页码（默认1）
  - page_size: 每页数量（默认20，最大100）
  

**Returns**:

- `dict` - 分页的签到记录列表

<a id="app.services.checkin_service.CheckinService.get_checkin_stats"></a>

#### get\_checkin\_stats

```python
@staticmethod
def get_checkin_stats(organizer_id, activity_id)
```

获取活动签到情况（组织者）

返回签到统计数据和详细列表：
- 总报名人数
- 已签到人数
- 未签到人数
- 签到率
- 已签到用户列表（含签到时间、方式）
- 未签到用户列表（含报名时间）

**Arguments**:

- `organizer_id` _int_ - 组织者ID
- `activity_id` _int_ - 活动ID
  

**Returns**:

- `dict` - 签到统计信息
  

**Raises**:

- `BusinessError` - 活动不存在、无权操作

<a id="app.services.notification_service"></a>

# app.services.notification\_service

通知服务模块

提供系统通知和公告的管理功能：
- 通知创建、列表查询、已读标记
- 公告创建、列表查询、删除
- 支持管理员和普通用户不同视角

<a id="app.services.notification_service.BusinessError"></a>

## BusinessError

<a id="app.services.notification_service.dt"></a>

## dt

<a id="app.services.notification_service.Notification"></a>

## Notification

<a id="app.services.notification_service.Announcement"></a>

## Announcement

<a id="app.services.notification_service.NotificationService"></a>

## NotificationService Objects

```python
class NotificationService()
```

通知服务类

提供系统通知和公告的业务逻辑：
- 创建通知（供其他服务调用）
- 获取通知列表（支持分页和未读筛选）
- 标记通知已读
- 发布系统公告
- 获取公告列表（区分管理员/普通用户）
- 删除公告

<a id="app.services.notification_service.NotificationService.create_notification"></a>

#### create\_notification

```python
@staticmethod
def create_notification(session, receiver_type, receiver_id, title, content,
                        type_, related_id)
```

创建通知（内部方法）

供其他服务模块调用，如：
- 活动审核结果通知
- 报名结果通知
- 活动变更通知
- 活动提醒通知

**Arguments**:

- `session` - 数据库会话
- `receiver_type` _str_ - 接收者类型：user / organizer
- `receiver_id` _int_ - 接收者ID
- `title` _str_ - 通知标题
- `content` _str_ - 通知内容
- `type_` _str_ - 通知类型
  - registration_result: 报名结果
  - activity_audit_result: 活动审核结果
  - activity_change: 活动变更
  - violation_result: 违规处理
  - activity_reminder: 活动提醒
  - organizer_audit_result: 组织者审核结果
- `related_id` _int_ - 关联业务ID（活动ID、报名ID等）
  

**Returns**:

- `Notification` - 创建的通知对象

<a id="app.services.notification_service.NotificationService.list_notifications"></a>

#### list\_notifications

```python
@staticmethod
def list_notifications(role, user_id, params)
```

获取我的通知列表

支持分页和未读筛选

**Arguments**:

- `role` _str_ - 用户角色：user / organizer
- `user_id` _int_ - 用户ID
- `params` _dict_ - 查询参数
  - page: 页码（默认1）
  - page_size: 每页数量（默认20，最大100）
  - unread: 是否只显示未读（1/true/True）
  

**Returns**:

- `dict` - 分页的通知列表，包含未读数量

<a id="app.services.notification_service.NotificationService.mark_notification_read"></a>

#### mark\_notification\_read

```python
@staticmethod
def mark_notification_read(role, user_id, notification_id)
```

标记通知已读

**Arguments**:

- `role` _str_ - 用户角色
- `user_id` _int_ - 用户ID
- `notification_id` _int_ - 通知ID
  

**Raises**:

- `BusinessError` - 通知不存在或不属于当前用户

<a id="app.services.notification_service.NotificationService.create_announcement"></a>

#### create\_announcement

```python
@staticmethod
def create_announcement(admin_id, title, content, start_time, end_time)
```

发布系统公告（管理员）

公告会在 start_time 到 end_time 期间对外展示

**Arguments**:

- `admin_id` _int_ - 发布管理员ID
- `title` _str_ - 公告标题（不超过50字符）
- `content` _str_ - 公告正文
- `start_time` _str_ - 生效时间（格式：%Y-%m-%d %H:%M:%S）
- `end_time` _str_ - 失效时间（格式：%Y-%m-%d %H:%M:%S）
  

**Returns**:

- `dict` - 包含 announcement_id 的字典
  

**Raises**:

- `BusinessError` - 标题/内容为空、标题过长、时间无效

<a id="app.services.notification_service.NotificationService.list_announcements"></a>

#### list\_announcements

```python
@staticmethod
def list_announcements()
```

获取所有系统公告（管理员用）

不过滤有效期，返回所有公告（按创建时间倒序）

**Returns**:

- `list` - 公告列表

<a id="app.services.notification_service.NotificationService.list_valid_announcements"></a>

#### list\_valid\_announcements

```python
@staticmethod
def list_valid_announcements()
```

获取有效期内的系统公告（普通用户用）

只返回当前时间在 start_time 和 end_time 之间的公告

**Returns**:

- `list` - 有效期内的公告列表

<a id="app.services.notification_service.NotificationService.delete_announcement"></a>

#### delete\_announcement

```python
@staticmethod
def delete_announcement(announcement_id)
```

删除公告（管理员）

**Arguments**:

- `announcement_id` _int_ - 公告ID
  

**Raises**:

- `BusinessError` - 公告不存在

<a id="app.services.category_service"></a>

# app.services.category\_service

分类服务模块

提供活动分类的树形结构管理功能

<a id="app.services.category_service.Category"></a>

## Category

<a id="app.services.category_service.CategoryService"></a>

## CategoryService Objects

```python
class CategoryService()
```

分类服务类

提供活动分类相关的业务逻辑：
- 获取分类树形结构（用于前端展示）
- 支持多级分类（目前支持两级）

<a id="app.services.category_service.CategoryService.get_category_tree"></a>

#### get\_category\_tree

```python
@staticmethod
def get_category_tree()
```

获取分类树形结构

将数据库中扁平存储的分类数据转换为树形结构，
便于前端渲染级联选择器或树形菜单。

分类结构示例：
- 学术类 (id:1, level:1)
- 讲座 (id:101, parent_id:1, level:2)
- 竞赛 (id:102, parent_id:1, level:2)
- 沙龙 (id:103, parent_id:1, level:2)
- 文体类 (id:2, level:1)
- 运动会 (id:201, parent_id:2, level:2)
- ...

构建逻辑：
1. 查询所有分类，按 sort_order 排序
2. 创建分类ID到节点的映射
3. 遍历所有分类：
- 如果 parent_id == 0，添加到根节点列表
- 否则，找到父节点并添加到其 children 数组

**Returns**:

- `list` - 树形结构的分类列表，每个节点包含：
  - id: 分类ID
  - name: 分类名称
  - level: 层级（1-一级，2-二级）
  - sort_order: 排序序号
  - children: 子分类列表

<a id="app.services.stats_service"></a>

# app.services.stats\_service

统计服务模块

提供平台级别的数据统计功能：
- 平台整体数据统计（管理员用）
- 用户活跃度排行榜

<a id="app.services.stats_service.BusinessError"></a>

## BusinessError

<a id="app.services.stats_service.Activity"></a>

## Activity

<a id="app.services.stats_service.User"></a>

## User

<a id="app.services.stats_service.Organizer"></a>

## Organizer

<a id="app.services.stats_service.Admin"></a>

## Admin

<a id="app.services.stats_service.Registration"></a>

## Registration

<a id="app.services.stats_service.Checkin"></a>

## Checkin

<a id="app.services.stats_service.Category"></a>

## Category

<a id="app.services.stats_service.StatsService"></a>

## StatsService Objects

```python
class StatsService()
```

统计服务类

提供平台数据统计和排行榜功能：
- 活动统计（按状态、按分类）
- 用户统计（学生、组织者、管理员）
- 参与统计（报名数、签到数、签到率）
- 用户活跃度排行榜

<a id="app.services.stats_service.StatsService.ACTIVE_STATUSES"></a>

#### ACTIVE\_STATUSES

<a id="app.services.stats_service.StatsService.PLATFORM_ACTIVITY_STATUSES"></a>

#### PLATFORM\_ACTIVITY\_STATUSES

<a id="app.services.stats_service.StatsService.get_platform_stats"></a>

#### get\_platform\_stats

```python
@staticmethod
def get_platform_stats()
```

获取平台数据统计（管理员）

统计内容包括：
1. 活动统计：
- 活动总数
- 按状态的分布（待审核、报名中、进行中等）
- 按分类的分布
2. 用户统计：
- 学生总数
- 组织者总数
- 管理员总数
3. 参与统计：
- 总报名次数
- 总签到次数
- 平均签到率

**Returns**:

- `dict` - 平台统计数据

<a id="app.services.stats_service.StatsService.get_leaderboard"></a>

#### get\_leaderboard

```python
@staticmethod
def get_leaderboard(params)
```

获取用户活跃度排行

根据用户的报名次数和签到次数进行排名
支持按周期（周/月/全部）、学院、年级筛选

排名规则：
- 主要按签到次数降序
- 签到次数相同按报名次数降序
- 报名次数相同按用户ID升序

**Arguments**:

- `params` _dict_ - 查询参数
  - period: 统计周期（week/month/all，默认all）
  - college: 学院筛选（可选）
  - grade: 年级筛选（可选）
  - page: 页码（默认1）
  - page_size: 每页数量（默认20，最大100）
  

**Returns**:

- `dict` - 分页的排行榜列表，每条包含排名、用户信息、报名次数、签到次数

<a id="app.task.scheduler"></a>

# app.task.scheduler

定时任务调度模块

提供后台定时任务功能：
- 自动更新活动状态（根据时间）
- 发送活动开始提醒通知

使用 APScheduler 作为调度框架

<a id="app.task.scheduler.BackgroundScheduler"></a>

## BackgroundScheduler

<a id="app.task.scheduler.IntervalTrigger"></a>

## IntervalTrigger

<a id="app.task.scheduler.Activity"></a>

## Activity

<a id="app.task.scheduler.Registration"></a>

## Registration

<a id="app.task.scheduler.NotificationService"></a>

## NotificationService

<a id="app.task.scheduler.update_activity_statuses"></a>

#### update\_activity\_statuses

```python
def update_activity_statuses()
```

更新活动状态（根据时间）

根据当前时间自动更新活动状态：
- open/edit_pending → ongoing（到达开始时间）
- ongoing → ended（到达结束时间）

执行频率：每 5 分钟

edit_pending 状态同理（活动修改审核中但时间到了）

<a id="app.task.scheduler.send_activity_reminders"></a>

#### send\_activity\_reminders

```python
def send_activity_reminders()
```

发送活动开始前1小时提醒

查找即将开始的活动（1小时后开始），给已报名用户发送提醒通知

执行频率：每 10 分钟

防重复机制：
- 检查是否已发送过提醒（通过 Notification 表）
- 每个活动只发送一次提醒

<a id="app.task.scheduler.start_scheduler"></a>

#### start\_scheduler

```python
def start_scheduler()
```

启动定时任务调度器

在应用启动时调用（在 create_app 中执行）

注册的任务：
1. update_activity_statuses - 每 5 分钟执行
2. send_activity_reminders - 每 10 分钟执行

调度器配置：
- 使用 BackgroundScheduler（后台线程）
- 使用 IntervalTrigger（间隔触发）

<a id="app.task.scheduler.stop_scheduler"></a>

#### stop\_scheduler

```python
def stop_scheduler()
```

停止定时任务调度器

在应用关闭时调用，优雅地停止所有后台任务

<a id="app.common.auth"></a>

# app.common.auth

JWT 认证模块

提供 JSON Web Token (JWT) 的创建和解析功能
用于用户身份认证和授权

<a id="app.common.auth.create_token"></a>

#### create\_token

```python
def create_token(role, user_id)
```

创建 JWT Token

生成包含用户身份信息的加密 Token，用于后续请求的身份验证

Token 载荷 (Payload) 包含：
- role: 用户角色（user/organizer/admin）
- user_id: 用户ID
- exp: Token 过期时间（当前时间 + 2小时）

**Arguments**:

- `role` _str_ - 用户角色
  - user: 普通用户
  - organizer: 组织者
  - admin: 管理员
- `user_id` _int_ - 用户ID
  

**Returns**:

- `str` - JWT Token 字符串
  

**Example**:

  >>> token = create_token('user', 123)
  >>> print(token)
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

<a id="app.common.auth.decode_token"></a>

#### decode\_token

```python
def decode_token(token)
```

解析 JWT Token

验证 Token 有效性并解析其中的用户信息

流程：
1. 使用密钥解密 Token
2. 验证签名是否正确
3. 检查是否过期

**Arguments**:

- `token` _str_ - JWT Token 字符串
  

**Returns**:

  dict or None: 解析成功返回 payload 字典，失败返回 None
  - role: 用户角色
  - user_id: 用户ID
  - exp: 过期时间戳
  

**Example**:

  >>> payload = decode_token(token)
  >>> if payload:
  ...     print(f"用户 {payload['user_id']} 角色: {payload['role']}")
  

**Notes**:

  - ExpiredSignatureError: Token 已过期
  - InvalidTokenError: Token 无效（签名错误、格式错误等）

<a id="app.common.database"></a>

# app.common.database

数据库会话管理模块

提供数据库连接和会话管理功能：
- 数据库引擎创建
- 会话工厂配置
- 上下文管理器风格的会话管理

<a id="app.common.database.contextmanager"></a>

## contextmanager

<a id="app.common.database.create_engine"></a>

## create\_engine

<a id="app.common.database.sessionmaker"></a>

## sessionmaker

<a id="app.common.database.scoped_session"></a>

## scoped\_session

<a id="app.common.database.get_config"></a>

## get\_config

<a id="app.common.database.config"></a>

#### config

<a id="app.common.errors"></a>

# app.common.errors

错误处理模块

提供自定义业务异常类和全局错误处理器：
- BusinessError: 业务异常类
- 全局错误处理：404、500 等 HTTP 异常

<a id="app.common.errors.BusinessError"></a>

## BusinessError Objects

```python
class BusinessError(Exception)
```

业务异常类

用于在业务逻辑层抛出可预期的业务错误
与系统异常（如数据库连接失败）区分开

**Attributes**:

- `message` _str_ - 错误消息，返回给前端
- `code` _int_ - 业务错误码
- `status_code` _int_ - HTTP 状态码
  
  错误码说明:
  - 200: 成功（不用于错误）
  - 400: 参数错误、业务逻辑错误
  - 401: 未登录、token 失效
  - 403: 权限不足
  - 404: 资源不存在
  - 500: 服务器内部错误

<a id="app.common.errors.BusinessError.to_response"></a>

#### to\_response

```python
def to_response()
```

将异常转换为 HTTP 响应

返回统一格式的错误响应

**Returns**:

- `tuple` - (response, status_code)
  - response: JSON 格式的错误响应
  - status_code: HTTP 状态码

<a id="app.common.errors.register_error_handlers"></a>

#### register\_error\_handlers

```python
def register_error_handlers(app)
```

注册全局错误处理

为 Flask 应用注册统一的错误处理器，确保所有错误返回一致的格式

**Arguments**:

- `app` - Flask 应用实例
  
  处理的错误类型:
  1. BusinessError - 自定义业务异常
  2. 404 - 路由未找到
  3. 500 - 服务器内部错误

<a id="app.common.response"></a>

# app.common.response

统一响应模块

提供统一的 API 成功响应格式
确保所有成功响应返回一致的数据结构

<a id="app.common.response.success"></a>

#### success

```python
def success(data=None, message='success', code=200)
```

统一成功响应

生成标准格式的成功响应，包含状态码、消息和数据

**Arguments**:

- `data` - 响应数据，可以是 dict、list、str 等任意类型，默认为 None
- `message` _str_ - 响应消息，默认为 'success'
- `code` _int_ - 业务状态码，默认为 200
  

**Returns**:

- `tuple` - (response, status_code)
  - response: JSON 格式的响应体
  - status_code: HTTP 状态码
  

**Notes**:

  此函数用于成功响应，错误响应请使用 BusinessError

<a id="app.common.serializers"></a>

# app.common.serializers

序列化工具模块

提供数据格式转换和序列化函数：
- datetime 对象格式化为 ISO 8601 格式

<a id="app.common.serializers.timezone"></a>

## timezone

<a id="app.common.serializers.dt"></a>

#### dt

```python
def dt(value)
```

格式化日期时间为 ISO 8601 格式（UTC）

将 datetime 对象转换为前端友好的标准格式
主要用于 API 响应中的时间字段序列化

**Arguments**:

- `value` - 待格式化的值，通常为 datetime 对象或 None
  

**Returns**:

  str | None:
  - 如果是 datetime 对象：返回 ISO 8601 格式的字符串
  - 如果是 None：返回 None
  - 其他类型：返回 str(value)
  
  格式说明:
  - 输出格式: "YYYY-MM-DDTHH:MM:SSZ"
  - 示例: "2026-05-31T10:42:44Z"
  - 末尾的 'Z' 表示 UTC 时区
  

**Notes**:

  该函数确保所有时间输出为 UTC 时区
  前端可以直接使用 new Date() 解析

<a id="app.api.deps"></a>

# app.api.deps

API 依赖模块

提供 API 层通用的依赖注入和工具函数：
- JSON 数据获取与验证
- JWT Token 解析获取当前用户
- 登录验证装饰器
- 角色权限验证装饰器

<a id="app.api.deps.wraps"></a>

## wraps

<a id="app.api.deps.decode_token"></a>

## decode\_token

<a id="app.api.deps.BusinessError"></a>

## BusinessError

<a id="app.api.deps.get_json_data"></a>

#### get\_json\_data

```python
def get_json_data()
```

获取并验证请求 JSON 数据

从 Flask request 对象中提取 JSON 数据
如果请求体为空或不是 JSON 格式，抛出异常

**Returns**:

- `dict` - 解析后的 JSON 数据
  

**Raises**:

- `BusinessError` - 请求体为空或不是有效 JSON

<a id="app.api.deps.get_current_user"></a>

#### get\_current\_user

```python
def get_current_user()
```

从 Authorization Header 解析 Token，获取当前用户信息

从请求头中提取 Bearer Token，解密后获取用户角色和ID

**Returns**:

- `tuple` - (role, user_id)
  - role: 用户角色（user/organizer/admin），解析失败时返回 None
  - user_id: 用户ID，解析失败时返回 None

<a id="app.api.deps.require_auth"></a>

#### require\_auth

```python
def require_auth()
```

要求登录的装饰器

验证请求是否携带有效的 JWT Token
验证通过后，将用户信息存入 Flask 的 g 对象中

**Raises**:

- `BusinessError` - 未登录或 Token 无效/过期（401）
  
  g 对象注入:
  - g.current_role: 当前用户角色
  - g.current_user_id: 当前用户ID

<a id="app.api.deps.require_role"></a>

#### require\_role

```python
def require_role(*allowed_roles)
```

要求特定角色的装饰器

验证当前登录用户是否拥有指定角色之一
必须在 @require_auth() 之后使用

**Arguments**:

- `*allowed_roles` - 允许的角色列表
  - 'user': 普通用户
  - 'organizer': 组织者
  - 'admin': 管理员
  

**Raises**:

- `BusinessError` - 未登录（401）或权限不足（403）

<a id="app.api.auth"></a>

# app.api.auth

认证 API 路由模块

提供用户认证相关的 API 接口：
- 普通用户注册
- 组织者注册
- 用户登录（支持三种角色）
- 用户退出
- 组织者证明图片上传

<a id="app.api.auth.get_json_data"></a>

## get\_json\_data

<a id="app.api.auth.success"></a>

## success

<a id="app.api.auth.BusinessError"></a>

## BusinessError

<a id="app.api.auth.AuthService"></a>

## AuthService

<a id="app.api.auth.bp"></a>

#### bp

<a id="app.api.auth.register_user"></a>

#### register\_user

```python
@bp.post('/register/user')
def register_user()
```

普通用户注册

学生使用学号、邮箱等信息注册普通用户账号

Request Body:
- student_id (str): 学号（10位数字）
- email (str): 邮箱地址
- username (str): 用户名/昵称
- password (str): 密码
- confirm_password (str): 确认密码
- gender (str): 性别（男/女）
- college (str): 学院
- major (str): 专业
- grade (str): 年级
- phone (str, optional): 手机号

**Returns**:

  - userId: 用户ID
  - user_id: 用户ID（兼容字段）
  - role: 角色（user）
  - token: JWT Token
  

**Raises**:

- `400` - 参数错误、学号格式错误、学号/邮箱已存在

<a id="app.api.auth.register_organizer"></a>

#### register\_organizer

```python
@bp.post('/register/organizer')
def register_organizer()
```

组织者注册

社团或组织使用邮箱注册组织者账号，需提供组织证明
注册后状态为 pending（待审核），需管理员审核通过后才能发布活动

Request Body:
- email (str): 邮箱地址（登录凭证）
- org_name (str): 组织名称
- password (str): 密码
- confirm_password (str): 确认密码
- org_proof_text (str): 组织证明文本
- org_proof_image (str, optional): 组织证明图片URL

**Returns**:

  - userId: 组织者ID
  - organizer_id: 组织者ID
  - role: 角色（organizer）
  - token: JWT Token
  

**Raises**:

- `400` - 参数错误、密码不一致、邮箱已注册

<a id="app.api.auth.login"></a>

#### login

```python
@bp.post('/login')
def login()
```

用户登录

支持三种角色登录：
- 普通用户：使用学号或邮箱登录
- 组织者：使用邮箱登录
- 管理员：使用管理员编号登录

Request Body:
- role (str): 角色类型（user/organizer/admin）
- account (str): 账号
- user: 学号或邮箱
- organizer: 邮箱
- admin: 管理员编号
- password (str): 密码

**Returns**:

  - token: JWT Token
  - user_id: 用户ID
  - role: 用户角色
  - expires_in: Token 有效期（秒，7200秒=2小时）
  

**Raises**:

- `401` - 账号不存在或密码错误
- `400` - 缺少必填字段

<a id="app.api.auth.logout"></a>

#### logout

```python
@bp.post('/logout')
def logout()
```

用户退出登录

客户端清除本地存储的 Token 即可，
服务端无状态，不需要额外处理

**Returns**:

- `message` - 退出成功

<a id="app.api.auth.upload_organizer_proof"></a>

#### upload\_organizer\_proof

```python
@bp.post('/upload-organizer-proof')
def upload_organizer_proof()
```

上传组织者证明图片

用于组织者注册时上传资质证明文件
此接口无需认证，因为用户尚未注册

Request:
- proof_image (file): 图片文件（支持 jpg/png，最大2MB）

**Returns**:

  - image_url: 图片访问URL
  

**Raises**:

- `400` - 未上传文件、文件格式错误、文件大小超限

<a id="app.api.user"></a>

# app.api.user

用户 API 路由模块

提供用户资料管理相关的 API 接口：
- 获取当前用户信息
- 修改用户信息
- 修改头像
- 修改密码
- 注销账号

支持三种角色：普通用户、组织者、管理员

<a id="app.api.user.get_json_data"></a>

## get\_json\_data

<a id="app.api.user.require_auth"></a>

## require\_auth

<a id="app.api.user.get_current_user"></a>

## get\_current\_user

<a id="app.api.user.success"></a>

## success

<a id="app.api.user.BusinessError"></a>

## BusinessError

<a id="app.api.user.UserService"></a>

## UserService

<a id="app.api.user.bp"></a>

#### bp

<a id="app.api.user.get_profile"></a>

#### get\_profile

```python
@bp.get('/profile')
@require_auth()
def get_profile()
```

获取当前用户信息

根据当前登录用户的角色返回不同的信息：
- 普通用户：返回用户基本信息 + 成就等级
- 组织者：返回组织信息 + 审核状态
- 管理员：返回管理员信息 + 角色权限

**Returns**:

- `dict` - 用户资料信息

<a id="app.api.user.update_profile"></a>

#### update\_profile

```python
@bp.put('/profile')
@require_auth()
def update_profile()
```

修改用户信息

支持修改的字段因角色而异：
- 普通用户：username, gender, college, major, grade, phone, avatar
- 组织者/管理员：仅支持 avatar

Request Body:
- username (str, optional): 用户名
- gender (str, optional): 性别
- college (str, optional): 学院
- major (str, optional): 专业
- grade (str, optional): 年级
- phone (str, optional): 手机号（需校验格式）
- avatar (str, optional): 头像URL

**Returns**:

- `message` - 更新成功
  

**Raises**:

- `400` - 手机号格式错误
- `404` - 用户不存在

<a id="app.api.user.update_avatar"></a>

#### update\_avatar

```python
@bp.post('/avatar')
@require_auth()
def update_avatar()
```

修改头像

支持两种方式：
1. 文件上传（multipart/form-data）：直接上传图片文件
2. URL 方式（application/json）：提供图片URL

图片上传限制：
- 格式：jpg/png
- 大小：不超过2MB

Request (文件上传):
- avatar (file): 头像图片文件

Request (URL方式):
{
"avatar": "https://example.com/avatar.jpg"
}

**Returns**:

  - avatar_url: 头像URL
  

**Raises**:

- `400` - 未上传文件、文件格式错误、文件大小超限

<a id="app.api.user.reset_password"></a>

#### reset\_password

```python
@bp.post('/reset-password')
@require_auth()
def reset_password()
```

修改密码

需要验证旧密码的正确性

Request Body:
- old_password (str): 旧密码
- new_password (str): 新密码
- confirm_password (str): 确认密码

**Returns**:

- `message` - 密码重置成功
  

**Raises**:

- `400` - 旧密码为空、新密码为空、两次密码不一致、旧密码错误
- `404` - 账号不存在

<a id="app.api.user.delete_account"></a>

#### delete\_account

```python
@bp.delete('/account')
@require_auth()
def delete_account()
```

注销账号

软删除：仅将账号状态标记为 deleted，不物理删除数据

限制：
- 超级管理员账号不可注销
- 注销后账号无法登录，但历史数据保留

Request Body:
- confirm (bool): 确认注销标志

**Returns**:

- `message` - 账号已注销
  

**Raises**:

- `400` - 未确认注销、超级管理员不可注销
- `404` - 账号不存在

<a id="app.api.admin_users"></a>

# app.api.admin\_users

管理员用户管理 API 路由模块

提供管理员对用户、组织者、管理员的管理功能：
- 用户管理（列表查询、详情查看）
- 组织者管理（列表查询、详情查看、审核）
- 管理员管理（创建、列表查询、删除）

权限说明：
- 普通管理员：可查看用户和组织者信息
- 超级管理员：可创建和删除管理员

<a id="app.api.admin_users.get_json_data"></a>

## get\_json\_data

<a id="app.api.admin_users.require_auth"></a>

## require\_auth

<a id="app.api.admin_users.require_role"></a>

## require\_role

<a id="app.api.admin_users.success"></a>

## success

<a id="app.api.admin_users.BusinessError"></a>

## BusinessError

<a id="app.api.admin_users.UserService"></a>

## UserService

<a id="app.api.admin_users.bp"></a>

#### bp

<a id="app.api.admin_users.list_users"></a>

#### list\_users

```python
@bp.get('/users')
@require_auth()
@require_role('admin')
def list_users()
```

获取用户列表（管理员）

支持分页和筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- student_id (str): 学号筛选（模糊匹配）
- college (str): 学院筛选（模糊匹配）

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 用户列表
  - user_id: 用户ID
  - student_id: 学号
  - email: 邮箱
  - college: 学院
  - major: 专业
  - grade: 年级
  - status: 状态

<a id="app.api.admin_users.get_user_detail"></a>

#### get\_user\_detail

```python
@bp.get('/users/<int:user_id>')
@require_auth()
@require_role('admin')
def get_user_detail(user_id)
```

获取单个普通用户详细信息（管理员）

Path Parameters:
- user_id (int): 用户ID

**Returns**:

  - user_id: 用户ID
  - student_id: 学号
  - email: 邮箱
  - gender: 性别
  - college: 学院
  - major: 专业
  - grade: 年级
  - status: 状态

<a id="app.api.admin_users.list_organizers"></a>

#### list\_organizers

```python
@bp.get('/organizers')
@require_auth()
@require_role('admin')
def list_organizers()
```

获取组织者列表（管理员）

支持分页和筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- org_name (str): 组织名称筛选（模糊匹配）
- status (str): 状态筛选
- pending: 待审核
- approved: 已通过
- rejected: 已拒绝

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 组织者列表
  - organizer_id: 组织者ID
  - email: 邮箱
  - org_name: 组织名称
  - status: 状态

<a id="app.api.admin_users.get_organizer_detail"></a>

#### get\_organizer\_detail

```python
@bp.get('/organizers/<int:organizer_id>')
@require_auth()
@require_role('admin')
def get_organizer_detail(organizer_id)
```

获取单个组织者详细信息（管理员）

包含组织证明和审核状态

Path Parameters:
- organizer_id (int): 组织者ID

**Returns**:

  - organizer_id: 组织者ID
  - email: 邮箱
  - org_name: 组织名称
  - org_proof_text: 组织证明文本
  - org_proof_image: 组织证明图片URL
  - status: 状态
  - avatar: 头像
  - reject_reason: 拒绝原因

<a id="app.api.admin_users.review_organizer"></a>

#### review\_organizer

```python
@bp.put('/organizers/<int:organizer_id>/review')
@require_auth()
@require_role('admin')
def review_organizer(organizer_id)
```

审核组织者（管理员）

对新注册的组织者进行资质审核

Path Parameters:
- organizer_id (int): 组织者ID

Request Body:
- action (str): 审核动作
- approve: 审核通过
- reject: 审核拒绝
- reject_reason (str): 拒绝原因（action为reject时必填）

**Returns**:

  - organizer_id: 组织者ID
  - status: 新状态
  

**Raises**:

- `400` - action无效、拒绝时未填写原因

<a id="app.api.admin_users.create_admin"></a>

#### create\_admin

```python
@bp.post('/admins')
@require_auth()
@require_role('admin')
def create_admin()
```

创建管理员（需要超级管理员权限）

自动生成6位管理员编号

Request Body:
- email (str): 邮箱
- password (str): 密码
- username (str): 管理员名称
- role (str): 角色（admin/super_admin）

**Returns**:

  - admin_id: 管理员ID
  - admin_no: 管理员编号（6位）
  

**Raises**:

- `403` - 不是超级管理员
- `400` - 邮箱已存在、参数无效

<a id="app.api.admin_users.list_admins"></a>

#### list\_admins

```python
@bp.get('/admins')
@require_auth()
@require_role('admin')
def list_admins()
```

获取管理员列表

返回所有管理员信息（排除已删除的）

**Returns**:

- `list` - 管理员列表
  - admin_id: 管理员ID
  - admin_no: 管理员编号
  - email: 邮箱
  - username: 名称
  - role: 角色
  - status: 状态

<a id="app.api.admin_users.delete_admin"></a>

#### delete\_admin

```python
@bp.delete('/admins/<int:admin_id>')
@require_auth()
@require_role('admin')
def delete_admin(admin_id)
```

删除管理员（需要超级管理员权限）

软删除，将管理员状态设为 deleted

限制：
- 超级管理员不可删除

Path Parameters:
- admin_id (int): 要删除的管理员ID

**Returns**:

- `message` - 删除成功提示
  

**Raises**:

- `403` - 不是超级管理员、不能删除超级管理员
- `404` - 管理员不存在

<a id="app.api.categories"></a>

# app.api.categories

分类 API 路由模块

提供活动分类管理相关的 API 接口：
- 获取分类树形结构

分类用于活动的前端筛选和展示

<a id="app.api.categories.success"></a>

## success

<a id="app.api.categories.CategoryService"></a>

## CategoryService

<a id="app.api.categories.bp"></a>

#### bp

<a id="app.api.categories.get_categories"></a>

#### get\_categories

```python
@bp.get('')
def get_categories()
```

获取分类列表（树形结构）

返回两级分类的树形结构，便于前端渲染级联选择器或树形菜单。
预设分类包括：
- 学术类（讲座、竞赛、沙龙）
- 文体类（运动会、体育比赛、文艺演出）
- 志愿服务（志愿服务、募捐活动）
- 职业发展（招聘会、职业讲座、实习分享、简历指导）
- 社交活动（联谊活动、社团招新、迎新活动）
- 培训讲座（技能培训、语言培训、考试辅导）
- 其他

**Returns**:

- `list` - 树形结构的分类列表，每个节点包含：
  - id: 分类ID
  - name: 分类名称
  - level: 层级（1-一级分类，2-二级分类）
  - sort_order: 排序序号
  - children: 子分类列表（二级分类）

<a id="app.api.activities"></a>

# app.api.activities

活动 API 路由模块（组织者视角）

提供活动管理相关的 API 接口：
- 创建活动（草稿）
- 提交审核
- 更新活动
- 删除活动
- 获取我发布的活动列表
- 公开的活动列表和详情查询

<a id="app.api.activities.get_json_data"></a>

## get\_json\_data

<a id="app.api.activities.require_auth"></a>

## require\_auth

<a id="app.api.activities.require_role"></a>

## require\_role

<a id="app.api.activities.success"></a>

## success

<a id="app.api.activities.BusinessError"></a>

## BusinessError

<a id="app.api.activities.ActivityService"></a>

## ActivityService

<a id="app.api.activities.bp"></a>

#### bp

<a id="app.api.activities.create_activity"></a>

#### create\_activity

```python
@bp.post('/organizer/activities')
@require_auth()
@require_role('organizer')
def create_activity()
```

创建活动（草稿）

组织者创建活动，初始状态为 draft（草稿）
只有审核通过的组织者才能创建活动

Request Body:
- name (str): 活动名称
- category_id (int): 分类ID
- start_time (str): 开始时间
- end_time (str): 结束时间
- campus (str): 校区（良乡/中关村）
- location (str): 具体地点
- max_participants (int): 人数上限
- registration_deadline (str): 报名截止时间
- cancel_deadline (str): 取消报名截止时间
- description (str): 活动描述

**Returns**:

  - activity_id: 活动ID
  - status: 活动状态（draft）
  

**Raises**:

- `403` - 组织者账号未审核通过
- `404` - 活动分类不存在

<a id="app.api.activities.submit_activity"></a>

#### submit\_activity

```python
@bp.post('/organizer/activities/<int:activity_id>/submit')
@require_auth()
@require_role('organizer')
def submit_activity(activity_id)
```

提交活动审核

将活动提交给管理员审核
- 草稿状态 → pending（待审核）
- 已发布状态 → edit_pending（修改待审核）

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - activity_id: 活动ID
  - status: 新状态（pending/edit_pending）
  

**Raises**:

- `403` - 无权操作（不是自己的活动）
- `404` - 活动不存在

<a id="app.api.activities.list_activities"></a>

#### list\_activities

```python
@bp.get('/activities')
def list_activities()
```

获取活动列表（公开接口）

支持分页和多条件筛选，默认只显示可见状态的活动

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- keyword (str): 关键词搜索（活动名称）
- category_id (int): 分类ID
- campus (str): 校区筛选
- status (str): 状态筛选（逗号分隔）
- organizer_id (int): 组织者ID筛选
- start_date (str): 开始日期（格式：YYYY-MM-DD）

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 活动列表

<a id="app.api.activities.get_activity_detail"></a>

#### get\_activity\_detail

```python
@bp.get('/activities/<int:activity_id>')
def get_activity_detail(activity_id)
```

获取活动详情（公开接口）

根据当前登录用户角色返回不同内容：
- 未登录用户：只看到已发布的活动
- 普通用户：额外看到报名状态和签到状态
- 组织者/管理员：edit_pending 状态时看到修改内容

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

- `dict` - 活动详细信息

<a id="app.api.activities.update_activity"></a>

#### update\_activity

```python
@bp.put('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def update_activity(activity_id)
```

更新活动

根据活动状态决定更新方式：
- 草稿/待审核/已拒绝：直接更新
- 已发布状态：创建修改记录，进入二次审核

限制：
- 活动开始前1小时内不可修改
- 已发布活动的人数限制只能增加不能减少

Path Parameters:
- activity_id (int): 活动ID

Request Body:
与创建活动相同

**Returns**:

  - activity_id: 活动ID
  - status: 活动状态
  

**Raises**:

- `403` - 无权操作
- `400` - 修改时间过期、人数限制减少等

<a id="app.api.activities.delete_activity"></a>

#### delete\_activity

```python
@bp.delete('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def delete_activity(activity_id)
```

删除活动

彻底删除活动及所有相关数据（报名、签到、签到码、修改记录）
删除前会发送通知给所有已报名用户

限制：
- 活动已开始不可删除
- 活动开始前1小时内不可删除

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

- `message` - 删除成功提示
  

**Raises**:

- `403` - 无权操作
- `400` - 活动已开始或开始前1小时内

<a id="app.api.activities.get_my_activities"></a>

#### get\_my\_activities

```python
@bp.get('/organizer/activities')
@require_auth()
@require_role('organizer')
def get_my_activities()
```

获取我发布的活动列表（组织者专用）

返回当前组织者创建的所有活动
支持分页和筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- keyword (str): 关键词搜索（活动名称）
- category_id (int): 分类ID
- campus (str): 校区筛选
- status (str): 状态筛选（逗号分隔）
- start_date (str): 开始日期（格式：YYYY-MM-DD）

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 活动列表

<a id="app.api.admin_activities"></a>

# app.api.admin\_activities

管理员活动审核 API 路由模块

提供管理员对活动的审核和管理功能：
- 获取待审核活动列表
- 获取活动详情（管理员视角）
- 审核活动（通过/拒绝）
- 下架活动

<a id="app.api.admin_activities.get_json_data"></a>

## get\_json\_data

<a id="app.api.admin_activities.require_auth"></a>

## require\_auth

<a id="app.api.admin_activities.require_role"></a>

## require\_role

<a id="app.api.admin_activities.success"></a>

## success

<a id="app.api.admin_activities.BusinessError"></a>

## BusinessError

<a id="app.api.admin_activities.ActivityService"></a>

## ActivityService

<a id="app.api.admin_activities.bp"></a>

#### bp

<a id="app.api.admin_activities.list_review_activities"></a>

#### list\_review\_activities

```python
@bp.get('/activities')
@require_auth()
@require_role('admin')
def list_review_activities()
```

获取待审核活动列表（管理员）

默认显示 pending（待审核）和 edit_pending（修改待审核）状态的活动
支持分页和多条件筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- status (str): 状态筛选（逗号分隔，如 pending,edit_pending）
- keyword (str): 关键词搜索（活动名称）
- organizer_id (int): 组织者ID筛选
- category_id (int): 分类ID筛选
- start_date (str): 开始日期（格式：YYYY-MM-DD）

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 审核活动列表
  - activity_id: 活动ID
  - name: 活动名称
  - organizer_id: 组织者ID
  - organizer_name: 组织者名称
  - start_time: 开始时间
  - category_name: 分类名称
  - category_path: 分类路径
  - status: 活动状态

<a id="app.api.admin_activities.get_admin_activity_detail"></a>

#### get\_admin\_activity\_detail

```python
@bp.get('/activities/<int:activity_id>')
@require_auth()
@require_role('admin')
def get_admin_activity_detail(activity_id)
```

获取活动详情（管理员视角）

管理员可以看到更多信息：
- edit_pending 状态时可以看到待审核的修改内容
- 可以看到组织者信息
- 可以看到拒绝原因

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

- `dict` - 活动详细信息，包含组织者信息和审核状态

<a id="app.api.admin_activities.review_activity"></a>

#### review\_activity

```python
@bp.put('/activities/<int:activity_id>/review')
@require_auth()
@require_role('admin')
def review_activity(activity_id)
```

审核活动（管理员）

对 pending（待审核）或 edit_pending（修改待审核）状态的活动进行审核

审核通过：
- 新活动：状态变为 open（报名中）
- 修改审核：应用修改内容，状态恢复为之前的状态

审核拒绝：
- 新活动：状态变为 rejected（已拒绝）
- 修改审核：丢弃修改内容，活动恢复原状

审核结果会通过通知系统发送给组织者
修改审核通过时，还会通知已报名用户活动已变更

Path Parameters:
- activity_id (int): 活动ID

Request Body:
- action (str): 审核动作
- approve: 审核通过
- reject: 审核拒绝
- reject_reason (str): 拒绝原因（action为reject时必填）

**Returns**:

  - activity_id: 活动ID
  - new_status: 审核后的活动状态
  

**Raises**:

- `400` - action无效、拒绝时未填写原因、活动状态不可审核
- `404` - 活动不存在

<a id="app.api.admin_activities.remove_activity"></a>

#### remove\_activity

```python
@bp.put('/activities/<int:activity_id>/remove')
@require_auth()
@require_role('admin')
def remove_activity(activity_id)
```

下架活动（管理员）

将活动状态改为 removed（已下架），删除所有报名和签到数据
下架后会通知组织者和所有已报名用户

限制：
- 活动开始后不可下架

Path Parameters:
- activity_id (int): 活动ID

Request Body:
- reason (str): 下架原因（必填）

**Returns**:

- `message` - 下架成功提示
  

**Raises**:

- `400` - 未填写下架原因、活动已开始
- `404` - 活动不存在

<a id="app.api.registrations"></a>

# app.api.registrations

报名 API 路由模块

提供报名管理相关的 API 接口：
- 报名活动（普通用户）
- 取消报名（普通用户）
- 我的报名列表（普通用户）
- 活动报名人员列表（组织者）
- 拒绝报名（组织者）
- 活动数据统计（组织者）

<a id="app.api.registrations.get_json_data"></a>

## get\_json\_data

<a id="app.api.registrations.require_auth"></a>

## require\_auth

<a id="app.api.registrations.require_role"></a>

## require\_role

<a id="app.api.registrations.success"></a>

## success

<a id="app.api.registrations.BusinessError"></a>

## BusinessError

<a id="app.api.registrations.RegistrationService"></a>

## RegistrationService

<a id="app.api.registrations.bp"></a>

#### bp

<a id="app.api.registrations.register_activity"></a>

#### register\_activity

```python
@bp.post('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def register_activity(activity_id)
```

报名活动（普通用户）

用户报名参加指定活动

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - registration_id: 报名记录ID
  - status: 报名状态
  - remaining_slots: 剩余名额
  

**Raises**:

- `400` - 活动不可报名、报名已截止、名额已满、重复报名、被拒绝冷却中等
- `404` - 活动不存在

<a id="app.api.registrations.cancel_registration"></a>

#### cancel\_registration

```python
@bp.delete('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def cancel_registration(activity_id)
```

取消报名（普通用户）

取消对指定活动的报名
取消后名额不会立即释放，有2分钟延迟释放（给用户反悔机会）

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - release_time: 名额释放时间
  

**Raises**:

- `400` - 取消报名已截止、尚未报名
- `404` - 活动不存在

<a id="app.api.registrations.get_my_registrations"></a>

#### get\_my\_registrations

```python
@bp.get('/user/registrations')
@require_auth()
@require_role('user')
def get_my_registrations()
```

获取我的报名列表（普通用户）

返回当前用户的有效报名记录（registered/re_registered）
支持分页和多条件筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- name (str): 活动名称筛选（模糊匹配）
- activity_id (int): 活动ID筛选
- category_id (int): 分类ID筛选
- start_date (str): 开始日期筛选（格式：YYYY-MM-DD）
- campus (str): 校区筛选

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - list: 报名列表
  - registration_id: 报名记录ID
  - activity_id: 活动ID
  - activity_name: 活动名称
  - start_time: 开始时间
  - end_time: 结束时间
  - location: 地点
  - registration_time: 报名时间
  - status: 报名状态
  - checkin_status: 签到状态（checked/not_checked）
  - checkin_time: 签到时间（如已签到）

<a id="app.api.registrations.get_activity_registrations"></a>

#### get\_activity\_registrations

```python
@bp.get('/organizer/activities/<int:activity_id>/registrations')
@require_auth()
@require_role('organizer')
def get_activity_registrations(activity_id)
```

获取活动报名人员列表（组织者）

返回指定活动的报名人员信息，包含签到情况和统计数据

Path Parameters:
- activity_id (int): 活动ID

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- gender (str): 性别筛选
- college (str): 学院筛选
- grade (str): 年级筛选
- major (str): 专业筛选

**Returns**:

  - total: 总记录数
  - statistics: 统计数据
  - total_registered: 总报名人数
  - total_checked: 已签到人数
  - remaining_slots: 剩余名额
  - by_gender: 性别分布
  - by_college: 学院分布
  - by_grade: 年级分布
  - by_major: 专业分布
  - list: 报名人员列表
  - registration_id: 报名记录ID
  - user_id: 用户ID
  - student_id: 学号
  - gender: 性别
  - college: 学院
  - major: 专业
  - grade: 年级
  - registration_time: 报名时间
  - status: 状态
  - reject_reason: 拒绝原因
  - checkin_status: 签到状态

<a id="app.api.registrations.reject_registration"></a>

#### reject\_registration

```python
@bp.post('/organizer/registrations/<int:registration_id>/reject')
@require_auth()
@require_role('organizer')
def reject_registration(registration_id)
```

拒绝报名（组织者）

拒绝某用户的报名申请

拒绝规则：
- 第1次拒绝：状态变为 rejected（可再次报名，但有10分钟冷却）
- 第2次拒绝：状态变为 blocked（永久禁止报名该活动）

Path Parameters:
- registration_id (int): 报名记录ID

Request Body:
- reason (str): 拒绝原因

**Returns**:

  - new_status: 新状态（rejected/blocked）
  - reject_count: 拒绝次数
  

**Raises**:

- `400` - 未填写拒绝原因、该用户没有有效报名
- `403` - 无权操作（不是自己的活动）
- `404` - 报名记录不存在

<a id="app.api.registrations.get_registration_stats"></a>

#### get\_registration\_stats

```python
@bp.get('/activities/<int:activity_id>/registration-stats')
@require_auth()
@require_role('organizer')
def get_registration_stats(activity_id)
```

获取活动数据统计（组织者）

返回报名人数统计、签到人数、剩余名额、人员分布等
与上面的 get_activity_registrations 接口共用统计逻辑

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - total_registered: 总报名人数
  - remaining_slots: 剩余名额
  - total_checked: 已签到人数
  - by_gender: 性别分布
  - by_college: 学院分布
  - by_grade: 年级分布
  - by_major: 专业分布

<a id="app.api.checkin"></a>

# app.api.checkin

签到 API 路由模块

提供签到管理相关的 API 接口：
- 获取签到码（组织者）
- 扫码签到（普通用户）
- 手动签到（组织者）
- 我的签到记录（普通用户）
- 签到统计（组织者）

<a id="app.api.checkin.get_json_data"></a>

## get\_json\_data

<a id="app.api.checkin.require_auth"></a>

## require\_auth

<a id="app.api.checkin.require_role"></a>

## require\_role

<a id="app.api.checkin.success"></a>

## success

<a id="app.api.checkin.BusinessError"></a>

## BusinessError

<a id="app.api.checkin.CheckinService"></a>

## CheckinService

<a id="app.api.checkin.bp"></a>

#### bp

<a id="app.api.checkin.get_checkin_code"></a>

#### get\_checkin\_code

```python
@bp.get('/organizer/activities/<int:activity_id>/checkin-code')
@require_auth()
@require_role('organizer')
def get_checkin_code(activity_id)
```

获取签到码（组织者）

组织者可以在签到时间窗口内向用户展示签到码
如果活动还没有签到码，会自动生成一个6位随机码

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - checkin_code: 6位签到码（大写字母+数字）
  

**Raises**:

- `403` - 无权操作（不是自己的活动）
- `404` - 活动不存在

<a id="app.api.checkin.checkin"></a>

#### checkin

```python
@bp.post('/activities/<int:activity_id>/checkin')
@require_auth()
@require_role('user')
def checkin(activity_id)
```

扫码签到（普通用户）

用户通过输入组织者提供的签到码完成签到

签到时间窗口：
- 开始时间：活动开始前30分钟
- 结束时间：活动结束时间

前置条件：
- 用户必须已报名该活动
- 用户未签到过

Path Parameters:
- activity_id (int): 活动ID

Request Body:
- checkin_code (str): 签到码（6位）

**Returns**:

  - checkin_id: 签到记录ID
  - checkin_time: 签到时间
  

**Raises**:

- `400` - 缺少签到码、签到码错误、签到未开始、签到已结束
- `403` - 未报名

<a id="app.api.checkin.manual_checkin"></a>

#### manual\_checkin

```python
@bp.post('/organizer/activities/<int:activity_id>/manual-checkin')
@require_auth()
@require_role('organizer')
def manual_checkin(activity_id)
```

手动签到（组织者）

组织者通过输入用户学号帮助用户完成签到
适用于扫码失败的场景

Path Parameters:
- activity_id (int): 活动ID

Request Body:
- student_id (str): 用户学号（10位）

**Returns**:

  - user_id: 用户ID
  - checkin_time: 签到时间
  

**Raises**:

- `400` - 缺少学号、用户未报名、已签到
- `403` - 无权操作（不是自己的活动）
- `404` - 活动不存在、用户不存在

<a id="app.api.checkin.get_my_checkins"></a>

#### get\_my\_checkins

```python
@bp.get('/user/checkins')
@require_auth()
@require_role('user')
def get_my_checkins()
```

获取我的签到记录（普通用户）

返回用户历史签到记录，按签到时间倒序

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）

**Returns**:

  - total: 总记录数
  - list: 签到记录列表
  - activity_id: 活动ID
  - activity_name: 活动名称
  - activity_start_time: 活动开始时间
  - checkin_time: 签到时间
  - checkin_method: 签到方式（code/manual）

<a id="app.api.checkin.get_checkin_stats"></a>

#### get\_checkin\_stats

```python
@bp.get('/organizer/activities/<int:activity_id>/checkins')
@require_auth()
@require_role('organizer')
def get_checkin_stats(activity_id)
```

获取活动签到情况（组织者）

返回活动的签到统计数据和详细列表

Path Parameters:
- activity_id (int): 活动ID

**Returns**:

  - total_registered: 总报名人数
  - checked_in: 已签到人数
  - not_checked_in: 未签到人数
  - checkin_rate: 签到率（百分比）
  - checkin_list: 已签到用户列表
  - user_id: 用户ID
  - student_id: 学号
  - username: 用户名
  - college: 学院
  - major: 专业
  - grade: 年级
  - checkin_time: 签到时间
  - checkin_method: 签到方式
  - notCheckedIn: 未签到用户列表
  - user_id: 用户ID
  - student_id: 学号
  - username: 用户名
  - registration_time: 报名时间
  

**Raises**:

- `403` - 无权操作（不是自己的活动）
- `404` - 活动不存在

<a id="app.api.notifications"></a>

# app.api.notifications

通知与公告 API 路由模块

提供通知和公告管理相关的 API 接口：
- 获取我的通知列表
- 标记通知已读
- 发布系统公告（管理员）
- 获取系统公告
- 删除公告（管理员）

<a id="app.api.notifications.get_json_data"></a>

## get\_json\_data

<a id="app.api.notifications.require_auth"></a>

## require\_auth

<a id="app.api.notifications.require_role"></a>

## require\_role

<a id="app.api.notifications.success"></a>

## success

<a id="app.api.notifications.BusinessError"></a>

## BusinessError

<a id="app.api.notifications.NotificationService"></a>

## NotificationService

<a id="app.api.notifications.bp"></a>

#### bp

<a id="app.api.notifications.list_notifications"></a>

#### list\_notifications

```python
@bp.get('/notifications')
@require_auth()
def list_notifications()
```

获取我的通知列表

支持分页和未读筛选

Query Parameters:
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）
- unread (bool): 是否只显示未读（1/true/True）

**Returns**:

  - total: 总记录数
  - page: 当前页码
  - page_size: 每页数量
  - unread_count: 未读通知数量
  - list: 通知列表
  - notification_id: 通知ID
  - title: 标题
  - content: 内容
  - type: 通知类型
  - related_id: 关联业务ID
  - is_read: 是否已读
  - created_at: 创建时间

<a id="app.api.notifications.mark_notification_read"></a>

#### mark\_notification\_read

```python
@bp.put('/notifications/<int:notification_id>/read')
@require_auth()
def mark_notification_read(notification_id)
```

标记通知已读

将指定通知标记为已读状态

Path Parameters:
- notification_id (int): 通知ID

**Returns**:

- `message` - 已标记为已读
  

**Raises**:

- `404` - 通知不存在或不属于当前用户

<a id="app.api.notifications.create_announcement"></a>

#### create\_announcement

```python
@bp.post('/admin/announcements')
@require_auth()
@require_role('admin')
def create_announcement()
```

发布系统公告（管理员）

管理员可以发布全站公告，公告会在指定时间范围内对外展示

Request Body:
- title (str): 公告标题（不超过50字符）
- content (str): 公告正文
- start_time (str, optional): 生效时间
- 格式：%Y-%m-%d %H:%M:%S
- 不传则立即生效
- end_time (str, optional): 失效时间
- 格式：%Y-%m-%d %H:%M:%S
- 不传则默认30天后失效

**Returns**:

  - announcement_id: 公告ID
  

**Raises**:

- `400` - 标题/内容为空、标题过长、时间无效

<a id="app.api.notifications.list_announcements"></a>

#### list\_announcements

```python
@bp.get('/announcements')
def list_announcements()
```

获取系统公告

根据当前用户角色返回不同的数据：
- 管理员：返回所有公告（不限有效期）
- 普通用户/未登录：只返回有效期内的公告

**Returns**:

- `list` - 公告列表
  - announcement_id: 公告ID
  - title: 标题
  - content: 内容
  - start_time: 生效时间
  - end_time: 失效时间

<a id="app.api.notifications.delete_announcement"></a>

#### delete\_announcement

```python
@bp.delete('/admin/announcements/<int:announcement_id>')
@require_auth()
@require_role('admin')
def delete_announcement(announcement_id)
```

删除公告（管理员）

永久删除指定的系统公告

Path Parameters:
- announcement_id (int): 公告ID

**Returns**:

- `message` - 公告删除成功
  

**Raises**:

- `404` - 公告不存在

<a id="app.api.statistics"></a>

# app.api.statistics

统计 API 路由模块

提供数据统计相关的 API 接口：
- 平台数据统计（管理员）
- 用户活跃度排行榜（公开）

<a id="app.api.statistics.require_auth"></a>

## require\_auth

<a id="app.api.statistics.require_role"></a>

## require\_role

<a id="app.api.statistics.success"></a>

## success

<a id="app.api.statistics.StatsService"></a>

## StatsService

<a id="app.api.statistics.bp"></a>

#### bp

<a id="app.api.statistics.admin_statistics"></a>

#### admin\_statistics

```python
@bp.get('/admin/statistics')
@require_auth()
@require_role('admin')
def admin_statistics()
```

获取平台数据统计（管理员）

提供平台的宏观统计数据，用于管理后台的数据看板

**Returns**:

- `dict` - 平台统计数据，包含以下模块：
  
  - activities: 活动统计
  - total: 活动总数
  - by_statuss: 按状态分布
  - pending: 待审核
  - open: 报名中
  - edit_pending: 修改审核中
  - ongoing: 进行中
  - ended: 已结束
  - by_categories: 按分类分布
  - 学术类: 数量
  - 文体类: 数量
  - 志愿服务: 数量
  - ...
  
  - user: 用户统计
  - total: 总用户数（学生+组织者+管理员）
  - student: 学生数量
  - organize: 组织者数量
  - admin: 管理员数量
  
  - total_participation_count: 总报名次数
  - average_checkin_rate: 平均签到率

<a id="app.api.statistics.leaderboard"></a>

#### leaderboard

```python
@bp.get('/leaderboard')
def leaderboard()
```

获取用户活跃度排行榜（公开）

根据用户的报名次数和签到次数进行排名
支持按周期、学院、年级筛选

Query Parameters:
- period (str): 统计周期
- week: 最近一周
- month: 最近一个月
- all: 全部时间（默认）
- college (str): 学院筛选（可选）
- grade (str): 年级筛选（可选）
- page (int): 页码（默认1）
- page_size (int): 每页数量（默认20，最大100）

**Returns**:

  - total: 总记录数
  - list: 排行榜列表
  - rank: 排名
  - user_id: 用户ID
  - student_id: 学号
  - college: 学院
  - grade: 年级
  - registration_count: 报名次数
  - effective_participation_count: 有效参与次数（签到次数）
  
  排名规则:
  1. 优先按签到次数降序
  2. 签到次数相同时按报名次数降序
  3. 报名次数相同时按用户ID升序

