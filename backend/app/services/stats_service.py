"""
统计服务模块

提供平台级别的数据统计功能：
- 平台整体数据统计（管理员用）
- 用户活跃度排行榜
"""
from datetime import datetime, timedelta
from sqlalchemy import func
from app.common.database import db_session
from app.common.errors import BusinessError
from models import Activity, User, Organizer, Admin, Registration, Checkin, Category


class StatsService:
    """
    统计服务类
    
    提供平台数据统计和排行榜功能：
    - 活动统计（按状态、按分类）
    - 用户统计（学生、组织者、管理员）
    - 参与统计（报名数、签到数、签到率）
    - 用户活跃度排行榜
    """

    ACTIVE_STATUSES = ('registered', 're_registered')
    PLATFORM_ACTIVITY_STATUSES = ('pending', 'open', 'edit_pending', 'ongoing', 'ended')

    # ========== 私有辅助方法 ==========
    @staticmethod
    def _parse_period(period):
        """
        解析周期参数
        
        Args:
            period (str): 周期类型
                - week: 最近一周
                - month: 最近一个月
                - all: 全部时间
        
        Returns:
            datetime: 周期开始时间，如果 period 为 all 则返回 None
        
        Raises:
            BusinessError: period 参数无效
        """
        period = str(period or 'all').strip().lower()
        if period not in ('week', 'month', 'all'):
            raise BusinessError('period无效', code=400)
        if period == 'week':
            return datetime.utcnow() - timedelta(days=7)
        if period == 'month':
            return datetime.utcnow() - timedelta(days=30)
        return None
    # ========== 核心业务方法 ==========
    @staticmethod
    def get_platform_stats():
        """
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
        
        Returns:
            dict: 平台统计数据
        """
        with db_session() as session:
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

            student_count = session.query(User).filter(User.status != 'deleted').count()
            organizer_count = session.query(Organizer).filter(Organizer.status != 'deleted').count()
            admin_count = session.query(Admin).filter(Admin.status != 'deleted').count()

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
    def get_leaderboard(params):
        """
        获取用户活跃度排行
        
        根据用户的报名次数和签到次数进行排名
        支持按周期（周/月/全部）、学院、年级筛选
        
        排名规则：
        - 主要按签到次数降序
        - 签到次数相同按报名次数降序
        - 报名次数相同按用户ID升序
        
        Args:
            params (dict): 查询参数
                - period: 统计周期（week/month/all，默认all）
                - college: 学院筛选（可选）
                - grade: 年级筛选（可选）
                - page: 页码（默认1）
                - page_size: 每页数量（默认20，最大100）
        
        Returns:
            dict: 分页的排行榜列表，每条包含排名、用户信息、报名次数、签到次数
        """
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

            reg_query = session.query(
                Registration.user_id,
                func.count(Registration.id).label('registration_count')
            ).filter(Registration.status.in_(StatsService.ACTIVE_STATUSES))
            if period_start:
                reg_query = reg_query.filter(Registration.registration_time >= period_start)
            reg_query = reg_query.group_by(Registration.user_id)
            reg_subq = reg_query.subquery()

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