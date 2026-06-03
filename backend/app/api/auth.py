from flask import Blueprint, request
from app.api.deps import get_json_data
from app.common.response import success
from app.common.errors import BusinessError
from app.services.auth_service import AuthService 

bp = Blueprint('Auth', __name__)


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
    if 'proof_image' not in request.files:
        raise BusinessError('请上传图片文件', code=400)
    
    file = request.files['proof_image']
    if not file or not file.filename:
        raise BusinessError('请选择图片文件', code=400)
    
    try:
        result = AuthService.upload_organizer_proof(file)
        return success(result, message='图片上传成功')
    except BusinessError as e:
        return e.to_response()