import {getSign, uploads} from "./utils.js";
import {getToken} from "./utils.js";

new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        fileName: "xxx",
        wishList: [],
        prize: [],
        tag:''
    },
    methods: {
        Upload: function (e) {
            let formData = new FormData();
            let data = JSON.stringify({
                user: "username",
                env: "dev"
            });
            formData.append('file', e.target.files[0]);
            formData.append('data', data);   // 上传文件的同时， 也可以上传其他数据
            let url = "/api/v1/upload/";
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Signatuer': getSign({"user": "username", "env": "dev"}),
                    'token': document.cookie.split(";")[2].split("=")[1]
                },
            };
            var vue = this;
            vue["fileName"] = "";
            axios.post(url, formData, config).then(function (response) {
                alert("---上传成功----");
                vue["wishList"] = response.data["data"];
            }).catch(function () {
                alert("----网络异常----")
            })
        },
        lottery: function (wishList) {
            this.tag="开始摇奖了此处是动画"
        },
        get_prize_list: function () {
            var vue = this;
            axios.get("/api/v1/prize/list/", {
                "headers": {'Signatuer': getSign({}), "Token": getToken()},
                "params": {}
            }).then(function (response) {
                alert("成功")
            }).catch(function(){
                alert("---网络异常---")
            })
        }
    }
});