function getSign(body) {
    var keys = Object.keys(body).sort();
    var keyStr = keys.join('');
    var valuesStr = "";
    for (var i in keys) {
        valuesStr += body[keys[i]];
    }
    var _str = keyStr + valuesStr;
    var sign = md5(_str);
    sign = md5("NCSS-SASH-" + sign);
    return sign
}

export {getSign}


// 上传文件
function uploads(e) {
    {
        console.log("111111111")
        let formData = new FormData();
        let data = JSON.stringify({
            user: "username",
            env: "dev"
        });
        formData.append('file', e.target.files[0]);
        formData.append('data', data);   // 上传文件的同时， 也可以上传其他数据
        let url = "/api/v1/upload/";
        let config = {
            headers: {'Content-Type': 'multipart/form-data'}
        };
        axios.post(url, formData, config).then(function (res) {
            console.log(res.data);
        });
    }
}

export {uploads}

//获取Token
function getToken() {
    return document.cookie.split(";")[2].split("=")[1];
}

export {getToken}