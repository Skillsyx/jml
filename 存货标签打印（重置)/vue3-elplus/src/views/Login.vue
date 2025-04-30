<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <h2 class="login-title">存货标签打印系统</h2>
      <el-form :model="loginForm" label-position="top" class="login-form">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" placeholder="请输入密码" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleLogin" block>登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      // 默认填入admin，提示用户账号和密码均为admin
      loginForm: {
        username: 'admin',
        password: 'admin'
      }
    }
  },
  methods: {
    handleLogin() {
      if (this.loginForm.username === 'admin' && this.loginForm.password === 'admin') {
        // 登录成功，跳转到使用界面
        localStorage.setItem('isAuthenticated', true)
        this.$router.push('/usage')
        // this.$router.push('/usage')
      } else {
        // 登录失败，利用 Element Plus 消息提示（确保Element Plus已全局注册）
        this.$message.error('用户名或密码错误')
      }
    }
  }
}
</script>

<style scoped>
/* 确保外层容器铺满整个屏幕，并设置为白色背景 */
.login-container {
  width: 100vw;
  height: 100vh;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 卡片样式：固定宽度和内边距 */
.login-card {
  width: 320px;
  padding: 20px;
}

/* 标题居中，添加适当的间距 */
.login-title {
  text-align: center;
  margin-bottom: 20px;
}

/* 按钮全宽显示 */
.login-btn {
  width: 100%;
}
</style>
