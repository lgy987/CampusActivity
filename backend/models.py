from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    """用户表 - 存储普通用户账号信息"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)  #用户ID，主键
    student_id = Column(String(20), unique=True, nullable=False, index=True)    #学号，10位数字，唯一索引，用于登录
    email = Column(String(100), unique=True, nullable=False, index=True)    #邮箱，唯一索引，用于登录
    username = Column(String(20), nullable=False)   #用户名/昵称
    password = Column(String(255), nullable=False)  #密码（哈希+盐值）
    gender = Column(String(10), nullable=False)     #性别：男/女
    college = Column(String(50), nullable=False)    #学院
    major = Column(String(50), nullable=False)  #专业
    grade = Column(String(20), nullable=False)  #年级，如：2023级
    phone = Column(String(11), nullable=True)   #联系方式，11位手机号
    avatar = Column(String(255), nullable=True) #头像URL
    status = Column(String(20), default='active', index=True)  #状态 状态：active-活跃，deleted-注销

class Organizer(Base):
    """组织者表 - 存储活动组织者/社团账号信息"""
    __tablename__ = 'organizer'
    id = Column(Integer, primary_key=True, autoincrement=True)  #组织者ID，主键
    email = Column(String(100), unique=True, nullable=False, index=True)    #邮箱，唯一索引，用于登录
    org_name = Column(String(50), nullable=False)   #组织名称
    password = Column(String(255), nullable=False)  #密码（哈希+盐值）
    org_proof_text = Column(Text, nullable=False)   #组织证明文本
    org_proof_image = Column(String(255), nullable=True)    #组织证明图片URL
    avatar = Column(String(255), nullable=True) #头像URL
    status = Column(String(20), default='pending', index=True)  # 状态：pending-待审核，approved-已通过，rejected-已拒绝，deleted-注销
    reject_reason = Column(Text, nullable=True) #审核不通过原因

class Admin(Base):
    """管理员表 - 存储管理员账号信息"""
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True) #管理员ID，主键
    admin_no = Column(String(6), unique=True, nullable=False, index=True) #管理员编号，6位数字，唯一索引
    email = Column(String(100), unique=True, nullable=False, index=True) #邮箱
    password = Column(String(255), nullable=False) #密码（哈希+盐值）
    username = Column(String(50), nullable=False) #管理员名称
    avatar = Column(String(255), nullable=True) #头像URL
    role = Column(String(20), default='admin')  # 角色：admin-管理员，super_admin-超级管理员
    status = Column(String(20), default='active') #状态：active-活跃，deleted-注销

class Category(Base):
    """活动分类表 - 存储活动的多级分类"""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True) #分类ID，主键
    name = Column(String(50), nullable=False) #分类名称
    parent_id = Column(Integer, default=0, index=True)  #父分类ID，0表示一级分类
    level = Column(Integer, default=1, index=True)  #层级：1-一级分类，2-二级分类
    sort_order = Column(Integer, default=0) #排序序号，数字越小越靠前

class Activity(Base):
    """活动表 - 存储活动详细信息"""
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True, autoincrement=True)  #活动ID，主键
    organizer_id = Column(Integer, ForeignKey('organizer.id', ondelete='CASCADE'), nullable=False, index=True)  #发布者ID，关联organizer表
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False, index=True)    #分类ID，关联category表
    name = Column(String(100), nullable=False)  #活动名称
    start_time = Column(DateTime, nullable=False, index=True)   #活动开始时间
    end_time = Column(DateTime, nullable=False) #活动结束时间
    campus = Column(String(20), nullable=False, index=True) #校区：良乡/中关村
    location = Column(String(100), nullable=False)  #具体地点
    max_participants = Column(Integer, nullable=False, default=1)   #人数限制，最小为1
    current_participants = Column(Integer, nullable=False, default=0)   #当前报名人数
    registration_deadline = Column(DateTime, nullable=False)    #报名截止时间
    cancel_deadline = Column(DateTime, nullable=False)  #取消报名截止时间
    description = Column(Text, nullable=False)  #活动简介/详情
    status = Column(String(20), default='draft', index=True)  # 状态：draft-草稿，pending-审核中，rejected-审核未通过，edit_pending-修改审核中，open-报名中，ongoing-进行中，ended-已结束，removed-下架
    reject_reason = Column(Text, nullable=True) #审核不通过原因
    organizer = relationship("Organizer") #关联的组织者信息
    category = relationship("Category") #关联的分类信息

class ActivityRevision(Base):
    """活动修改记录表 - 存储活动修改待审核的版本"""
    __tablename__ = 'activity_revision'
    id = Column(Integer, primary_key=True, autoincrement=True)  #修改记录ID，主键
    activity_id = Column(Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False, index=True)  #原活动ID，关联activity表
    organizer_id = Column(Integer, ForeignKey('organizer.id', ondelete='CASCADE'), nullable=False, index=True)  #发布者ID
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False, index=True)    #分类ID
    name = Column(String(100), nullable=False)  #活动名称
    start_time = Column(DateTime, nullable=False, index=True)   #活动开始时间
    end_time = Column(DateTime, nullable=False) #活动结束时间
    campus = Column(String(20), nullable=False, index=True) #校区：良乡/中关村
    location = Column(String(100), nullable=False)  #具体地点
    max_participants = Column(Integer, nullable=False, default=1)   #人数限制，最小为1
    registration_deadline = Column(DateTime, nullable=False)    #报名截止时间
    cancel_deadline = Column(DateTime, nullable=False)  #取消报名截止时间
    description = Column(Text, nullable=False)  #活动简介
    reject_reason = Column(Text, nullable=True) #修改审核不通过原因

class Registration(Base):
    """报名记录表 - 存储用户对活动的报名记录"""
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True, autoincrement=True)  #报名记录ID，主键
    activity_id = Column(Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False, index=True)    #活动ID
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)    #用户ID
    registration_time = Column(DateTime, default=func.now())    #报名时间
    status = Column(String(20), default='registered', index=True)  #状态：registered-已报名，cancelled-已取消，rejected-已拒绝，re_registered-再次报名，blocked-不允许报名
    reject_count = Column(Integer, default=0)   #被拒绝次数（针对本活动）
    last_reject_time = Column(DateTime, nullable=True)  #最后一次被拒绝时间
    reject_reason = Column(Text, nullable=True) #被拒绝原因
    slot_release_at = Column(DateTime, nullable=True)   #名额释放时间（当用户取消报名或被拒绝时，记录名额释放的时间点，用于计算冷却期）
    activity = relationship("Activity") #关联的活动信息
    user = relationship("User") #关联的用户信息
    __table_args__ = (UniqueConstraint('activity_id', 'user_id', name='uniq_activity_user'),)

class Checkin(Base):
    """签到记录表 - 存储用户签到记录"""
    __tablename__ = 'checkin'
    id = Column(Integer, primary_key=True, autoincrement=True)  #签到记录ID，主键
    activity_id = Column(Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False, index=True)    #活动ID
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)    #用户ID
    checkin_time = Column(DateTime, default=func.now())    #签到时间
    checkin_method = Column(String(20), nullable=False)  # 签到方式：code-签到码签到，manual-手动签到
    operator_id = Column(Integer, nullable=True)  # 手动签到操作人ID（组织者ID）
    activity = relationship("Activity") #关联的活动信息
    user = relationship("User") #关联的用户信息
    __table_args__ = (UniqueConstraint('activity_id', 'user_id', name='uniq_checkin_activity_user'),)

class ActivityCheckinCode(Base):
    """活动签到码表 - 存储活动的签到码"""
    __tablename__ = 'activity_checkin_code'
    id = Column(Integer, primary_key=True, autoincrement=True)  #签到码ID，主键
    activity_id = Column(Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)   #活动ID，一个活动只有一个签到码
    checkin_code = Column(String(6), nullable=False, unique=True, index=True) #6位签到码
    created_at = Column(DateTime, default=func.now())   #签到码生成时间
    activity = relationship("Activity") #关联的活动信息

class Announcement(Base):
    """系统公告表 - 存储管理员发布的系统公告"""
    __tablename__ = 'announcement'
    id = Column(Integer, primary_key=True, autoincrement=True)  #公告ID，主键
    admin_id = Column(Integer, ForeignKey('admin.id'), nullable=False, index=True)  #发布管理员ID
    title = Column(String(50), nullable=False)  #公告标题
    content = Column(Text, nullable=False)  #公告正文
    start_time = Column(DateTime, nullable=False)   #公告生效时间
    end_time = Column(DateTime, nullable=False) #公告失效时间
    created_at = Column(DateTime, default=func.now(), index=True)   #发布时间

class Notification(Base):
    """消息通知表 - 存储用户/组织者的系统通知"""
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True, autoincrement=True)  #通知ID，主键
    receiver_type = Column(String(20), nullable=False)  # 接收者类型：user-普通用户，organizer-组织者
    receiver_id = Column(Integer, nullable=False, index=True)   #接收者ID
    title = Column(String(100), nullable=False) #通知标题
    content = Column(Text, nullable=False)  #通知内容
    type = Column(String(30), nullable=False, index=True)  #通知类型：registration_result-报名结果，activity_audit_result-活动审核结果，activity_change-活动变更，violation_result-违规处理，activity_reminder-活动提醒，organizer_audit_result-组织者审核结果
    related_id = Column(Integer, nullable=True, index=True) #关联业务ID（如活动ID、报名ID等）
    is_read = Column(Boolean, default=False)    #是否已读：False-未读，True-已读
    created_at = Column(DateTime, default=func.now(), index=True)   #通知发送时间
