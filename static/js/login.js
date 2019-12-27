import {getSign} from "./utils.js";
new Vue({
    delimiters: ['${', '}'],
    el: '#app',
    data: {
        account: '',
        pwd: ''
    },
    methods: {
        logIn: function () {
            var VueThis = this;
            var body = {"account": VueThis.account, "pwd": VueThis.pwd};
            console.log(this.account);
            axios.post("/api/v1/login/", body, {
                "headers": {'Signatuer': getSign(body)},
                "params": {}
            }).then(function (res) {
                var token = document.cookie.split(";")[2].split("=")[1];
                window.location.href ='/?token='+token
            })
        }
    }
});