from django import forms

#用于防止大量不合理的用户名和密码进行攻击网站

class LoginForm(forms.Form):
    '''
    表单限制类：
        继承于django内置的表单认证模块forms.Form，
        当用户输入的内容不符合设置的要求时，django内置的form表单认证会自动阻挡，
        并且报出视图函数没有返回HttpResponse对象的异常,(该异常页面可在view视图函数中进行重新编辑)
        不会再到view的提交处理函数(LoginView.post)获取数据。
    '''
    #设置属性--用户名-必填，并且最小长度为2
    username = forms.CharField(required=True,min_length=2)
    #属性--密码必填，并且最小长度为3
    password = forms.CharField(required=True,min_length=3)

#修改密码
class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)     #password1---是表单中name属性值
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        #获取填写的密码
        pwd1 = self.cleaned_data['password1']        #[名称是表单中的name属性值]
        pwd2 = self.cleaned_data['password2']
        #判断两次的密码是否一致
        if pwd1 != pwd2:
            raise  forms.ValidationError('两次密码不一致')
        return self.cleaned_data