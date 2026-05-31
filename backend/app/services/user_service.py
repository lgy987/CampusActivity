import re
from werkzeug.security import generate_password_hash
from app.common.database import db_session
from app.common.errors import BusinessError
from models import User, Organizer, Admin, Checkin


class UserService:
    """用户服务"""

    ACHIEVEMENT_LEVELS = [
        {'title': '初级探索者', 'required_count': 5},
        {'title': '中级探索者', 'required_count': 20},
        {'title': '高级探索者', 'required_count': 30},
    ]

    @staticmethod
    def get_profile(role, user_id):
        """获取当前用户信息"""
        from flask import url_for
        with db_session() as session:
            if role == 'user':
                user = session.get(User, user_id)
                if not user or user.status == 'deleted':
                    raise BusinessError('用户不存在', code=404, status_code=404)

                effective_count = session.query(Checkin).filter(Checkin.user_id == user.id).count()
                achievement_title = '无'
                for level in UserService.ACHIEVEMENT_LEVELS:
                    if effective_count >= level['required_count']:
                        achievement_title = level['title']

                avatar_url = user.avatar
                if avatar_url and avatar_url.startswith('/'):
                    avatar_url = url_for('static', filename=avatar_url.replace('/static/', ''), _external=True)

                return {
                    'user_id': user.id,
                    'student_id': user.student_id,
                    'email': user.email,
                    'username': user.username,
                    'avatar': avatar_url,
                    'gender': user.gender,
                    'college': user.college,
                    'major': user.major,
                    'grade': user.grade,
                    'phone': user.phone or '',
                    'status': user.status,
                    'achievement': {
                        'title': achievement_title,
                        'effective_participation_count': effective_count
                    }
                }

            elif role == 'organizer':
                organizer = session.get(Organizer, user_id)
                if not organizer or organizer.status == 'deleted':
                    raise BusinessError('组织者不存在', code=404, status_code=404)
                
                avatar_url = organizer.avatar
                if avatar_url and avatar_url.startswith('/'):
                    avatar_url = url_for('static', filename=avatar_url.replace('/static/', ''), _external=True)

                return {
                    'organizer_id': organizer.id,
                    'email': organizer.email,
                    'org_name': organizer.org_name,
                    'avatar': avatar_url,
                    'status': organizer.status,
                    'org_proof_text': organizer.org_proof_text,
                    'org_proof_image': organizer.org_proof_image
                }

            elif role == 'admin':
                admin = session.get(Admin, user_id)
                if not admin or admin.status == 'deleted':
                    raise BusinessError('管理员不存在', code=404, status_code=404)
                
                avatar_url = admin.avatar
                if avatar_url and avatar_url.startswith('/'):
                    avatar_url = url_for('static', filename=avatar_url.replace('/static/', ''), _external=True)

                return {
                    'admin_id': admin.id,
                    'admin_no': admin.admin_no,
                    'email': admin.email,
                    'username': admin.username,
                    'avatar': avatar_url,
                    'role': admin.role
                }

            else:
                raise BusinessError('无效角色')

    @staticmethod
    def update_profile(role, user_id, data):
        """修改用户信息"""
        with db_session() as session:
            if role == 'user':
                user = session.get(User, user_id)
                if not user or user.status == 'deleted':
                    raise BusinessError('用户不存在', code=404, status_code=404)

                if 'username' in data:
                    user.username = str(data['username']).strip()
                if 'gender' in data:
                    user.gender = str(data['gender']).strip()
                if 'college' in data:
                    user.college = str(data['college']).strip()
                if 'major' in data:
                    user.major = str(data['major']).strip()
                if 'grade' in data:
                    user.grade = str(data['grade']).strip()
                if 'phone' in data:
                    phone = str(data.get('phone') or '').strip() or None
                    if phone and not re.fullmatch(r'1\d{10}', phone):
                        raise BusinessError('手机号须为11位')
                    user.phone = phone
                if 'avatar' in data:
                    user.avatar = str(data['avatar']).strip() or None

            elif role in ('organizer', 'admin'):
                model = Organizer if role == 'organizer' else Admin
                entity = session.get(model, user_id)
                if not entity or entity.status == 'deleted':
                    raise BusinessError(f'{role}不存在', code=404, status_code=404)
                if 'avatar' in data:
                    entity.avatar = str(data['avatar']).strip() or None

    @staticmethod
    def update_avatar_url(role, user_id, avatar_url):
        """更新头像URL"""
        with db_session() as session:
            if role == 'user':
                user = session.get(User, user_id)
                if not user or user.status == 'deleted':
                    raise BusinessError('用户不存在', code=404, status_code=404)
                user.avatar = avatar_url
            elif role == 'organizer':
                organizer = session.get(Organizer, user_id)
                if not organizer or organizer.status == 'deleted':
                    raise BusinessError('组织者不存在', code=404, status_code=404)
                organizer.avatar = avatar_url
            elif role == 'admin':
                admin = session.get(Admin, user_id)
                if not admin or admin.status == 'deleted':
                    raise BusinessError('管理员不存在', code=404, status_code=404)
                admin.avatar = avatar_url

    @staticmethod
    def upload_avatar(role, user_id, file):
        """上传头像文件"""
        from werkzeug.utils import secure_filename
        from flask import current_app, url_for
        from pathlib import Path
        from uuid import uuid4
        import os

        # 校验文件
        if not file or not file.filename:
            raise BusinessError('请上传头像文件')

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in ('jpg', 'jpeg', 'png'):
            raise BusinessError('头像仅支持jpg/png格式')

        # 保存文件
        upload_dir = Path(current_app.root_path) / 'static' / 'avatars'
        upload_dir.mkdir(parents=True, exist_ok=True)

        with db_session() as session:
            if role == 'user':
                entity = session.get(User, user_id)
            elif role == 'organizer':
                entity = session.get(Organizer, user_id)
            elif role == 'admin':
                entity = session.get(Admin, user_id)
            else:
                raise BusinessError('无效角色')

            if entity and entity.avatar:
                # 从 URL 中提取文件名
                old_filename = entity.avatar.split('/')[-1]
                old_file_path = upload_dir / old_filename
                if old_file_path.exists() and old_file_path.is_file():
                    os.remove(old_file_path)

        new_filename = f"{role}_{user_id}_{uuid4().hex}.{ext}"
        file.save(upload_dir / new_filename)

        avatar_url = url_for('static', filename=f'avatars/{new_filename}', _external=True)
        UserService.update_avatar_url(role, user_id, avatar_url)
        return avatar_url

    @staticmethod
    def reset_password(role, user_id, old_password, new_password):
        """重置密码"""
        from werkzeug.security import check_password_hash
        with db_session() as session:
            if role == 'user':
                entity = session.get(User, user_id)
            elif role == 'organizer':
                entity = session.get(Organizer, user_id)
            elif role == 'admin':
                entity = session.get(Admin, user_id)
            else:
                raise BusinessError('无效角色')

            if not entity or entity.status == 'deleted':
                raise BusinessError('账号不存在', code=404, status_code=404)
            
            if not check_password_hash(entity.password, old_password):
                raise BusinessError('旧密码错误', code=400, status_code=400)

            entity.password = generate_password_hash(new_password)

    @staticmethod
    def delete_account(role, user_id):
        """注销账号"""
        with db_session() as session:
            if role == 'user':
                entity = session.get(User, user_id)
            elif role == 'organizer':
                entity = session.get(Organizer, user_id)
            elif role == 'admin':
                entity = session.get(Admin, user_id)
                if entity and entity.role == 'super_admin':
                    raise BusinessError('超级管理员账号不可注销')
            else:
                raise BusinessError('无效角色')

            if not entity or entity.status == 'deleted':
                raise BusinessError('账号不存在', code=404, status_code=404)

            entity.status = 'deleted'

    # ========== 管理员用户管理 ==========

    @staticmethod
    def list_users(params):
        """获取用户列表"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        student_id = params.get('student_id', '').strip()
        college = params.get('college', '').strip()

        with db_session() as session:
            query = session.query(User).filter(User.status != 'deleted')
            if student_id:
                query = query.filter(User.student_id.contains(student_id))
            if college:
                query = query.filter(User.college.contains(college))

            total = query.count()
            rows = query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'list': [
                    {
                        'user_id': row.id,
                        'student_id': row.student_id,
                        'email': row.email,
                        'college': row.college,
                        'major': row.major,
                        'grade': row.grade,
                        'status': row.status
                    }
                    for row in rows
                ]
            }

    @staticmethod
    def get_user_detail(user_id):
        """获取单个普通用户详细信息"""
        with db_session() as session:
            user = session.get(User, user_id)
            if not user or user.status == 'deleted':
                raise BusinessError('用户不存在', code=404, status_code=404)
            return {
                'user_id': user.id,
                'student_id': user.student_id,
                'email': user.email,
                'gender': user.gender,
                'college': user.college,
                'major': user.major,
                'grade': user.grade,
                'status': user.status
            }

    @staticmethod
    def list_organizers(params):
        """获取组织者列表"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        org_name = params.get('org_name', '').strip()
        status = params.get('status', '').strip()

        with db_session() as session:
            query = session.query(Organizer).filter(Organizer.status != 'deleted')
            if status:
                query = query.filter(Organizer.status == status)
            if org_name:
                query = query.filter(Organizer.org_name.contains(org_name))

            total = query.count()
            rows = query.order_by(Organizer.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'list': [
                    {
                        'organizer_id': row.id,
                        'email': row.email,
                        'org_name': row.org_name,
                        'status': row.status
                    }
                    for row in rows
                ]
            }

    @staticmethod
    def get_organizer_detail(organizer_id):
        """获取单个组织者详细信息"""
        with db_session() as session:
            organizer = session.get(Organizer, organizer_id)
            if not organizer or organizer.status == 'deleted':
                raise BusinessError('组织者不存在', code=404, status_code=404)
            return {
                'organizer_id': organizer.id,
                'email': organizer.email,
                'org_name': organizer.org_name,
                'org_proof_text': organizer.org_proof_text,
                'org_proof_image': organizer.org_proof_image,
                'status': organizer.status,
                'avatar': organizer.avatar,
                'reject_reason': organizer.reject_reason or ''
            }

    @staticmethod
    def review_organizer(organizer_id, action, reject_reason):
        """审核组织者"""
        with db_session() as session:
            from app.services.notification_service import NotificationService
            organizer = session.get(Organizer, organizer_id)
            if not organizer or organizer.status == 'deleted':
                raise BusinessError('组织者不存在', code=404, status_code=404)

            if action == 'approve':
                organizer.status = 'approved'
                organizer.reject_reason = None
                title = "组织者审核通过"
                content = f"恭喜！您的组织者账号【{organizer.org_name}】已通过审核，现在可以创建和发布活动了。"
            else:
                organizer.status = 'rejected'
                organizer.reject_reason = reject_reason
                title = "组织者审核未通过"
                content = f"很遗憾，您的组织者账号【{organizer.org_name}】审核未通过。原因：{reject_reason}"

            NotificationService.create_notification(
            session,
            "organizer",
            organizer_id,
            title,
            content,
            "organizer_audit_result",
            organizer_id
            )
            return {'organizer_id': organizer.id, 'status': organizer.status}

    @staticmethod
    def create_admin(current_admin_id, data):
        """创建管理员（需要超级管理员权限）"""
        email = data.get('email', '').strip()
        password = data.get('password', '')
        username = data.get('username', '').strip()
        role = data.get('role', '').strip()

        if not email or not password or not username or role not in ('admin', 'super_admin'):
            raise BusinessError('参数无效', code=400)

        with db_session() as session:
            # 检查当前管理员是否为超级管理员
            current_admin = session.get(Admin, current_admin_id)
            if not current_admin or current_admin.role != 'super_admin':
                raise BusinessError('需要超级管理员权限', code=403, status_code=403)

            # 检查邮箱是否已存在
            if session.query(Admin).filter(Admin.email == email).first():
                raise BusinessError('邮箱已存在', code=400)

            # 生成管理员编号
            max_no = 0
            for (admin_no,) in session.query(Admin.admin_no).all():
                if admin_no and admin_no.isdigit():
                    max_no = max(max_no, int(admin_no))
            admin_no = f"{max_no + 1:06d}"

            admin = Admin(
                admin_no=admin_no,
                email=email,
                password=generate_password_hash(password),
                username=username,
                role=role,
                status='active'
            )
            session.add(admin)
            session.flush()

            return {'admin_id': admin.id, 'admin_no': admin.admin_no}

    @staticmethod
    def list_admins():
        """获取管理员列表"""
        with db_session() as session:
            rows = session.query(Admin).filter(Admin.status != 'deleted').order_by(Admin.id.asc()).all()
            return [
                {
                    'admin_id': row.id,
                    'admin_no': row.admin_no,
                    'email': row.email,
                    'username': row.username,
                    'role': row.role,
                    'status': row.status
                }
                for row in rows
            ]

    @staticmethod
    def delete_admin(current_admin_id, admin_id):
        """删除管理员（需要超级管理员权限）"""
        with db_session() as session:
            current_admin = session.get(Admin, current_admin_id)
            if not current_admin or current_admin.role != 'super_admin':
                raise BusinessError('需要超级管理员权限', code=403, status_code=403)

            target = session.get(Admin, admin_id)
            if not target or target.status == 'deleted':
                raise BusinessError('管理员不存在', code=404, status_code=404)
            if target.role == 'super_admin':
                raise BusinessError('超级管理员不可删除', code=400)

            target.status = 'deleted'