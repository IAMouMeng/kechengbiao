/**
 * 响应拦截
 * @param {Object} http 
 */
module.exports = (vm) => {
    uni.$u.http.interceptors.response.use((response) => {
        const data = response.data

        if (data.code == 401) {
            uni.$u.toast(data.msg);
            uni.removeStorage({
                key: 'token'
            });
            uni.reLaunch({
                url: '/pages/login/index'
            });
        }else if (data.code !== 200) {
            return Promise.reject(data)
        }

        return data.data || {}
    }, (response) => {
        return Promise.reject(response)
    })
}