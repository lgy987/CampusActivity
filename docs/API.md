<a id="models"></a>

# models

<a id="models.User"></a>

## User Objects

```python
class User(Base)
```

<a id="models.User.status"></a>

#### status

active/deleted

<a id="models.Organizer"></a>

## Organizer Objects

```python
class Organizer(Base)
```

<a id="models.Organizer.status"></a>

#### status

pending/approved/rejected/deleted

<a id="models.Admin"></a>

## Admin Objects

```python
class Admin(Base)
```

<a id="models.Admin.role"></a>

#### role

admin/super_admin

<a id="models.Activity"></a>

## Activity Objects

```python
class Activity(Base)
```

<a id="models.Activity.status"></a>

#### status

draft/pending/rejected/edit_pending/open/ongoing/ended/removed

<a id="models.Registration"></a>

## Registration Objects

```python
class Registration(Base)
```

<a id="models.Registration.status"></a>

#### status

registered/cancelled/rejected/re_registered/blocked

<a id="models.Checkin"></a>

## Checkin Objects

```python
class Checkin(Base)
```

<a id="models.Checkin.checkin_method"></a>

#### checkin\_method

code/manual

<a id="models.Checkin.operator_id"></a>

#### operator\_id

组织者ID

<a id="models.Notification"></a>

## Notification Objects

```python
class Notification(Base)
```

<a id="models.Notification.receiver_type"></a>

#### receiver\_type

user/organizer

<a id="models.Notification.type"></a>

#### type

registration_result/activity_audit_result/...

