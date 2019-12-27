import {getSign, getToken} from "./utils.js";

var vue = new Vue({
    delimiters: ['${', '}'],
    el: '#lottery',
    data: {
        fileName: '',
        participates: this.GetParticipates(),
        personnel: "",
        tag: false
    },
    methods: {
        GetPersonnel: function (participates) {
            this.tag=!this.tag;
            while (this.tag) {
                this.personnel = ''
            }
        },
        GetParticipates: function () {
            var vueThis = this;
            params = {"file_name": this.fileName};
            axios.get("/api/v1/wish/list/", {
                "headers": {'Signatuer': getSign(params), "Token": getToken()},
                "params": params
            }).then(function (res) {
                participates = res.data["data"];
                vueThis.GetPersonnel(participates)
            })
        }
    }
});


