<template>
	<view>
		<view v-if="loading">
			<u-loading-page :loading="loading" loading-text="数据更新中" iconSize="32" loadingColor="blue"
				fontSize="15"></u-loading-page>
		</view>
		<!-- 
		<view style="margin-top: 150px;">
			<u-empty mode="permission" text="请先登录教务系统" icon="http://cdn.uviewui.com/uview/empty/permission.png">
				<view style="margin-top: 20px;">
					<u-button size="small" type="success" @click="jumpToLoginPage" :style="{ marginTop: 10 + 'px' }">
						立即登录
					</u-button>
				</view>
			</u-empty>
    	</view> -->

		<view v-else class="course-box">
			<view>
				<u-modal :show="firstUseModel.show" @confirm="confirmModel()" :title="firstUseModel.title"
					:content="firstUseModel.content" :confirmText="firstUseModel.confirmText"></u-modal>
			</view>
			<u-row justify="space-between" gutter="10">
				<u-col span="6">
					<view class="week">
						<picker @change="changeWeek" :value="showWeek - 1" :range="weeks" range-key="name">
							<view>第 {{ showWeek }} 周</view>
						</picker>
					</view>
					<u-icon name="arrow-down-fill" color="black" size="15" top="2"></u-icon>
					<view class="desc">{{ semester }}</view>
				</u-col>
				<u-col span="6">
					<u-row justify="space-between">
						<u-col span="4" @click="updateCourses">
							<view style="float: right; margin-right: 10px"><u-icon name="reload" color="#679fff"
									size="20"></u-icon>
							</view>
						</u-col>
						<u-col span="4" @click="shareCourse">
							<view style="float: right; margin-right: 10px"><u-icon name="share" color="#679fff"
									size="20"></u-icon>
							</view>
						</u-col>
						<u-col span="4">
							<picker style="float: right; margin-right: 10px" @change="setWeek" :value="showWeek - 1"
								:range="weeks" range-key="name">
								<view><u-icon name="setting" color="#679fff" size="20"></u-icon>
								</view>
							</picker>
						</u-col>
					</u-row>
				</u-col>
			</u-row>
			<u-row justify="space-between" gutter="0">
				<u-col span="1">
					<view class="course-date">
						<view>{{ weekList.month }}</view>
						<view>月</view>
					</view>
				</u-col>
				<u-col v-for="(day, index) in ['一', '二', '三', '四', '五', '六', '日']" :key="index" span="1.5">
					<view class="course-date">
						<view :class="`${weekList.month}/${weekList.todayWeek}` == getDayOfWeekDate(index + 1) ? 'today' : ''
							">
							<view>{{ day }}</view>
							<view>{{ getDayOfWeekDate(index + 1) }}</view>
						</view>
					</view>
				</u-col>
			</u-row>
			<view style="margin-top: 5px">
				<u-row align="top" justify="space-between">
					<u-col span="1" class="course">
						<view v-for="count in 14" :key="count" class="course-number">
							{{ count + 1 }}
						</view>
					</u-col>
					<u-col span="11">
						<view class="course-grid">
							<u-row align="top" gutter="3" justify="space-between">
								<view class="bg"></view>
								<u-col v-for="(day, index) in ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun',]"
									:key="index" span="1.61">
									<view v-for="(item, itemIndex) in courseList[day]" :key="itemIndex">
										<view :class="item.isCourse ? 'course-period' : 'course-empty'" :key="itemIndex"
											:style="{ height: mathHeight(item.blocks), backgroundColor: item.isCourse ? mathColor() : 'transparent', }">
											<view v-if="item.isCourse">
												{{ item.name }}<br />@{{ item.classroom }}<br />{{
													item.teacher
												}}
											</view>
										</view>
									</view>
								</u-col>
							</u-row>
						</view>
					</u-col>
				</u-row>
			</view>
		</view>
	</view>
</template>

<style>
.course-box {
	padding: 5px 5px;
	text-align: center;
}

.course-box .week {
	font-size: 13px;
	font-weight: bold;
	float: left;
	margin-left: 10px;
}

.course-box .desc {
	font-size: 10px;
	margin-top: 5px;
	margin-left: 10px;
	color: #8f9ca2;
}

.course-grid {
	height: 980px;
	background: linear-gradient(to right,
			rgba(255, 255, 255, 1) 5px,
			transparent 1px),
		linear-gradient(to bottom, rgba(0, 0, 0, 0.2) 1px, transparent 1px);
	background-size: 10px 70px;
}

.today {
	border-radius: 5px;
	padding: 2px;
	background-color: rgba(0, 179, 255, 0.2);
	box-shadow: rgba(0, 0, 0, 0.08) 0px 4px 12px;
}

.course-date {
	font-size: 10px;
	padding: 5px;
	line-height: 15px;
	text-align: center;
}

