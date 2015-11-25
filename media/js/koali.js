	function isHidden(oDiv,btn){
            var vDiv = document.getElementById(oDiv);
            vDiv.style.display = (vDiv.style.display == 'none')?'block':'none';
            btn.innerHTML = (btn.innerHTML == '展开▽')?'隐藏':'展开▽'
        }
        
        function changePlan(ex_index,in_index,content){
            var summit = new XMLHttpRequest();

            summit.open("POST", "http://120.25.12.205/web_changePlan/");
            summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            var sum_data = "in_index=" + in_index + "&ex_index=" + ex_index + "&content=" + document.getElementById(content).value;
            summit.send(sum_data);
            summit.onreadystatechange = function () {
                if (summit.readyState === 4) {
                    if (summit.status === 200) {
                        var response = JSON.parse(summit.responseText);
                        if (response.status === 0) {
                            alert("保存成功！");
                        }
                        else {
                            alert("保存失败请重试！");
                        }
                    }
                }
            }
        }

	function changeTag(){
            var summit = new XMLHttpRequest();

            summit.open("POST", "http://120.25.12.205/web_changeTag/");
            summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            var sum_data = "name=" + document.getElementById('name').value + "&stage=" + document.getElementById('stage').value
                    + "&fund=" + document.getElementById('fund').value
                    + "&summary=" + document.getElementById('summary').value + "&direction1=" + document.getElementById('direction1').value
                    + "&direction2=" + document.getElementById('direction2').value;
            summit.send(sum_data);
            summit.onreadystatechange = function () {
                if (summit.readyState === 4) {
                    if (summit.status === 200) {
                        var response = JSON.parse(summit.responseText);
                        if (response.status === 0) {
                            alert('保存成功！');
                        }
                        else {
                            alert("保存失败请重试！");
                        }
                    }
                    else{
                        alert(sum_data);
                    }
                }
            }
        }

function shift(index,check){
            var summit = new XMLHttpRequest();

            summit.open("POST", "http://120.25.12.205/web_shift/");
            summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            if(document.getElementById(check).checked){
                var sum_data = "index=" + index + "&choice=yes";
            }
            else{
                var sum_data = "index=" + index + "&choice=no";
            }

            summit.send(sum_data);
        }

function changeInvestTag(){
	   var summit = new XMLHttpRequest();

            summit.open("POST", "http://120.25.12.205/web_changeInvestInfo/");
            summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            var sum_data = "company=" + document.getElementById('company').value + "&stage=" + document.getElementById('stage').value
                    + "&mail=" + document.getElementById('mail').value
                    + "&summary=" + document.getElementById('summary').value + "&direction1=" + document.getElementById('direction1').value
                    + "&direction2=" + document.getElementById('direction2').value + "&phase=" + document.getElementById('phase').value
		    + "&team" + document.getElementById('team').value + "&assembly=" + document.getElementById('assembly').value;
            summit.send(sum_data);
            summit.onreadystatechange = function () {
                if (summit.readyState === 4) {
                    if (summit.status === 200) {
                        var response = JSON.parse(summit.responseText);
                        if (response.status === 0) {
                            alert('保存成功！');
                        }
                        else {
                            alert("保存失败请重试！");
                        }
                    }
                    else{
                        alert(sum_data);
                    }
                }
            }

	}

        function uploadImg(){
           $.ajax({
                cache: true,
                type: "POST",
                url:ajaxCallUrl,
                data:$('#uploadForm').serialize(),// 你的formid
                async: false,
                error: function(request) {
                    alert("上传失败");
                },
                success: function(data) {
                var response = JSON.parse(summit.responseText);
                        if (response.status === 0) {
                            alert('上传成功！');
                        }
                        else {
                            alert("保存失败请重试！");
                        }
                }
            });
        }

function passwordOnFocus() {
var passwordInput = document.getElementById("password");
passwordInput.type = "password";
if (passwordInput.value == "请输入密码") {
passwordInput.value = "";
passwordInput.style.color = "#000";
}
}

function passwordChange(){
    password = document.getElementById("password").value;
}

function accountChange(){
    account = document.getElementById("account").value;
}

