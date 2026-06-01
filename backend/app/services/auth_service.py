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
    """认证服务"""

    @staticmethod
    def register_user(data):
        """普通用户注册"""
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

        # 校验
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
        """组织者注册"""
        email = str(data.get('email', '')).strip()
        org_name = str(data.get('org_name', '')).strip()
        password = str(data.get('password', ''))
        confirm_password = str(data.get('confirm_password', ''))
        org_proof_text = str(data.get('org_proof_text', '')).strip()
        org_proof_image = str(data.get('org_proof_image') or '').strip() or None

        if password != confirm_password:
            raise BusinessError('两次密码不一致')

        with db_session() as session:
             # 查找是否存在该邮箱的组织者（包括已注销的）
            existing = session.query(Organizer).filter(Organizer.email == email).first()
        
            if existing:
                # 如果账号已注销，允许重新激活
                if existing.status == 'deleted':
                    # 更新账号信息，重新激活
                    existing.org_name = org_name
                    existing.password = generate_password_hash(password)
                    existing.org_proof_text = org_proof_text
                    existing.org_proof_image = org_proof_image
                    existing.status = 'pending'  # 重新审核
                    session.flush()
                
                    token = create_token('organizer', existing.id)
                    return {'userId': existing.id, 'organizer_id': existing.id, 'role': 'organizer', 'token': token}
                else:
                    # 账号存在且未注销（pending/approved/rejected），不能重复注册
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
        """用户登录"""
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
        """上传组织者证明图片（无需认证，用于注册时上传）"""
        # 校验文件
        if not file or not file.filename:
            raise BusinessError('请上传图片文件', code=400)
        
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in ('jpg', 'jpeg', 'png'):
            raise BusinessError('图片仅支持jpg/png格式', code=400)
        
        # 校验文件大小（2MB）
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > 2 * 1024 * 1024:
            raise BusinessError('图片大小不能超过2MB', code=400)
        
        # 保存文件
        upload_dir = Path(current_app.root_path) / 'static' / 'temp_proofs'
        upload_dir.mkdir(parents=True, exist_ok=True)
        new_filename = f"temp_{uuid4().hex}.{ext}"
        file.save(upload_dir / new_filename)
        
        # 返回图片URL
        image_url = url_for('static', filename=f'temp_proofs/{new_filename}', _external=True)
        
        return {'image_url': image_url}