.course-number {
	text-align: center;
	font-size: 10px;
	height: 60px;
	padding: 5px;
	line-height: 60px;
}

.course-period {
	font-size: 10px;
	margin-top: 3px;
	margin-bottom: 6px;
	padding: 5px;
	color: white;
	border-radius: 5px;
	box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px -3px,
		rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;
	word-break: break-all;
	overflow: hidden;
}

.course-empty {
	margin-top: 3px;
	margin-bottom: 6px;
	padding: 5px;
}
</style>
<script>
import { getCoursesList, updateCoursesList, getSystemInfo } from "../../common/api";

export default {
	data() {
		return {
			firstUseModel: {
				show: false,
				title: "公告",
				content: "",
				confirmText: "知道啦！",
			},
			weekList: {
				month: 0,
				todayWeek: 0,
			},
			loading: false,
			semester: "",
			todayWeek: 1,
			showWeek: 1,
			weeks: [],
			coursNew: {},
			courseList: {},
		};
	},
	async mounted() {

		const res = await getSystemInfo();

		const storageConfirm = await this.getStorage("confirm");
		const storageNotice = await this.getStorage("notice");

		if (!storageConfirm || (res.notice != "" && storageNotice != res.notice)) {
			this.firstUseModel.content = res.notice;
			this.firstUseModel.show = true;
			await this.setStorage("notice", res.notice);
		}

		const storageTodayWeek = await this.getStorage("toadyWeek");

		if (storageTodayWeek) {
			this.todayWeek = storageTodayWeek;
			this.showWeek = storageTodayWeek;
		} else {
			this.todayWeek = res.week;
			this.showWeek = res.week;
		}

		const storageCoursNew = await this.getStorage("coursNew");
		if (storageCoursNew) {
			this.coursNew = storageCoursNew;
		} else {
			await this.getCoursesList();
		}

		this.editSemester();
		this.initWeeksList(20);

		this.genCourseList(this.coursNew);
	},
	onLoad() {
		this.checkAuth();
	},
	async onShow() {
		const dateNow = new Date();

		// 更新 日期
		this.weekList.month = dateNow.getMonth() + 1;
		this.weekList.todayWeek = dateNow.getDate();

		let start = await this.getStorage("start");
		let todayWeek = await this.getStorage("toadyWeek");

		if (!start) {
			await this.setStorage(
				"start",
				new Date(
					dateNow.getFullYear(),
					dateNow.getMonth(),
					dateNow.getDate() + 1 - dateNow.getDay() || 7
				)
			);
			return;
		}

		todayWeek = todayWeek ? todayWeek : 1;

		start = new Date(start);

		const dayDiff = Math.floor((dateNow - start) / (24 * 60 * 60 * 1000));

		let newWeek = Math.trunc((dayDiff + 1) / 7) + todayWeek;

		if (newWeek > 20) {
			newWeek = 20;
		} else if (!newWeek) {
			newWeek = 1;
		}

		if (newWeek !== todayWeek) {
			this.setWeek({
				detail: {
					value: +newWeek - 1,
				},
			});

			uni.reLaunch({
				url: "/pages/class/index",
			});
		}
	},
	methods: {
		async getStorage(key) {
			try {
				const value = uni.getStorageSync(key);
				if (value) {
					return value;
				}
			} catch (error) {
				return null;
			}
		},
		async setStorage(key, data) {
			try {
				uni.setStorageSync(key, data);
			} catch (error) {
				console.log("Set key error!!!!");
			}
		},
		jumpToLoginPage() {
			uni.navigateTo({
				url: "/pages/login/index",
			});
		},
		confirmModel() {
			this.firstUseModel.show = false;
			this.setStorage("confirm", "1");
		},
		editSemester() {
			const dateNow = new Date();
			const yearNow = dateNow.getFullYear();
			const monthNow = dateNow.getMonth() + 1;
			const semester = monthNow >= 8 || monthNow == 1 ? 1 : 2;

			if (monthNow >= 2 && monthNow <= 8) {
				this.semester = `${yearNow - 1}-${yearNow} 第${semester}学期 ${this.todayWeek == this.showWeek ? "(本周)" : "(非本周)"
					}`;
			} else {
				this.semester = `${yearNow}-${yearNow + 1} 第${semester - 1}学期 ${this.todayWeek == this.showWeek ? "(本周)" : "(非本周)"
					}`;
			}
		},
		async updateCourses() {
			this.loading = true;
			this.showWeek = this.todayWeek;
			this.editSemester();
			this.initWeeksList(20);
			await this.updateCoursesList();
			this.genCourseList(await this.getCoursesList());
			this.loading = false;
		},
		shareCourse() {
			uni.showModal({
				title:
					"巴拉巴拉，这个功能还没做好（主要是还得交300认证费），需要分享请点击右上角那三个点，转发给你的盆友们就好啦！",
			});
		},
		async changeWeek(e) {
			// 切换周生成时间下一版本再更新 先研究一段时间

			this.showWeek = parseInt(e.detail.value) + 1;
			this.editSemester();
			this.genCourseList(this.coursNew);
		},
		setWeek(e) {
			const newWeek = parseInt(e.detail.value) + 1;
			if (newWeek != this.todayWeek) {
				const dateNow = new Date();
				this.setStorage(
					"start",
					new Date(
						dateNow.getFullYear(),
						dateNow.getMonth(),
						dateNow.getDate() + 1 - dateNow.getDay() || 7
					)
				);
				this.todayWeek = newWeek;
				this.initWeeksList(20);
				this.changeWeek(e);
				this.setStorage("toadyWeek", newWeek);
				uni.showToast({
					title: `当前周已切换为第 ${this.showWeek} 周`,
					icon: "none",
				});
			}
		},
		mathHeight(blocks) {
			return `${70 * blocks - 16}px`;
		},
		mathColor() {
			const randomR = Math.random() * 120;
			const randomG = Math.random() * 150;
			const randomB = Math.random() * 256;
			return `rgba(${randomR},${randomG},${randomB},0.5)`;
		},
		initWeeksList(num) {
			this.weeks = Array.from({ length: num }, (_, i) => ({
				name:
					i + 1 !== this.todayWeek ? `第 ${i + 1} 周` : `第 ${i + 1} 周 (本周)`,
			}));
		},
		getDayOfWeekDate(dayOfWeek) {
			const today = new Date();
			const todayDayOfWeek = today.getDay(); // 0表示星期日，1表示星期一，以此类推
			const diff = dayOfWeek - todayDayOfWeek;
			const targetDate = new Date(today.setDate(today.getDate() + diff));
			return `${targetDate.getMonth() + 1}/${targetDate.getDate()}`
		},
		checkIsEmpty(item) {
			// console.log(item)
			if (item.isCourse == 1) {
				if (item.info.type == "双") {
					if (this.showWeek % 2 === 0) {
						return 'course-period'
					}
					return 'none'
				}

				if (item.info.type == "单") {
					if (this.showWeek % 2 !== 0) {
						return 'course-period'
					}
					return 'none'
				}

				if (!item.info.type) {
					return 'course-period';
				}

			} else {
				return 'course-empty';
			}
			// return 'course-period'
		},
		initCourseList() {
			this.courseList = {
				Mon: [],
				Tues: [],
				Wed: [],
				Thur: [],
				Fri: [],
				Sat: [],
				Sun: [],
			};
		},
		checkAndCount(key, item) {
			if (this.showWeek < item.info.start || this.showWeek > item.info.end) {
				return true;
			}

			if (item.info.type == "双") {
				if (this.showWeek % 2 !== 0) {
					return true
				}
			}

			if (item.info.type == "单") {
				if (this.showWeek % 2 === 0) {
					return true
				}
			}
			for (const course of this.courseList[key]) {
				if (
					course.name === item.name &&
					course.info.start === item.info.start &&
					course.info.end === item.info.end &&
					course.info.day === item.info.day &&
					course.classroom === item.classroom
				) {
					course.blocks += item.info.periods.length;
					course.info.periods = course.info.periods.concat(item.info.periods);
					return true
				}
			}
			return false;
		},
		async updateCoursesList() {
			return await updateCoursesList();
		},
		async getCoursesList() {
			const res = await getCoursesList();
			if (res.length === 0) {
				uni.showToast({
					title: `暂无数据`,
					icon: "none",
				});
				return [];
			}

			this.coursNew = res.courses;
			await this.setStorage("coursNew", res.courses);

			return res.courses;
		},
		genCourseList(courseNew) {
			this.initCourseList();
			// 创建深拷贝
			const data = JSON.parse(JSON.stringify(courseNew));
			// 初步生成课表
			for (const [key, value] of Object.entries(data)) {
				value.forEach((item) => {
					if (!this.checkAndCount(key, item)) {
						item.blocks = item.info.periods.length;
						item.isCourse = 1;
						this.courseList[key].push(item);
					}
				});
			}
			// 插入间隔
			for (const key of Object.keys(this.courseList)) {
				let newList = [];
				for (let i = 0; i < this.courseList[key].length; i++) {
					const count =
						i > 0
							? this.courseList[key][i].info.periods[0] -
							this.courseList[key][i - 1].info.periods.slice(-1) -
							1
							: this.courseList[key][i].info.periods[0] - 1;
					if (count >= 2) {
						newList.push({ blocks: count, isCourse: 0 });
					}
					newList.push(this.courseList[key][i]);
				}
				this.courseList[key] = newList;
			}
		},
	},
};
</script>