function login() {
    var account = document.getElementById("account").value;
    var summit = new XMLHttpRequest();

    summit.open("POST", "http://120.25.12.205/login_verify/");
    summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (account.indexOf("@") > 0) {
        var sum_data = "mail=" + account + "&password=" + password;
    }
    else {
       var sum_data = "phone=" + account + "&password=" + password;
        }
    summit.send(sum_data);
    summit.onreadystatechange = function () {
        if (summit.readyState === 4) {
            if (summit.status === 200) {
                var response = JSON.parse(summit.responseText);
		if (response.status==0) {
                        window.location="http://120.25.12.205/mainpage/";
                }
                else {
                    var response = JSON.parse(summit.responseText);
                    if(response.status==404)
                        {
                           alert(response.message);
                        }
                }
            }
        }
    }
}


    var phone;
    var name;
    var password;
    var nickname;
    var selForm;
    var form = document.getElementsByName("form");
    for (var i = form.length - 1; i >= 0; i--) {
        if (form[i].checked === "checked") {
            selForm = form[i].value;
        }
    }

    function passwordOnFocus() {
        var passwordInput = document.getElementById("password");
        passwordInput.type = "password";
        if (passwordInput.value == "请输入6位以上密码") {
            passwordInput.value = "";
            passwordInput.style.color = "#000";
        }
    }

    function checkpasswordOnFocus() {
        var checkpasswordInput = document.getElementById("checkpass");
        checkpasswordInput.type = "password";
        if (checkpasswordInput.value == "请再次输入密码") {
            checkpasswordInput.value = "";
            checkpasswordInput.style.color = "#000";
        }
    }

    function checkNumber() {
        //检测账号是否存在
        var request = new XMLHttpRequest();
        request.open("GET", "http://120.25.12.205/check/?phone=" + document.getElementById("phone").value);
        request.send();
        request.onreadystatechange = function() {
            if (request.readyState === 4) {
                if (request.status === 200) {
                    var result = JSON.parse(request.responseText);
                    if (result.message === "available") {
                        document.getElementById("result1").innerHTML = "该账号可以使用";
                    } else {
                        document.getElementById("result1").innerHTML = "该账号已被注册";
                    }
                }
            }
        }
    }

    function verify() {

        //发送和处理ajax
        var request = new XMLHttpRequest();
        request.open("POST", "http://120.25.12.205/verify_phone/");
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var data = "phone=" + document.getElementById("phone").value;
        request.send(data);
        request.onreadystatechange = function() {
            if (request.readyState === 4) {
                if (request.status === 200) {
                    var result = JSON.parse(request.responseText);
                    if (result.status === 0) {
                        document.getElementById("result2").innerHTML = "验证码已发送至您手机，请注意查收";
                    } else {
                        document.getElementById("result2").innerHTML = "验证码发送失败，请重新获取";
                    }
                }
            }
        }
    }

    function summit() {
        if (document.getElementById("agree").checked == true) {
            var request = new XMLHttpRequest();
            request.open("POST", "http://120.25.12.205/summit_verifying_code/");
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            var data = "phone=" + document.getElementById("phone").value + "&vcode=" + document.getElementById("vcode").value;
            request.send(data);
            request.onreadystatechange = function() {
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        var result = JSON.parse(request.responseText);
                        if (result.status === 0) {
                            var check = new XMLHttpRequest();
                            check.open("GET", "http://120.25.12.205/check/?phone=" + document.getElementById("phone").value);
                            check.send();
                            check.onreadystatechange = function() {
                                if (check.readyState === 4) {
                                    if (check.status === 200) {
                                        var result = JSON.parse(check.responseText);
                                        if (result.message === "available") {
                                            phone = document.getElementById("phone").value;
                                            var summit = new XMLHttpRequest();
                                            summit.open("POST", "http://120.25.12.205/register/");
                                            summit.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                                            var sum_data = "phone=" + phone + "&name=" + name + "&password=" + password + "&form=" + selForm;
                                            summit.send(sum_data);
                                            summit.onreadystatechange = function() {
                                                if (summit.readyState === 4) {
                                                    if (summit.status === 200) {
                                                        var response = JSON.parse(summit.responseText);

                                                        if (response.message === "success") {
								window.loaction("http://120.25.12.205/success/?phone="+phone);
                                                        } else {
                                                            alert("注册失败，请重新操作");
                                                        }
                                                    }
                                                }
                                            }

                                        } else {
                                            alert("账号已存在！");
                                        }
                                    }
                                }
                            }
                        } else {
                            alert("验证码错误！");
                        }
                    }
                }
            }

        } else {
            alert("请认真阅读并选择是否同意用户协议！");
        }

    }

    function formChange() {
        form = document.getElementsByName("form");
        for (var i = form.length - 1; i >= 0; i--) {
            if (form[i].checked === "checked") {
                selForm = form[i].value;
            }
        };
    }

    function passwordChange() {
        password = document.getElementById("password").value;
    }

    function checkpassChange() {
        checkpass = document.getElementById("checkpass").value;
        if (checkpass != password) {
            alert("两次输入不一致");
        }
    }

    function nameChange() {
        name = document.getElementById("name").value;
	}
