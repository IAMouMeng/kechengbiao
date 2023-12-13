<template>
	<view>
		<isszz-captcha :options="captchaOptions" v-if="captchaShow" @close="captchaShow = false"
			@success="captchaSuccess"></isszz-captcha>
		<view class="t-login">
			<image class="img-a" src="@/static/images/login/2.png"></image>
			<image class="img-b" src="@/static/images/login/3.png"></image>
			<view class="t-b">{{ title }}</view>
			<form class="cl">
				<view class="t-a">
					<image src="@/static/images/login/student.png"></image>
					<input type="number" name="username" placeholder="请输入教务系统账号" maxlength="10" v-model="username" />
				</view>
				<view class="t-a">
					<image src="@/static/images/login/yz.png"></image>
					<input type="password" name="password" maxlength="32" placeholder="请输入教务系统密码" v-model="password" />
				</view>
				<button @tap="login()">登 录</button>
			</form>
		</view>
	</view>
</template>
<script>
import { userLogin } from '../../common/api'

export default {
	data() {
		return {
			title: '教务系统登录',
			username: '',
			password: '',
			captchaShow: false,
			// 验证码配置项
			captchaOptions: {
				theme: '#07f',
				title: '安全验证',
				desc: '拖动滑块，使图片角度为正',
				successClose: 1000,
				timerProgressBar: true,
				timerProgressBarColor: 'rgba(0, 0, 0, 0.2)',
				url: {
					info: 'https://captcha.lnsec.cn/captcha/rotate',
					check: 'https://captcha.lnsec.cn/captcha/verify',
					img: 'https://captcha.lnsec.cn/captcha/img',
				},
			},
		};
	},
	onShow() {
		const self = this
		uni.removeStorage({
			key: 'coursNew',
		});
		uni.removeStorage({
			key : 'token'
		});
		uni.removeStorage({
			key : 'year'
		});
		uni.getStorage({
            key: 'username',
            success: function (res) {
                self.username = res.data
            }
        });
        uni.getStorage({
            key: 'password',
            success: function (res) {
                self.password = res.data
            }
        });
	},
	methods: {
		login() {
			if (!this.password || !this.username) {
				uni.$u.toast("请输入用户名和密码");
			} else if (this.username.length != 10) {
				uni.$u.toast("教务系统用户名有误");
			} else {
				this.openCaptcha();
			}
		},
		openCaptcha() {
			this.captchaShow = true
		},
		jumpToIndexPage() {
			uni.reLaunch({
				url: '/pages/class/index'
			});
		},
		captchaSuccess(token) {
			uni.showLoading({
				title: "正在登陆",
				mask: true
			})
			uni.removeStorage({
				key: 'token'
			});

			let self = this;
			userLogin({
				"username": this.username,
				"password": this.password,
				"token": token
			}).then(res => {
				uni.setStorage({
					key: 'username',
					data: this.username,
				});
				uni.setStorage({
					key: 'password',
					data: this.password,
				});
				uni.setStorage({
					key: 'year',
					data: this.username.slice(0, 4),
				});
				uni.setStorage({
					key: 'token',
					data: res.token,
					success: function () {
						self.jumpToIndexPage()
						self.$u.toast("登陆成功");
					}
				});
			}).catch(res => {
				self.$u.toast(res.msg);
			})

		}
	}
};
</script>
<style>
.content {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

.logo {
	height: 200rpx;
	width: 200rpx;
	margin-top: 200rpx;
	margin-left: auto;
	margin-right: auto;
	margin-bottom: 50rpx;
}

.text-area {
	display: flex;
	justify-content: center;
}

.title {
	font-size: 36rpx;
	color: #8f8f94;
}


.img-a {
	position: absolute;
	width: 100%;
	top: -280rpx;
	right: -100rpx;
}

.img-b {
	position: absolute;
	width: 50%;
	bottom: 0;
	left: -50rpx;
	margin-bottom: -200rpx;
}

.t-login {
	width: 600rpx;
	margin: 0 auto;
	font-size: 28rpx;
	color: #000;
}

.t-login button {
	font-size: 28rpx;
	background: #5677fc;
	color: #fff;
	height: 90rpx;
	line-height: 90rpx;
	border-radius: 50rpx;
	box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.t-login input {
	padding: 0 20rpx 0 120rpx;
	height: 90rpx;
	line-height: 90rpx;
	margin-bottom: 50rpx;
	background: #f8f7fc;
	border: 1px solid #e9e9e9;
	font-size: 28rpx;
	border-radius: 50rpx;
}

.t-login .t-a {
	position: relative;
}

.t-login .t-a image {
	width: 40rpx;
	height: 40rpx;
	position: absolute;
	left: 40rpx;
	top: 28rpx;
	border-right: 2rpx solid #dedede;
	padding-right: 20rpx;
}

.t-login .t-b {
	text-align: left;
	font-size: 46rpx;
	color: #000;
	padding: 300rpx 0 120rpx 0;
	font-weight: bold;
}

.t-login .uni-input-placeholder {
	color: #000;
}

.cl {
	zoom: 1;
}

.cl:after {
	clear: both;
	display: block;
	visibility: hidden;
	height: 0;
	content: '\20';
}
</style>
