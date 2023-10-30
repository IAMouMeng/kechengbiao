import { checkUserToken } from "./api";

export default {
  methods: {
    checkAuth() {
      try {
        const value = uni.getStorageSync("token");
        if (value) {
          return checkUserToken().then(() => {
            return true;
          });
        }
      } catch (e) {
        //error
      }
    },
  },
};
