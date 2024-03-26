const { http } = uni.$u

// 用户登录
export const userLogin = (params) => http.post('/api/user/login', params)
// 校验Token状态
export const checkUserToken = () => http.get('/api/user/check', { custom: { auth: 1 } })
// 获取用户信息
export const getUserInfo = () => http.get('/api/user/info', { custom: { auth: 1 } })
// 获取配置信息
export const getSystemInfo = () => http.get('/api/system/config', { custom: { auth: 1 } })
// 更新成绩数据
export const updateExamsList = (year,xq) => http.get(`/api/edu/updateExamsList?year=${year}&xq=${xq}` , { custom: { auth: 1 } })
// 获取成绩数据
export const getExamsList = (year,xq) => http.get(`/api/edu/getExamsList?year=${year}&xq=${xq}` , { custom: { auth: 1 } })
// 更新课表数据
export const updateCoursesList = () => http.get(`/api/edu/updateCoursesList` , { custom: { auth: 1 } })
// 获取课表数据
export const getCoursesList = () => http.get(`/api/edu/getCoursesList` , { custom: { auth: 1 } })


