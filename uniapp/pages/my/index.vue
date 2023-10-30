<template>
  <view class="mypage-container">
    <u-modal title="截图并扫描下方二维码，与我联系" confirmText="关闭" @confirm="showContactModel = false" :show="showContactModel">
      <image style="width:160px;height: 160px" src="../../static/my/contact.png"></image>
    </u-modal>
    <view class="user-info-box" @click="jumpToPage('/pages/my/info')">
      <view class="avatar-box">
        <view v-if="userinfo.name">
          <image class="avatar" :src="userinfo.avatar"></image>
          <view class="avatar-text">
            <view class="name">{{ userinfo.name }}</view>
            <view class="desc">{{ userinfo.username }}</view>
          </view>
        </view>
        <view v-else>
          <u-skeleton rows="1" avatarSize="116rpx" rowsWidth="30rpx" titleWidth="100" titleHeight="50rpx" title loading
            avatar></u-skeleton>
        </view>

      </view>
      <view class="arrow-box">
      </view>
    </view>

    <!-- 常用功能 -->
    <view class="usual-ability-box">
      <view class="usual-ability-title">
        常用功能
      </view>
      <view class="usual-ability-content">
        <view class="usual-ability-item" @click="jumpToPage('/pages/my/info')">
          <image src="../../static/my/info.png"></image>
          <view class="usual-ability-item-text">
            个人信息
          </view>
        </view>
        <!-- <view class="usual-ability-item">
          <image src="../../static/my/search.png"></image>
          <view class="usual-ability-item-text">
            空教室查询
          </view>
        </view> -->
      </view>
    </view>

    <view class="usual-ability-box">
      <view class="usual-ability-title">
        信息中心
      </view>
      <view class="usual-ability-content">
        <view class="usual-ability-item" @click="jumpToPage('/pages/my/privacy')">
          <image src="../../static/my/privacy.png"></image>
          <view class="usual-ability-item-text">
            隐私协议
          </view>
        </view>
        <!-- <view class="usual-ability-item" @click="jumpToPage('/pages/my/about')">
          <image src="../../static/my/about.png"></image>
          <view class="usual-ability-item-text">
            关于我们
          </view>
        </view> -->
        <view class="usual-ability-item" @click="showContactModel = true">
          <image src="../../static/my/help.png"></image>
          <view class="usual-ability-item-text">
            帮助反馈
          </view>
        </view>
        <!-- <view class="usual-ability-item">
          <image src="../../static/my/github.png"></image>
          <view class="usual-ability-item-text">
            开放源码
          </view>
        </view> -->
      </view>
    </view>

  </view>
</template>

<script>
import { checkUserToken, getUserInfo } from '../../common/api';

export default {
  data() {
    return {
      showContactModel: false,
      userinfo: {}
    }
  },
  onLoad(){
		this.checkAuth()
	},
  onShow() {
    getUserInfo().then(res => {
      this.userinfo = res
    }).catch(res => {
      uni.$u.toast(res.msg);
    })
  },
  methods: {
    jumpToPage(path) {
      let self = this;
      uni.navigateTo({
        url: path,
        success: (res) => {
          res.eventChannel.emit('acceptDataFromOpenerPage', { data: this.userinfo })
        }
      });
    }
  }
}
</script>

<style>
.head {
  height: 140rpx;
}

/* 用户信息部分 */
.user-info-box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 300rpx;
}

.avatar-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  align-items: center;
  padding-left: 40rpx;
}

.avatar-box .avatar {
  width: 116rpx;
  height: 116rpx;
  border-radius: 116rpx;
}

.avatar-box .avatar-text {
  float: right;
  padding-left: 20rpx;
}

.avatar-text .name {
  font-size: 50rpx;
  font-weight: 500;
  color: #000002;
}

.avatar-text .desc {
  color: #a0a1a3;
  padding-top: 10rpx;
  font-size: 30rpx;
}

.arrow-box {
  width: 20rpx;
  height: 20rpx;
  border-top: 3rpx solid #a9acb3;
  border-right: 3rpx solid #a9acb3;
  transform: rotate(45deg);
  margin-right: 40rpx;
}


.usual-ability-box {
  background-color: #fff;
  padding: 0rpx 35rpx 55rpx 55rpx;
}

/* 常用功能 */
.usual-ability-title {
  margin-top: 15rpx;
  font-size: 35rpx;
  font-weight: 700;
  margin-bottom: 30rpx;
}

.usual-ability-content {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.usual-ability-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 160rpx;
  height: 160rpx;
}

.usual-ability-item image {
  width: 40rpx;
  height: 40rpx;
  margin-bottom: 25rpx;
}

.usual-ability-item-text {
  font-size: 25rpx;
  font-weight: 400;
}
</style>
