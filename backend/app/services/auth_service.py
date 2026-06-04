"""
认证服务模块

提供用户注册、登录、组织者注册、文件上传等功能
"""
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from flask import current_app, url_for
from pathlib import Path
from uuid import uuid4

from app.common.errors import BusinessError
from app.common.auth import create_token
from app.common.database import db_session
from models import User, Organizer, Admin

class AuthService:
    """
    认证服务类
    
    提供用户认证相关的业务逻辑：
    - 普通用户注册
    - 组织者注册
    - 用户登录（支持三种角色）
    - 组织者证明图片上传
    """

    @staticmethod
    def register_user(data):
        """
        普通用户注册
        
        流程：
        1. 提取并验证用户输入数据
        2. 检查学号/邮箱是否已存在
        3. 创建用户记录
        4. 生成 JWT Token
        
        Args:
            data (dict): 用户注册信息，包含以下字段：
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
        
        Returns:
            dict: 包含 userId, user_id, role, token 的字典
        
        Raises:
            BusinessError: 学号格式错误、密码不一致、学号/邮箱已存在等
        """
        student_id = str(data.get('student_id', '')).strip()
        email = str(data.get('email', '')).strip()
        username = str(data.get('username', '')).strip()
        password = str(data.get('password', ''))
        confirm_password = str(data.get('confirm_password', ''))
        gender = str(data.get('gender', '')).strip()
        college = str(data.get('college', '')).strip()
        major = str(data.get('major', '')).strip()
        grade = str(data.get('grade', '')).strip()
        phone = str(data.get('phone') or '').strip() or None

        if not re.fullmatch(r'\d{10}', student_id):
            raise BusinessError('学号必须为10位数字')
        if password != confirm_password:
            raise BusinessError('两次密码不一致')
        if phone and not re.fullmatch(r'1\d{10}', phone):
            raise BusinessError('手机号须为11位')
        with db_session() as session:
            if session.query(User).filter(User.student_id == student_id).first():
                raise BusinessError('学号已存在')
            if session.query(User).filter(User.email == email).first():
                raise BusinessError('邮箱已注册')
            user = User(
                student_id=student_id,
                email=email,
                username=username,
                password=generate_password_hash(password),
                gender=gender,
                college=college,
                major=major,
                grade=grade,
                phone=phone,
                status='active'
            )
            session.add(user)
            session.flush() 
            token = create_token('user', user.id)
            return {'userId': user.id, 'user_id': user.id, 'role': 'user', 'token': token}

    @staticmethod
    def register_organizer(data):
        """
        组织者注册
        
        流程：
        1. 验证密码一致性
        2. 检查邮箱是否已存在
        3. 如果邮箱对应的账号已注销，则重新激活
        4. 否则创建新的组织者账号（状态为 pending 待审核）
        
        Args:
            data (dict): 组织者注册信息，包含以下字段：
                - email: 邮箱
                - org_name: 组织名称
                - password: 密码
                - confirm_password: 确认密码
                - org_proof_text: 组织证明文本
                - org_proof_image: 组织证明图片URL（可选）
        
        Returns:
            dict: 包含 userId, organizer_id, role, token 的字典
        
        Raises:
            BusinessError: 密码不一致、邮箱已注册等
        """
        email = str(data.get('email', '')).strip()
        org_name = str(data.get('org_name', '')).strip()
        password = str(data.get('password', ''))
        confirm_password = str(data.get('confirm_password', ''))
        org_proof_text = str(data.get('org_proof_text', '')).strip()
        org_proof_image = str(data.get('org_proof_image') or '').strip() or None
        if password != confirm_password:
            raise BusinessError('两次密码不一致')

        with db_session() as session:
            existing = session.query(Organizer).filter(Organizer.email == email).first()
        
            if existing:
                if existing.status == 'deleted':
                    existing.org_name = org_name
                    existing.password = generate_password_hash(password)
                    existing.org_proof_text = org_proof_text
                    existing.org_proof_image = org_proof_image
                    existing.status = 'pending'  
                    session.flush()
                
                    token = create_token('organizer', existing.id)
                    return {'userId': existing.id, 'organizer_id': existing.id, 'role': 'organizer', 'token': token}
                else:
                    raise BusinessError('邮箱已注册')
            organizer = Organizer(
                email=email,
                org_name=org_name,
                password=generate_password_hash(password),
                org_proof_text=org_proof_text,
                org_proof_image=org_proof_image,
                status='pending'
            )
            session.add(organizer)
            session.flush()

            token = create_token('organizer', organizer.id)
            return {'userId': organizer.id, 'organizer_id': organizer.id, 'role': 'organizer', 'token': token}

    @staticmethod
    def login(role, account, password):
        """
        用户登录（支持三种角色）
        
        流程：
        1. 根据角色查询对应的数据表
        2. 验证账号是否存在且未被注销
        3. 验证密码是否正确
        4. 生成并返回 JWT Token
        
        Args:
            role (str): 角色类型，可选值：'user' / 'organizer' / 'admin'
            account (str): 账号
                - user: 学号或邮箱
                - organizer: 邮箱
                - admin: 管理员编号
            password (str): 密码
        
        Returns:
            dict: 包含 token, user_id, role, expires_in 的字典
        
        Raises:
            BusinessError: 账号不存在、密码错误、角色类型无效
        """
        with db_session() as session:
            if role == 'user':
                entity = session.query(User).filter(
                    or_(User.student_id == account, User.email == account)
                ).first()
                if not entity or entity.status == 'deleted':
                    raise BusinessError('该账号不存在', code=401)
                if not check_password_hash(entity.password, password):
                    raise BusinessError('账号或密码错误', code=401)
                return {'token': create_token('user', entity.id), 'user_id': entity.id, 'role': 'user', 'expires_in': 7200} 
            elif role == 'organizer':
                entity = session.query(Organizer).filter(Organizer.email == account).first()
                if not entity or entity.status == 'deleted':
                    raise BusinessError('该账号不存在', code=401)
                if not check_password_hash(entity.password, password):
                    raise BusinessError('账号或密码错误', code=401)
                return {'token': create_token('organizer', entity.id), 'user_id': entity.id, 'role': 'organizer', 'expires_in': 7200}
            elif role == 'admin':
                entity = session.query(Admin).filter(Admin.admin_no == account).first()
                if not entity or entity.status == 'deleted':
                    raise BusinessError('该账号不存在', code=401)
                if not check_password_hash(entity.password, password):
                    raise BusinessError('账号或密码错误', code=401)
                return {'token': create_token('admin', entity.id), 'user_id': entity.id, 'role': 'admin', 'expires_in': 7200}
            else:
                raise BusinessError('角色类型无效')
            
    @staticmethod
    def upload_organizer_proof(file):
        """
        上传组织者证明图片
        
        用于组织者注册时上传资质证明文件。
        此接口无需认证，因为用户尚未注册。
        
        流程：
        1. 校验文件是否存在
        2. 校验文件格式（仅支持 jpg/png）
        3. 校验文件大小（不超过 2MB）
        4. 保存文件到临时目录
        5. 返回文件访问 URL
        
        Args:
            file: 上传的图片文件（Flask file 对象）
        
        Returns:
            dict: 包含 image_url 的字典
        
        Raises:
            BusinessError: 文件格式错误、大小超限等
        """
        if not file or not file.filename:
            raise BusinessError('请上传图片文件', code=400)
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in ('jpg', 'jpeg', 'png'):
            raise BusinessError('图片仅支持jpg/png格式', code=400)
        
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > 2 * 1024 * 1024:
            raise BusinessError('图片大小不能超过2MB', code=400)
        
        upload_dir = Path(current_app.root_path) / 'static' / 'temp_proofs'
        upload_dir.mkdir(parents=True, exist_ok=True)
        new_filename = f"temp_{uuid4().hex}.{ext}"
        file.save(upload_dir / new_filename)
        
        image_url = url_for('static', filename=f'temp_proofs/{new_filename}', _external=True)
        
        return {'image_url': image_url}