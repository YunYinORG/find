function getcard(focus)
{
	var card=$('#card')
	var number=card.val().trim();
	var reg=/^(\d{7}|\d{10})$/;
	if(!reg.test(number))
	{
		displayErr("校园卡号格式不对哦！");
		if (focus) card.focus()
		return false;
	}else{
		return number;
	}
}
function getName(focus)
{
	var input=$('#name')
	var name=input.val().trim();
    var reg=/^[\u4E00-\u9FA5]{2,5}(·[\u4E00-\u9FA5]{2,8})?$/;
	if(!reg.test(name))
	{
		displayErr("请填写正确的姓名哦!");
		if (focus) input.focus()
		return false;
	}else{
		return name;
	}
}
function displayErr(msg){$('#err').html(msg);}
function ModalErr(msg){ if (msg){$('#err-modal').html(msg).show(200);}else{$('#err-modal').html('').hide();}}
function showModal(name){$('#main').hide();$('.modal').hide();$('#'+name+'-modal').show()};
$('#card').blur(function(){if($(this).val()&&getcard())displayErr('');});
$('#name').blur(function(){if($(this).val()&&getName())displayErr('');});
$('.close').click(function(){$('.modal').hide();$("#main").show();$('#err-modal').hide()});
$('#err-modal').click(function(){$(this).hide(200)});
$('.login').click(function(){showModal('login');});
//临时注册
$('#opne_phone_login').click(function(){
	$('#sms-code').hide();
	showModal('phone');
	$('#phone-msg').html('非学生可使用手机号作为临时账号(<a href="http://api.yunyin.org" target="_blank">该校学生请使用云印校园账号登录</a>)，为了防止滥用和骚扰，只允许发送一次信息(直到确认找回)');
	$('#user').show();
});
//验证通知
$('#submit').click(function(){
	var number,name;
	if((number=getcard(true))&&(name=getName(true)))
	{
		displayErr('');
		$(this).text('正在通知...').attr('disabled','disabled');
		var data={number:number,name:name};
		$.post('/notify/', data, function(result)
		{
			switch(result.status)
			{
				case 0://未登录
					showModal('login');
					$('#submit').text('通知失主').removeAttr('disabled');
					break;
				case 1://通知成功
					$('#submit').text('已通知');
					$('input').attr('disabled','disabled');
					$('#err').html("已经通知"+name+"["+number+"]");
					break;
				case -2://需要绑定手机
					$('#sms-code').hide();
					$('#user').hide();
					showModal('phone');
					$('#phone-msg').text('发送消息前，需要验证您的手机');
					break;
				case -1://验证失败
					displayErr(result['message']);
					$('#submit').text('通知失主').removeAttr('disabled');
					break;

				case 2://广播
					school=result.message;
					if (school>0){
						$('#school-select').hide();
					}
					showModal('msg');
					break;
				default:
					if (result['message'])
					{
						displayErr(result['message']);
					}
					$('#submit').text('通知失主').removeAttr('disabled');
					break;
			}
		})
	}
});

//提交手机号
$('#submit-phone').click(function(){
	var phone=$('#phone').val();
	if(!/^1[34578]\d{9}$/.test(phone))
	{
		ModalErr('手机号格式有误，检查一下')
		$('#phone').focus();
		return false;
	}
	var data={'phone':phone};
	var nameInput=$('#user')
	var name=nameInput.val();
	if(nameInput.css('display')!='none')
	{
		if(!/^[\u4E00-\u9FA5]{2,4}/.test(name))
		{
			ModalErr('请填写正确的中文姓名哦!');
			nameInput.focus();
			return false;
		}else{
			data['name']=name
		}
	}
	ModalErr('');
	$(this).attr('disabled','disabled');
	$.post('/phone/',data,function(result){
		if(result.status==1)
		{
			$('#sms-code').show();
			setTimeout(function(){
				$("#submit-phone").removeAttr('disabled');
			},1000)
		}else{
			ModalErr(result.message);
			$("#submit-phone").removeAttr('disabled');
		}
	});
});
//提交验证码
$('#submit-code').click(function(){
	var code=$('#code').val()
	if(!/^\d{4,6}$/.test(code))
	{
		ModalErr('验证码是4到6位数字哦！');
		$('#code').empty().focus();
		return false;
	}
	$(this).attr('disabled','disabled');
	ModalErr('');
	$.post('/phone/code',{'code':code},function(result){
		if(result.status==1)
		{
			$('.close').click();
			$('.first').html('<h3>已登录</h3><p>'+result.message+'</p>');
		}else{
			ModalErr(result.message);
			if(result.status==-1)
			{
				$('#sms-code').hide();
			}else{
				$('#code').empty().focus();
			}
		}
		$('#submit-code').removeAttr('disabled');
	});

});

//广播消息
$('#submit-msg').click(function(){
$(this).attr('disabled','disabled');
var msg=$('#msg').val();
	if(msg.length>16)
	{
		ModalErr('字数超过16个了！')
		$('#msg').focus();
		return false;
	}
	var data={'msg':msg};
	var select=$('#sch')
	if(select.css('display')!='none')
	{
		var school=select.val();
		data['sch']=school;
	}
	$.post('/notify/broadcast',data,function(result){
		alert(result);
		$('#submit-msg').removeAttr('disabled');
	});
});