function getcard(focus)
{
	var card=$('#card')
	var number=card.val().trim();
	var reg=/^\d{7}|\d{10}$/;
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
$('#card').blur(function(){if($(this).val()&&getcard())displayErr('');});
$('#name').blur(function(){if($(this).val()&&getName())displayErr('');});

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
					$('#login-modal').show();
					$('#submit').text('通知失主').removeAttr('disabled');
					break;
				case 1://通知成功
					$('#submit').text('已通知');
					$('input').attr('disabled','disabled');
					$('#err').html("已经通知"+name+"["+number+"]");
					break;
				case -1://验证失败
					displayErr(result['message']);
					$('#submit').text('通知失主').removeAttr('disabled');
					break;
				case 2://广播
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
$('.login').click(function(){$('#login-modal').show();});