/**
 * 请求拦截
 * @param {Object} http
 */
module.exports = (vm) => {
    uni.$u.http.interceptors.request.use((config) => {

        config.data = config.data || {}

        if (config.custom?.auth) {
            const value = uni.getStorageSync('token');
            if (value) {
                Object.assign(config.header, { "Access-Token": value })
            } else {
                uni.$u.toast("登录信息失效，请重新登录");
                uni.removeStorage({
                    key: 'token'
                });
                uni.reLaunch({
                    url: '/pages/login/index'
                });
            }
        }

        return config
    }, (config) => // 可使用async await 做异步操作
        Promise.reject(config))
}
