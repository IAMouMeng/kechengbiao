<template>
    <view class="container">
        <u-modal title="真的要退出吗？" confirmText="假的" cancelText="真的" :show="showLogoutModel" showCancelButton
            @confirm="showLogoutModel = false" @cancel="logOut" @close="close">
        </u-modal>
        <view class="ui-all">
            <view class="ui-list">
                <text>姓名</text>
                <input type="text" :value="userinfo.name" disabled />
            </view>
            <view class="ui-list">
                <text>学号</text>
                <input type="text" :value="userinfo.username" disabled />
            </view>
            <view class="ui-list">
                <text>学院</text>
                <input type="text" :value="userinfo.institute" disabled />
            </view>
            <view class="ui-list">
                <text>专业</text>
                <input type="text" :value="userinfo.profession" disabled />
            </view>
            <view class="ui-list">
                <text>班级</text>
                <input type="text" :value="userinfo.classname" disabled />
            </view>
            <button class="back" @click="back">返 回</button>
            <button class="logout" @click="showLogoutModel = true">退 出 登 录</button>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            showLogoutModel: false,
            userinfo: {}
        }
    },
    onShow: function () {
        let self = this;
        const eventChannel = this.getOpenerEventChannel();
        eventChannel.on('acceptDataFromOpenerPage', function (res) {
            self.userinfo = res.data
        })
    },
    methods: {
        back() {
            uni.navigateBack({
                delta: 1,
            })
        }, logOut() {
            uni.removeStorage({
                key: 'token'
            });
            uni.reLaunch({
                url: '/pages/login/index'
            });
        }
    }
}
</script>

<style lang="less">
.container {
    display: block;
}

.ui-all {
    padding: 20rpx 40rpx;

    .avatar {
        width: 100%;
        text-align: left;
        padding: 20rpx 0;
        border-bottom: solid 1px #f2f2f2;
        position: relative;

        .imgAvatar {
            width: 140rpx;
            height: 140rpx;
            border-radius: 50%;
            display: inline-block;
            vertical-align: middle;
            overflow: hidden;

            .iavatar {
                width: 100%;
                height: 100%;
                display: block;
            }
        }

        text {
            display: inline-block;
            vertical-align: middle;
            color: #8e8e93;
            font-size: 28rpx;
            margin-left: 40rpx;
        }

        &:after {
            content: ' ';
            width: 20rpx;
            height: 20rpx;
            border-top: solid 1px #030303;
            border-right: solid 1px #030303;
            transform: rotate(45deg);
            -ms-transform: rotate(45deg);
            /* IE 9 */
            -moz-transform: rotate(45deg);
            /* Firefox */
            -webkit-transform: rotate(45deg);
            /* Safari 和 Chrome */
            -o-transform: rotate(45deg);
            position: absolute;
            top: 85rpx;
            right: 0;
        }
    }

    .ui-list {
        width: 100%;
        text-align: left;
        padding: 20rpx 0;
        border-bottom: solid 1px #f2f2f2;
        position: relative;

        text {
            color: #4a4a4a;
            font-size: 28rpx;
            display: inline-block;
            vertical-align: middle;
            min-width: 150rpx;
        }

        input {
            color: #030303;
            font-size: 30rpx;
            display: inline-block;
            vertical-align: middle;
        }

        button {
            color: #030303;
            font-size: 30rpx;
            display: inline-block;
            vertical-align: middle;
            background: none;
            margin: 0;
            padding: 0;

            &::after {
                display: none;
            }
        }

    }

    .right:after {
        content: ' ';
        width: 20rpx;
        height: 20rpx;
        border-top: solid 1px #030303;
        border-right: solid 1px #030303;
        transform: rotate(45deg);
        -ms-transform: rotate(45deg);
        /* IE 9 */
        -moz-transform: rotate(45deg);
        /* Firefox */
        -webkit-transform: rotate(45deg);
        /* Safari 和 Chrome */
        -o-transform: rotate(45deg);
        position: absolute;
        top: 40rpx;
        right: 0;
    }

    .back {
        background: #030303;
        border: none;
        color: #ffffff;
        margin-top: 40rpx;
        font-size: 28rpx;
    }

    .logout {
        background: #ffffff;
        border: none;
        color: #000000;
        margin-top: 40rpx;
        font-size: 28rpx;
    }
}
</style>
