from datetime import datetime, timedelta
from sqlalchemy import func
from app.common.database import db_session
from app.common.errors import BusinessError
from models import Activity, User, Organizer, Admin, Registration, Checkin, Category


class StatsService:
    """统计服务"""

    ACTIVE_STATUSES = ('registered', 're_registered')
    PLATFORM_ACTIVITY_STATUSES = ('pending', 'open', 'edit_pending', 'ongoing', 'ended')

    @staticmethod
    def get_platform_stats():
        """获取平台数据统计（管理员）"""
        with db_session() as session:
            # 活动统计
            activity_query = session.query(Activity).filter(Activity.status.in_(StatsService.PLATFORM_ACTIVITY_STATUSES))
            activities_total = activity_query.count()

            status_counts = session.query(Activity.status, func.count(Activity.id)).filter(
                Activity.status.in_(StatsService.PLATFORM_ACTIVITY_STATUSES)
            ).group_by(Activity.status).all()
            by_statuss = {status: count for status, count in status_counts}
            for status in StatsService.PLATFORM_ACTIVITY_STATUSES:
                by_statuss.setdefault(status, 0)

            category_counts = session.query(Category.name, func.count(Activity.id)).join(
                Activity, Activity.category_id == Category.id
            ).filter(
                Activity.status.in_(StatsService.PLATFORM_ACTIVITY_STATUSES)
            ).group_by(Category.name).all()
            by_categories = {name: count for name, count in category_counts}

            # 用户统计
            student_count = session.query(User).filter(User.status != 'deleted').count()
            organizer_count = session.query(Organizer).filter(Organizer.status != 'deleted').count()
            admin_count = session.query(Admin).filter(Admin.status != 'deleted').count()

            # 参与统计
            total_registrations = session.query(Registration).filter(
                Registration.status.in_(StatsService.ACTIVE_STATUSES)
            ).count()
            total_checkins = session.query(Checkin).count()

            if total_registrations:
                average_checkin_rate = f'{(total_checkins / total_registrations * 100):.1f}%'
            else:
                average_checkin_rate = '0.0%'

            return {
                'activities': {
                    'total': activities_total,
                    'by_statuss': by_statuss,
                    'by_categories': by_categories
                },
                'user': {
                    'total': student_count + organizer_count + admin_count,
                    'student': student_count,
                    'organize': organizer_count,
                    'admin': admin_count
                },
                'total_participation_count': total_registrations,
                'average_checkin_rate': average_checkin_rate
            }

    @staticmethod
    def _parse_period(period):
        """解析周期参数"""
        period = str(period or 'all').strip().lower()
        if period not in ('week', 'month', 'all'):
            raise BusinessError('period无效', code=400)
        if period == 'week':
            return datetime.utcnow() - timedelta(days=7)
        if period == 'month':
            return datetime.utcnow() - timedelta(days=30)
        return None

    @staticmethod
    def get_leaderboard(params):
        """获取用户活跃度排行"""
        period = params.get('period', 'all')
        college = params.get('college', '').strip()
        grade = params.get('grade', '').strip()
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)

        period_start = StatsService._parse_period(period)

        with db_session() as session:
            user_query = session.query(User).filter(User.status != 'deleted')
            if college:
                user_query = user_query.filter(User.college == college)
            if grade:
                user_query = user_query.filter(User.grade == grade)

            # 报名次数子查询
            reg_query = session.query(
                Registration.user_id,
                func.count(Registration.id).label('registration_count')
            ).filter(Registration.status.in_(StatsService.ACTIVE_STATUSES))
            if period_start:
                reg_query = reg_query.filter(Registration.registration_time >= period_start)
            reg_query = reg_query.group_by(Registration.user_id)
            reg_subq = reg_query.subquery()

            # 签到次数子查询
            checkin_query = session.query(
                Checkin.user_id,
                func.count(Checkin.id).label('effective_count')
            )
            if period_start:
                checkin_query = checkin_query.filter(Checkin.checkin_time >= period_start)
            checkin_query = checkin_query.group_by(Checkin.user_id)
            checkin_subq = checkin_query.subquery()

            query = user_query.outerjoin(reg_subq, reg_subq.c.user_id == User.id).outerjoin(
                checkin_subq, checkin_subq.c.user_id == User.id
            ).add_columns(
                func.coalesce(reg_subq.c.registration_count, 0).label('registration_count'),
                func.coalesce(checkin_subq.c.effective_count, 0).label('effective_participation_count')
            )

            total = query.count()
            rows = query.order_by(
                func.coalesce(checkin_subq.c.effective_count, 0).desc(),
                func.coalesce(reg_subq.c.registration_count, 0).desc(),
                User.id.asc()
            ).offset((page - 1) * page_size).limit(page_size).all()

            data = []
            for index, (user, reg_count, eff_count) in enumerate(rows):
                data.append({
                    'rank': (page - 1) * page_size + index + 1,
                    'user_id': user.id,
                    'student_id': user.student_id,
                    'college': user.college,
                    'grade': user.grade,
                    'registration_count': int(reg_count),
                    'effective_participation_count': int(eff_count)
                })

            return {'total': total, 'list': data}