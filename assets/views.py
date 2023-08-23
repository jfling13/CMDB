from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from captcha.models import CaptchaStore
from . import models
from . import forms
from datetime import datetime
from assets import asset_handler
import os
from django.conf import settings
# Create your views here.


def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar_file = request.FILES['avatar']
        file_extension = os.path.splitext(avatar_file.name)[1]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = timestamp + file_extension
        relative_file_path = os.path.join(settings.MEDIA_URL, file_name)#生成可访问的公开链接
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)#生成实际的物理存储地址
        with open(file_path, "wb") as f:
            for chunk in avatar_file.chunks():
                f.write(chunk)
        user_id = request.session.get('user_id')
        user_profile = models.UserProfile.objects.get(id=user_id)
        user_profile.avatar_file = relative_file_path
        user_profile.save()
        return JsonResponse({'success': True, 'new_avatar_url': relative_file_path})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request'})

def login(request):
    if request.session.get('is_login', None):
        return redirect("/assets/index/")
    login_form = forms.UserForm(request.POST)
    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(username=username)
            except:
                message= 'user is not exsist'
                return render(request, "assets/login.html", locals())
            
            is_password_correct = check_password(password, user.password)
            if is_password_correct:
                request.session["is_login"] = True
                request.session["user_id"] = user.id
                request.session["user_name"] = user.username
                return redirect("/assets/index/")
            else:
                message= "password wrong"
                return render(request,'assets/login.html',locals())
    login_form = forms.UserForm()  
    return render(request,'assets/login.html', locals())


def index(request):
    if not request.session.get('is_login',None):  # 找到is_login就是True，没找到返回None
        return redirect('/assets/login/') 
    else:
        assets = models.Asset.objects.all()
    timestamp = datetime.now()
    user_id = request.session.get('user_id')
    user_profile = models.UserProfile.objects.get(id=user_id)
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    if not request.session.get('is_login',None):  # 找到is_login就是True，没找到返回None
        return redirect('/assets/login/')  #redirect时候使用实际url，reverse或者模板中引用url时使用命名式name
    else:
        total = models.Asset.objects.count()
        upline = models.Asset.objects.filter(status=0).count()
        offline = models.Asset.objects.filter(status=1).count()
        unknown = models.Asset.objects.filter(status=2).count()
        breakdown = models.Asset.objects.filter(status=3).count()
        backup = models.Asset.objects.filter(status=4).count()
        up_rate = round(upline/total*100)
        o_rate = round(offline/total*100)
        un_rate = round(unknown/total*100)
        bd_rate = round(breakdown/total*100)
        bu_rate = round(backup/total*100)
        server_number = models.Server.objects.count()
        networkdevice_number = models.NetworkDevice.objects.count()
        storagedevice_number = models.StorageDevice.objects.count()
        securitydevice_number = models.SecurityDevice.objects.count()
        software_number = models.Software.objects.count()
    timestamp = datetime.now()
    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    if not request.session.get('is_login',None):  # 找到is_login就是True，没找到返回None
        return redirect('/assets/login/') 
    else:
        asset = get_object_or_404(models.Asset, id=asset_id)
    
    timestamp = datetime.now()
    return render(request, 'assets/detail.html', locals())

@csrf_exempt
def report(request):
    """
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。这部分工作，请根据实际情况，自己进行。
    :param request:
    :return:
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse("资产数据已经更新！")
            else:   # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号，请检查数据！")
    return HttpResponse('200 ok')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/assets/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect('/assets/login/')