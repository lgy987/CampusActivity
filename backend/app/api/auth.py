from flask import Blueprint, request
from app.api.deps import get_json_data
from app.common.response import success
from app.common.errors import BusinessError
from app.services.auth_service import AuthService 

bp = Blueprint('auth', __name__)


@bp.post('/register/user')
def register_user():
    """普通用户注册"""
    data = get_json_data()
    try:
        result = AuthService.register_user(data)
        return success(result, message='注册成功，已自动登录')
    except BusinessError as e:
        return e.to_response()


@bp.post('/register/organizer')
def register_organizer():
    """组织者注册"""
    data = get_json_data()
    try:
        result = AuthService.register_organizer(data)
        return success(result, message='注册成功，自动登录，请等待管理员审核')
    except BusinessError as e:
        return e.to_response()


@bp.post('/login')
def login():
    """用户登录"""
    data = get_json_data()
    required_fields = ['role', 'account', 'password']
    for field in required_fields:
        if not str(data.get(field, '')).strip():
            return BusinessError(f'缺少必填字段：{field}', code=400).to_response()

    try:
        result = AuthService.login(
            role=str(data['role']).strip(),
            account=str(data['account']).strip(),
            password=str(data['password'])
        )
        return success(result, message='登录成功')
    except BusinessError as e:
        return e.to_response()


@bp.post('/logout')
def logout():
    """退出登录"""
    return success(None, message='退出成功')

@bp.post('/upload-organizer-proof')
def upload_organizer_proof():
    """上传组织者证明图片（无需认证，用于注册时上传）"""
    from werkzeug.utils import secure_filename
    from flask import current_app, url_for
    from pathlib import Path
    from uuid import uuid4
    
    print("=== upload_organizer_proof 被调用 ===")
    
    if 'proof_image' not in request.files:
        raise BusinessError('请上传图片文件', code=400)
    
    file = request.files['proof_image']
    if not file or not file.filename:
        raise BusinessError('请选择图片文件', code=400)
    
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
    
    return success({'image_url': image_url}, message='图片上传成功')