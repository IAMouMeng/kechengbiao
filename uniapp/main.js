import Vue from 'vue'
import App from './App'


// 引入全局uView
import uView from '@/uni_modules/uview-ui'

Vue.config.productionTip = false

App.mpType = 'app'

Vue.use(uView)


import mixin from "@/common/mixin";
Vue.mixin(mixin)

// #ifdef MP
// 引入uView对小程序分享的mixin封装
const mpShare = require('@/uni_modules/uview-ui/libs/mixin/mpShare.js')
Vue.mixin(mpShare)
// #endif

const app = new Vue({
    ...App
})

// 引入请求封装
require('./util/request/index')(app)

app.$mount()

console.log("Author: Mr.Sun\nMail: iamoumeng@aliyun.com")
