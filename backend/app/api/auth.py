"""
认证 API 路由模块

提供用户认证相关的 API 接口：
- 普通用户注册
- 组织者注册
- 用户登录（支持三种角色）
- 用户退出
- 组织者证明图片上传
"""
from flask import Blueprint, request
from app.api.deps import get_json_data
from app.common.response import success
from app.common.errors import BusinessError
from app.services.auth_service import AuthService 

bp = Blueprint('Auth', __name__)


@bp.post('/register/user')
def register_user():
    """
    普通用户注册
    
    学生使用学号、邮箱等信息注册普通用户账号
    
    Request Body:
        - student_id (str): 学号（10位数字）
        - email (str): 邮箱地址
        - username (str): 用户名/昵称
        - password (str): 密码
        - confirm_password (str): 确认密码
        - gender (str): 性别（男/女）
        - college (str): 学院
        - major (str): 专业
        - grade (str): 年级
        - phone (str, optional): 手机号
    
    Returns:
        - userId: 用户ID
        - user_id: 用户ID（兼容字段）
        - role: 角色（user）
        - token: JWT Token
    
    Raises:
        400: 参数错误、学号格式错误、学号/邮箱已存在
    """
    data = get_json_data()
    try:
        result = AuthService.register_user(data)
        return success(result, message='注册成功，已自动登录')
    except BusinessError as e:
        return e.to_response()


@bp.post('/register/organizer')
def register_organizer():
    """
    组织者注册
    
    社团或组织使用邮箱注册组织者账号，需提供组织证明
    注册后状态为 pending（待审核），需管理员审核通过后才能发布活动
    
    Request Body:
        - email (str): 邮箱地址（登录凭证）
        - org_name (str): 组织名称
        - password (str): 密码
        - confirm_password (str): 确认密码
        - org_proof_text (str): 组织证明文本
        - org_proof_image (str, optional): 组织证明图片URL
    
    Returns:
        - userId: 组织者ID
        - organizer_id: 组织者ID
        - role: 角色（organizer）
        - token: JWT Token
    
    Raises:
        400: 参数错误、密码不一致、邮箱已注册
    """
    data = get_json_data()
    try:
        result = AuthService.register_organizer(data)
        return success(result, message='注册成功，自动登录，请等待管理员审核')
    except BusinessError as e:
        return e.to_response()


@bp.post('/login')
def login():
    """
    用户登录
    
    支持三种角色登录：
    - 普通用户：使用学号或邮箱登录
    - 组织者：使用邮箱登录
    - 管理员：使用管理员编号登录
    
    Request Body:
        - role (str): 角色类型（user/organizer/admin）
        - account (str): 账号
            - user: 学号或邮箱
            - organizer: 邮箱
            - admin: 管理员编号
        - password (str): 密码
    
    Returns:
        - token: JWT Token
        - user_id: 用户ID
        - role: 用户角色
        - expires_in: Token 有效期（秒，7200秒=2小时）
    
    Raises:
        401: 账号不存在或密码错误
        400: 缺少必填字段
    """
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
    """
    用户退出登录
    
    客户端清除本地存储的 Token 即可，
    服务端无状态，不需要额外处理
    
    Returns:
        message: 退出成功
    """
    return success(None, message='退出成功')

@bp.post('/upload-organizer-proof')
def upload_organizer_proof():
    """
    上传组织者证明图片
    
    用于组织者注册时上传资质证明文件
    此接口无需认证，因为用户尚未注册
    
    Request:
        - proof_image (file): 图片文件（支持 jpg/png，最大2MB）
    
    Returns:
        - image_url: 图片访问URL
    
    Raises:
        400: 未上传文件、文件格式错误、文件大小超限
    """
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