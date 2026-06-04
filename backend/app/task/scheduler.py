"""
定时任务调度模块

提供后台定时任务功能：
- 自动更新活动状态（根据时间）
- 发送活动开始提醒通知

使用 APScheduler 作为调度框架
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.common.database import db_session
from models import Activity, Registration
from app.services.notification_service import NotificationService


def update_activity_statuses():
    """
    更新活动状态（根据时间）
    
    根据当前时间自动更新活动状态：
    - open/edit_pending → ongoing（到达开始时间）
    - ongoing → ended（到达结束时间）
    
    执行频率：每 5 分钟
    
    edit_pending 状态同理（活动修改审核中但时间到了）
    """
    now = datetime.utcnow()
    
    with db_session() as session:
        activities_to_start = session.query(Activity).filter(
            Activity.status.in_(('open', 'edit_pending')),
            Activity.start_time <= now
        ).all()
        
        for activity in activities_to_start:
            old_status = activity.status
            activity.status = 'ongoing'
            print(f"活动 {activity.id} 状态从 {old_status} 更新为 ongoing")
        
        activities_to_end = session.query(Activity).filter(
            Activity.status == 'ongoing',
            Activity.end_time <= now
        ).all()
        
        for activity in activities_to_end:
            activity.status = 'ended'
            print(f"活动 {activity.id} 状态更新为 ended")
        
        session.flush()


def send_activity_reminders():
    """
    发送活动开始前1小时提醒
    
    查找即将开始的活动（1小时后开始），给已报名用户发送提醒通知
    
    执行频率：每 10 分钟
    
    防重复机制：
    - 检查是否已发送过提醒（通过 Notification 表）
    - 每个活动只发送一次提醒
    """
    now = datetime.utcnow()
    one_hour_later = now + timedelta(hours=1)
    
    with db_session() as session:
        activities_to_remind = session.query(Activity).filter(
            Activity.status.in_(('open', 'ongoing', 'edit_pending')),
            Activity.start_time > now,
            Activity.start_time <= one_hour_later
        ).all()
        
        for activity in activities_to_remind:
            registered_users = session.query(Registration.user_id).filter(
                Registration.activity_id == activity.id,
                Registration.status.in_(('registered', 're_registered'))
            ).all()
            
            if not registered_users:
                continue
            
            from models import Notification
            already_sent = session.query(Notification).filter(
                Notification.receiver_type == 'user',
                Notification.related_id == activity.id,
                Notification.type == 'activity_reminder'
            ).first()
            
            if already_sent:
                continue
            
            for (user_id,) in registered_users:
                NotificationService.create_notification(
                    session,
                    'user',
                    user_id,
                    '活动即将开始提醒',
                    f'您报名的活动 "{activity.name}" 将于 {activity.start_time.strftime("%Y-%m-%d %H:%M")} 开始，请准时参加！',
                    'activity_reminder',
                    activity.id
                )
            print(f"已向 {len(registered_users)} 位用户发送活动 {activity.id} 开始提醒")
        
        session.flush()

# ========== 调度器管理 ==========
# 创建全局调度器
_scheduler = None


def start_scheduler():
    """
    启动定时任务调度器
    
    在应用启动时调用（在 create_app 中执行）
    
    注册的任务：
    1. update_activity_statuses - 每 5 分钟执行
    2. send_activity_reminders - 每 10 分钟执行
    
    调度器配置：
    - 使用 BackgroundScheduler（后台线程）
    - 使用 IntervalTrigger（间隔触发）
    
    """
    global _scheduler
    if _scheduler is not None:
        return
    
    update_activity_statuses()
    _scheduler = BackgroundScheduler()
    
    _scheduler.add_job(
        update_activity_statuses,
        trigger=IntervalTrigger(minutes=5),
        id='update_activity_statuses'
    )
    
    _scheduler.add_job(
        send_activity_reminders,
        trigger=IntervalTrigger(minutes=10),
        id='send_activity_reminders'
    )
    
    _scheduler.start()
    print("定时任务调度器已启动")


def stop_scheduler():
    """
    停止定时任务调度器
    
    在应用关闭时调用，优雅地停止所有后台任务
    """
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        print("定时任务调度器已停止")