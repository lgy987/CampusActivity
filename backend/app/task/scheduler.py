# app/tasks/scheduler.py
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.common.database import db_session
from models import Activity, Registration
from app.services.notification_service import NotificationService


def update_activity_statuses():
    """更新活动状态（根据时间）"""
    now = datetime.utcnow()
    
    with db_session() as session:
        # 将开始时间已到的活动状态改为 ongoing
        activities_to_start = session.query(Activity).filter(
            Activity.status.in_(('open', 'edit_pending')),
            Activity.start_time <= now
        ).all()
        
        for activity in activities_to_start:
            old_status = activity.status
            activity.status = 'ongoing'
            print(f"活动 {activity.id} 状态从 {old_status} 更新为 ongoing")
        
        # 将结束时间已过的活动状态改为 ended
        activities_to_end = session.query(Activity).filter(
            Activity.status == 'ongoing',
            Activity.end_time <= now
        ).all()
        
        for activity in activities_to_end:
            activity.status = 'ended'
            print(f"活动 {activity.id} 状态更新为 ended")
        
        session.flush()


def send_activity_reminders():
    """发送活动开始前1小时提醒"""
    now = datetime.utcnow()
    one_hour_later = now + timedelta(hours=1)
    
    with db_session() as session:
        # 查找1小时后开始的活动
        activities_to_remind = session.query(Activity).filter(
            Activity.status.in_(('open', 'ongoing', 'edit_pending')),
            Activity.start_time > now,
            Activity.start_time <= one_hour_later
        ).all()
        
        for activity in activities_to_remind:
            # 获取已报名用户
            registered_users = session.query(Registration.user_id).filter(
                Registration.activity_id == activity.id,
                Registration.status.in_(('registered', 're_registered'))
            ).all()
            
            if not registered_users:
                continue
            
            # 检查是否已发送过提醒（避免重复发送）
            from models import Notification
            already_sent = session.query(Notification).filter(
                Notification.receiver_type == 'user',
                Notification.related_id == activity.id,
                Notification.type == 'activity_reminder'
            ).first()
            
            if already_sent:
                continue
            
            # 发送提醒通知
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


# 创建全局调度器
_scheduler = None


def start_scheduler():
    """启动定时任务调度器"""
    global _scheduler
    if _scheduler is not None:
        return
    
    _scheduler = BackgroundScheduler()
    
    # 每5分钟检查一次活动状态更新
    _scheduler.add_job(
        update_activity_statuses,
        trigger=IntervalTrigger(minutes=5),
        id='update_activity_statuses'
    )
    
    # 每10分钟检查一次活动提醒（避免频繁查询）
    _scheduler.add_job(
        send_activity_reminders,
        trigger=IntervalTrigger(minutes=10),
        id='send_activity_reminders'
    )
    
    _scheduler.start()
    print("定时任务调度器已启动")


def stop_scheduler():
    """停止定时任务调度器"""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        print("定时任务调度器已停止")