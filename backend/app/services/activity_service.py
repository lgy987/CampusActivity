from datetime import datetime
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from app.services.notification_service import NotificationService
from models import Activity, ActivityRevision, Category, Organizer, Registration


class ActivityService:
    """活动服务"""

    ACTIVE_STATUSES = ('registered', 're_registered')
    EDITABLE_DIRECT_STATUSES = ('draft', 'pending', 'rejected')

    @staticmethod
    def _parse_datetime(value):
        """解析日期时间字符串"""
        if not value:
            return None
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise BusinessError('Invalid datetime format')

    @staticmethod
    def _normalize_payload(data):
        """校验并标准化活动数据"""
        required = ['name', 'category_id', 'start_time', 'end_time', 'campus', 'location',
                    'max_participants', 'registration_deadline', 'cancel_deadline', 'description']
        missing = [f for f in required if not str(data.get(f, '')).strip()]
        if missing:
            raise BusinessError(f'缺少必填字段：{", ".join(missing)}')

        try:
            category_id = int(data['category_id'])
            max_participants = int(data['max_participants'])
        except (TypeError, ValueError):
            raise BusinessError('分类ID或人数上限无效')

        if max_participants <= 0:
            raise BusinessError('人数上限必须大于0')

        start_time = ActivityService._parse_datetime(data.get('start_time'))
        end_time = ActivityService._parse_datetime(data.get('end_time'))
        registration_deadline = ActivityService._parse_datetime(data.get('registration_deadline'))
        cancel_deadline = ActivityService._parse_datetime(data.get('cancel_deadline'))

        if not start_time or not end_time:
            raise BusinessError('活动时间不能为空')
        if end_time <= start_time:
            raise BusinessError('结束时间必须晚于开始时间')
        if registration_deadline and registration_deadline > start_time:
            raise BusinessError('报名截止时间必须早于活动开始')
        if cancel_deadline and cancel_deadline > start_time:
            raise BusinessError('取消截止时间必须早于活动开始')
        if registration_deadline and cancel_deadline and cancel_deadline > registration_deadline:
            raise BusinessError('取消截止时间必须早于报名截止时间')

        return {
            'name': str(data['name']).strip(),
            'category_id': category_id,
            'start_time': start_time,
            'end_time': end_time,
            'campus': str(data['campus']).strip(),
            'location': str(data['location']).strip(),
            'max_participants': max_participants,
            'registration_deadline': registration_deadline,
            'cancel_deadline': cancel_deadline,
            'description': str(data['description']).strip()
        }

    @staticmethod
    def create_activity(organizer_id, data):
        """创建活动（草稿）"""
        payload = ActivityService._normalize_payload(data)

        with db_session() as session:
            organizer = session.get(Organizer, organizer_id)
            if not organizer or organizer.status != 'approved':
                raise BusinessError('组织者账号未审核通过，暂不能创建活动', code=403, status_code=403)

            if not session.get(Category, payload['category_id']):
                raise BusinessError('活动分类不存在', code=404, status_code=404)

            activity = Activity(
                organizer_id=organizer_id,
                category_id=payload['category_id'],
                name=payload['name'],
                start_time=payload['start_time'],
                end_time=payload['end_time'],
                campus=payload['campus'],
                location=payload['location'],
                max_participants=payload['max_participants'],
                current_participants=0,
                registration_deadline=payload['registration_deadline'],
                cancel_deadline=payload['cancel_deadline'],
                description=payload['description'],
                status='draft'
            )
            session.add(activity)
            session.flush()

            return {'activity_id': activity.id, 'status': activity.status}

    @staticmethod
    def submit_activity(organizer_id, activity_id):
        """提交审核"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity or activity.status == 'removed':
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            if activity.status in ('open', 'ongoing', 'edit_pending'):
                activity.status = 'edit_pending'
            else:
                activity.status = 'pending'
            activity.reject_reason = None
            session.flush()

            return {'activity_id': activity.id, 'status': activity.status}

    @staticmethod
    def _category_map(session):
        """获取分类映射"""
        return {row.id: row for row in session.query(Category).all()}

    @staticmethod
    def _category_path(category_id, by_id):
        """获取分类完整路径"""
        names = []
        current = by_id.get(category_id)
        while current:
            names.append(current.name)
            current = by_id.get(current.parent_id)
        return ' > '.join(reversed(names))

    @staticmethod
    def list_activities(params):
        """获取活动列表"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        keyword = params.get('keyword', '').strip()
        category_id = params.get('category_id')
        campus = params.get('campus', '').strip()
        statuses = [s.strip() for s in params.get('status', '').split(',') if s.strip()] if params.get('status') else None
        organizer_id = params.get('organizer_id')
        start_date = params.get('start_date')

        with db_session() as session:
            query = session.query(Activity)

            if keyword:
                query = query.filter(Activity.name.contains(keyword))
            if category_id:
                try:
                    cat_id = int(category_id)
                    # 检查是否为一级分类（parent_id == 0）
                    category = session.get(Category, cat_id)
                    if category and category.parent_id == 0:
                        # 一级分类：查询所有子分类ID
                        child_ids = session.query(Category.id).filter(Category.parent_id == cat_id).all()
                        child_ids = [c[0] for c in child_ids]
                        if child_ids:
                            query = query.filter(Activity.category_id.in_(child_ids))
                        else:
                            # 没有子分类，按原分类查（理论上不会发生）
                            query = query.filter(Activity.category_id == cat_id)
                    else:
                        # 二级分类：精确匹配
                        query = query.filter(Activity.category_id == cat_id)
                except ValueError:
                    raise BusinessError('分类ID无效')
            if campus:
                query = query.filter(Activity.campus == campus)
            if statuses:
                query = query.filter(Activity.status.in_(statuses))
            else:
                query = query.filter(Activity.status.in_(('open', 'ongoing', 'edit_pending')))
            if organizer_id:
                try:
                    query = query.filter(Activity.organizer_id == int(organizer_id))
                except ValueError:
                    raise BusinessError('组织者ID无效')
            if start_date:
                from datetime import timezone, timedelta
                try:
                    # 解析本地日期
                    local_date = datetime.strptime(start_date, '%Y-%m-%d')
                    # 本地日期的开始时间（00:00:00）转换为 UTC
                    # 假设本地时区为东八区（UTC+8）
                    china_tz = timezone(timedelta(hours=8))
                    local_start = local_date.replace(tzinfo=china_tz)
                    utc_start = local_start.astimezone(timezone.utc).replace(tzinfo=None)
                    local_end = local_date.replace(hour=23, minute=59, second=59, tzinfo=china_tz)
                    utc_end = local_end.astimezone(timezone.utc).replace(tzinfo=None)
                     # 筛选当天范围内的活动
                    query = query.filter(
                        Activity.start_time >= utc_start,
                        Activity.start_time <= utc_end
                    )
                    # 筛选 start_time >= UTC 开始时间
                except ValueError:
                    raise BusinessError('start_date无效')

            total = query.count()
            rows = query.order_by(Activity.start_time.desc(), Activity.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

            categories = ActivityService._category_map(session)
            from app.services.registration_service import RegistrationService
            items = []
            for row in rows:
                category = categories.get(row.category_id)
                current_participants = RegistrationService._active_count(session, row.id)
                items.append({
                    'activity_id': row.id,
                    'name': row.name,
                    'start_time': dt(row.start_time),
                    'category_name': category.name if category else None,
                    'category_path': ActivityService._category_path(row.category_id, categories) if category else None,
                    'location': row.location,
                    'campus': row.campus,
                    'current_participants': current_participants,
                    'max_participants': row.max_participants
                })

            return {'total': total, 'page': page, 'page_size': page_size, 'list': items}

    @staticmethod
    def get_detail(activity_id, role, user_id):
        """获取活动详情"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)

            organizer = session.get(Organizer, activity.organizer_id)
            categories = ActivityService._category_map(session)

            # 如果是 edit_pending 状态，管理员或组织者看到修改内容
            revision = None
            if activity.status == 'edit_pending' and role in ('admin', 'organizer'):
                if role == 'admin' or user_id == activity.organizer_id:
                    revision = session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity_id).first()
            source = revision or activity

            # 获取当前用户报名和签到状态
            registration = None
            checkin = None
            if role == 'user' and user_id:
                registration = session.query(Registration).filter(
                    Registration.activity_id == activity_id, Registration.user_id == user_id
                ).first()
                from models import Checkin
                checkin = session.query(Checkin).filter(
                    Checkin.activity_id == activity_id, Checkin.user_id == user_id
                ).first()

            from app.services.registration_service import RegistrationService
            current_participants = RegistrationService._active_count(session, activity_id)

            category = categories.get(source.category_id)
            return {
                'activity_id': activity.id,
                'organizer_id': activity.organizer_id,
                'organizer_name': organizer.org_name if organizer else None,
                'name': source.name,
                'category_id': source.category_id,
                'category_name': category.name if category else None,
                'category_path': ActivityService._category_path(source.category_id, categories) if category else None,
                'start_time': dt(source.start_time),
                'end_time': dt(source.end_time),
                'campus': source.campus,
                'location': source.location,
                'max_participants': source.max_participants,
                'current_participants': current_participants,
                'registration_deadline': dt(source.registration_deadline),
                'cancel_deadline': dt(source.cancel_deadline),
                'description': source.description,
                'status': activity.status,
                'is_registered': bool(registration and registration.status in ActivityService.ACTIVE_STATUSES),
                'registration_status': registration.status if registration else None,
                'check_status': bool(checkin)
            }

    @staticmethod
    def update_activity(organizer_id, activity_id, data):
        """更新活动"""
        payload = ActivityService._normalize_payload(data)

        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity or activity.status == 'removed':
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            if not session.get(Category, payload['category_id']):
                raise BusinessError('活动分类不存在', code=404, status_code=404)

            from datetime import datetime, timedelta
            now = datetime.utcnow()
            # 如果活动已发布（open/ongoing/edit_pending），检查是否在开始前1小时内
            if activity.status in ('open', 'ongoing', 'edit_pending'):
                if now >= activity.start_time - timedelta(hours=1):
                    raise BusinessError('活动开始前1小时内不允许修改', code=400)
                
            # 人数限制校验：已发布活动只能增加不能减少
            if activity.status in ('open', 'ongoing', 'edit_pending') and payload['max_participants'] < activity.max_participants:
                raise BusinessError('人数限制只能增加，不能减少', code=400)

            if activity.status in ActivityService.EDITABLE_DIRECT_STATUSES:
                # 直接更新
                ActivityService._apply_activity_fields(activity, payload)
            else:
                # 需要二次审核
                revision = session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity.id).first()
                if not revision:
                    revision = ActivityRevision(
                        activity_id=activity.id,
                        organizer_id=activity.organizer_id,
                        category_id=payload['category_id'],
                        name=payload['name'],
                        start_time=payload['start_time'],
                        end_time=payload['end_time'],
                        campus=payload['campus'],
                        location=payload['location'],
                        max_participants=payload['max_participants'],
                        registration_deadline=payload['registration_deadline'],
                        cancel_deadline=payload['cancel_deadline'],
                        description=payload['description']
                    )
                    session.add(revision)
                else:
                    ActivityService._apply_revision_fields(revision, payload)
                activity.status = 'edit_pending'

            activity.reject_reason = None
            session.flush()

            return {'activity_id': activity.id, 'status': activity.status}

    @staticmethod
    def _apply_activity_fields(activity, payload):
        """应用活动字段"""
        activity.name = payload['name']
        activity.category_id = payload['category_id']
        activity.start_time = payload['start_time']
        activity.end_time = payload['end_time']
        activity.campus = payload['campus']
        activity.location = payload['location']
        activity.max_participants = payload['max_participants']
        activity.registration_deadline = payload['registration_deadline']
        activity.cancel_deadline = payload['cancel_deadline']
        activity.description = payload['description']

    @staticmethod
    def _apply_revision_fields(revision, payload):
        """应用修改记录字段"""
        revision.name = payload['name']
        revision.category_id = payload['category_id']
        revision.start_time = payload['start_time']
        revision.end_time = payload['end_time']
        revision.campus = payload['campus']
        revision.location = payload['location']
        revision.max_participants = payload['max_participants']
        revision.registration_deadline = payload['registration_deadline']
        revision.cancel_deadline = payload['cancel_deadline']
        revision.description = payload['description']

    @staticmethod
    def delete_activity(organizer_id, activity_id):
        """删除活动（组织者）- 彻底删除活动及所有相关数据"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity or activity.status == 'removed':
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)
        
            from datetime import datetime, timedelta
            now = datetime.utcnow()
        
            # 检查活动是否已开始
            if activity.start_time and now > activity.start_time:
                raise BusinessError('活动已开始，无法删除', code=400)
        
            # 检查是否在活动开始前1小时内
            if activity.start_time and now >= activity.start_time - timedelta(hours=1):
                raise BusinessError('活动开始前1小时内不允许删除', code=400)

            activity_name = activity.name
        
            # 获取所有已报名用户（在删除前）
            registered_users = session.query(Registration.user_id).filter(
                Registration.activity_id == activity_id,
                Registration.status.in_(ActivityService.ACTIVE_STATUSES)
            ).all()
        
            # 发送通知给报名用户（在删除前）
            for (user_id,) in registered_users:
                NotificationService.create_notification(
                    session, 'user', user_id,
                    '活动删除',
                    f'你的活动 {activity_name} 被组织者删除了。',
                    'activity_change', activity_id
            )
        
            # 通知组织者自己
            NotificationService.create_notification(
                session, 'organizer', organizer_id,
                'Activity Deleted',
                f'Your activity {activity_name} has been deleted.',
                'activity_audit_result', activity_id
            )
        
            # 删除所有相关数据
            session.query(Registration).filter(Registration.activity_id == activity_id).delete()
            from models import Checkin, ActivityCheckinCode
            session.query(Checkin).filter(Checkin.activity_id == activity_id).delete()
            session.query(ActivityCheckinCode).filter(ActivityCheckinCode.activity_id == activity_id).delete()
            session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity_id).delete()
        
            # 最后删除活动
            session.delete(activity)
            session.flush()

    @staticmethod
    def get_my_activities(organizer_id, params):
        """获取我发布的活动"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        keyword = params.get('keyword', '').strip()
        category_id = params.get('category_id')
        campus = params.get('campus', '').strip()
        statuses = [s.strip() for s in params.get('status', '').split(',') if s.strip()] if params.get('status') else None
        start_date = params.get('start_date')

        with db_session() as session:
            query = session.query(Activity).filter(Activity.organizer_id == organizer_id)

            if keyword:
                query = query.filter(Activity.name.contains(keyword))
            if category_id:
                try:
                    cat_id = int(category_id)
                    # 检查是否为一级分类（parent_id == 0）
                    category = session.get(Category, cat_id)
                    if category and category.parent_id == 0:
                    # 一级分类：查询所有子分类ID
                        child_ids = session.query(Category.id).filter(Category.parent_id == cat_id).all()
                        child_ids = [c[0] for c in child_ids]
                        if child_ids:
                            query = query.filter(Activity.category_id.in_(child_ids))
                        else:
                            # 没有子分类，按原分类查（理论上不会发生）
                            query = query.filter(Activity.category_id == cat_id)
                    else:
                        # 二级分类：精确匹配
                        query = query.filter(Activity.category_id == cat_id)
                except ValueError:
                    raise BusinessError('分类ID无效')
            
            if campus:
                query = query.filter(Activity.campus == campus)
            if statuses:
                query = query.filter(Activity.status.in_(statuses))
            if start_date:
                from datetime import timezone, timedelta
                try:
                    # 解析本地日期
                    local_date = datetime.strptime(start_date, '%Y-%m-%d')
                    # 本地日期的开始时间（00:00:00）转换为 UTC
                    # 假设本地时区为东八区（UTC+8）
                    china_tz = timezone(timedelta(hours=8))
                    local_start = local_date.replace(tzinfo=china_tz)
                    utc_start = local_start.astimezone(timezone.utc).replace(tzinfo=None)
                    local_end = local_date.replace(hour=23, minute=59, second=59, tzinfo=china_tz)
                    utc_end = local_end.astimezone(timezone.utc).replace(tzinfo=None)
                
                    query = query.filter(
                        Activity.start_time >= utc_start,
                        Activity.start_time <= utc_end
                    )
                except ValueError:
                    raise BusinessError('start_date无效')

            total = query.count()
            rows = query.order_by(Activity.start_time.desc(), Activity.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

            categories = ActivityService._category_map(session)
            items = []
            for row in rows:
                revision = session.query(ActivityRevision).filter(ActivityRevision.activity_id == row.id).first() if row.status == 'edit_pending' else None
                source = revision or row
                category = categories.get(source.category_id)
                items.append({
                    'activity_id': row.id,
                    'name': source.name,
                    'start_time': dt(source.start_time),
                    'category_name': category.name if category else None,
                    'category_path': ActivityService._category_path(source.category_id, categories) if category else None,
                    'location': source.location,
                    'campus': source.campus,
                    'current_participants': row.current_participants,
                    'max_participants': source.max_participants,
                    'status': row.status
                })

            return {'total': total, 'page': page, 'page_size': page_size, 'list': items}

    @staticmethod
    def list_review_activities(params):
        """获取审核活动列表（管理员）"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        statuses = [s.strip() for s in params.get('status', '').split(',') if s.strip()] if params.get('status') else None
        keyword = params.get('keyword', '').strip()
        organizer_id = params.get('organizer_id')
        category_id = params.get('category_id')
        start_date = params.get('start_date')

        with db_session() as session:
            query = session.query(Activity, Organizer).join(Organizer, Activity.organizer_id == Organizer.id)

            if statuses:
                query = query.filter(Activity.status.in_(statuses))
            else:
                query = query.filter(Activity.status.in_(('pending', 'edit_pending')))
            if keyword:
                query = query.filter(Activity.name.contains(keyword))
            if organizer_id:
                try:
                    query = query.filter(Activity.organizer_id == int(organizer_id))
                except ValueError:
                    raise BusinessError('组织者ID无效')
            if category_id:
                try:
                    query = query.filter(Activity.category_id == int(category_id))
                except ValueError:
                    raise BusinessError('分类ID无效')
            if start_date:
                from datetime import timezone, timedelta
                try:
                    # 解析本地日期
                    local_date = datetime.strptime(start_date, '%Y-%m-%d')
                    # 本地日期的开始时间（00:00:00）转换为 UTC
                    # 假设本地时区为东八区（UTC+8）
                    china_tz = timezone(timedelta(hours=8))
                    local_start = local_date.replace(tzinfo=china_tz)
                    utc_start = local_start.astimezone(timezone.utc).replace(tzinfo=None)
                    local_end = local_date.replace(hour=23, minute=59, second=59, tzinfo=china_tz)
                    utc_end = local_end.astimezone(timezone.utc).replace(tzinfo=None)
                
                    query = query.filter(
                        Activity.start_time >= utc_start,
                        Activity.start_time <= utc_end
                    )
                except ValueError:
                    raise BusinessError('start_date无效')

            total = query.count()
            rows = query.order_by(Activity.start_time.desc(), Activity.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

            categories = ActivityService._category_map(session)
            items = []
            for activity, organizer in rows:
                revision = session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity.id).first() if activity.status == 'edit_pending' else None
                source = revision or activity
                category = categories.get(source.category_id)
                items.append({
                    'activity_id': activity.id,
                    'name': source.name,
                    'organizer_id': organizer.id,
                    'organizer_name': organizer.org_name,
                    'start_time': dt(source.start_time),
                    'category_name': category.name if category else None,
                    'category_path': ActivityService._category_path(source.category_id, categories) if category else None,
                    'status': activity.status
                })

            return {'total': total, 'page': page, 'page_size': page_size, 'list': items}

    @staticmethod
    def review_activity(activity_id, action, reject_reason):
        """审核活动（管理员）"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity or activity.status == 'removed':
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.status not in ('pending', 'edit_pending'):
                raise BusinessError('当前活动状态不可审核', code=400)

            is_edit_pending = (activity.status == 'edit_pending')
            revision = None
        
            if is_edit_pending:
                revision = session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity.id).first()

            if action == 'approve':
                if is_edit_pending:
                    if revision:
                        ActivityService._apply_activity_fields(activity, {
                            'name': revision.name,
                            'category_id': revision.category_id,
                            'start_time': revision.start_time,
                            'end_time': revision.end_time,
                            'campus': revision.campus,
                            'location': revision.location,
                            'max_participants': revision.max_participants,
                            'registration_deadline': revision.registration_deadline,
                            'cancel_deadline': revision.cancel_deadline,
                            'description': revision.description
                        })
                        session.delete(revision)
                    activity.status = ActivityService._compute_activity_status(activity)
                else:
                    activity.status = 'open'
                activity.reject_reason = None
                new_status = activity.status
            
                # 通知组织者
                organizer_notice = f'你的活动 {activity.name} 已通过审核。'
                NotificationService.create_notification(
                    session, 'organizer', activity.organizer_id,
                    '活动审核结果', organizer_notice,
                    'activity_audit_result', activity.id
                )
            
                # 如果是 edit_pending，还需要通知所有已报名用户活动已变更
                if is_edit_pending:
                    # 获取所有已报名用户
                    registered_users = session.query(Registration.user_id).filter(
                        Registration.activity_id == activity_id,
                        Registration.status.in_(('registered', 're_registered'))
                    ).all()
                
                    user_notice = f'活动 "{activity.name}" 信息已更新，请查看最新详情。'
                    for (user_id,) in registered_users:
                        NotificationService.create_notification(
                            session, 'user', user_id,
                            '活动变更通知', user_notice,
                            'activity_change', activity.id
                        )
            else:  # reject
                if is_edit_pending:
                    if revision:
                        session.delete(revision)
                    activity.status = ActivityService._compute_activity_status(activity)
                    activity.reject_reason = reject_reason
                    new_status = activity.status
                else:
                    activity.status = 'rejected'
                    activity.reject_reason = reject_reason
                    new_status = 'rejected'
            
                organizer_notice = f'你的活动 {activity.name} 被拒绝。原因: {reject_reason}'
                NotificationService.create_notification(
                    session, 'organizer', activity.organizer_id,
                    '活动审核结果', organizer_notice,
                    'activity_audit_result', activity.id
                )
            # 拒绝时不需要通知已报名用户（活动未变更）

            session.flush()
            return {'activity_id': activity.id, 'new_status': new_status}

    @staticmethod
    def _compute_activity_status(activity):
        """计算活动当前状态（基于时间）"""
        from datetime import datetime
        now = datetime.utcnow()
        if activity.end_time and now > activity.end_time:
            return 'ended'
        if activity.start_time and activity.start_time <= now <= activity.end_time:
            return 'ongoing'
        return 'open'

    @staticmethod
    def remove_activity(activity_id, reason):
        """下架活动（管理员）- 状态改为removed，删除报名和签到数据"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity or activity.status == 'removed':
                raise BusinessError('活动不存在', code=404, status_code=404)
        
            from datetime import datetime
            now = datetime.utcnow()
        
            # 可选：活动开始后不能下架
            if activity.start_time and now > activity.start_time:
                raise BusinessError('活动已开始，无法下架', code=400)

            activity_name = activity.name
        
            # 获取所有已报名用户（在删除前）
            registered_users = session.query(Registration.user_id).filter(
                Registration.activity_id == activity_id,
                Registration.status.in_(ActivityService.ACTIVE_STATUSES)
            ).all()
        
            # 发送通知给报名用户
            for (user_id,) in registered_users:
                NotificationService.create_notification(
                    session, 'user', user_id,
                    '活动下架',
                    f'你的活动{activity_name} 被管理员下架了。原因是 {reason}',
                    'activity_audit_result', activity_id
                )
        
            # 通知组织者
            NotificationService.create_notification(
                session, 'organizer', activity.organizer_id,
                '活动下架',
                f'你的活动 {activity_name} 被管理员下架了。原因是 {reason}',
                'activity_audit_result', activity_id
            )
        
            # 删除所有相关数据
            session.query(Registration).filter(Registration.activity_id == activity_id).delete()
            from models import Checkin, ActivityCheckinCode
            session.query(Checkin).filter(Checkin.activity_id == activity_id).delete()
            session.query(ActivityCheckinCode).filter(ActivityCheckinCode.activity_id == activity_id).delete()
            session.query(ActivityRevision).filter(ActivityRevision.activity_id == activity_id).delete()
        
            # 更新活动状态
            activity.status = 'removed'
            activity.reject_reason = reason
            activity.current_participants = 0
        
            session.flush()