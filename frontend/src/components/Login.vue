<template>
  <div class="auth-page">
    <div class="auth-container" :class="{ 'register-mode': isRegister }">
      <div class="tabs">
        <button 
          class="tab" 
          :class="{ active: !isRegister }"
          @click="isRegister = false"
        >
          Вход
        </button>
        <button 
          class="tab" 
          :class="{ active: isRegister }"
          @click="isRegister = true"
        >
          Регистрация
        </button>
      </div>

      <transition name="fade" mode="out-in">
        <form 
          v-if="!isRegister" 
          key="login" 
          class="auth-form"
          @submit.prevent="handleLogin"
        >
          <h2>Вход в аккаунт</h2>
          
          <div class="form-group">
            <label for="login-email">Email</label>
            <input 
              id="login-email" 
              v-model="loginForm.email" 
              type="email" 
              required
              placeholder="Введите ваш email"
            >
          </div>

          <div class="form-group">
            <label for="login-password">Пароль</label>
            <input 
              id="login-password" 
              v-model="loginForm.password" 
              type="password" 
              required
              placeholder="Введите пароль"
            >
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Войти</span>
            <span v-else class="loader"></span>
          </button>

          <div v-if="loginError" class="error-message">
            {{ loginError }}
          </div>
        </form>

        <form 
          v-else 
          key="register" 
          class="auth-form"
          @submit.prevent="handleRegister"
        >
          <h2>Создать аккаунт</h2>
          
          <div class="form-group">
            <label for="register-name">Имя</label>
            <input 
              id="register-name" 
              v-model="registerForm.name" 
              type="text" 
              required
              placeholder="Введите ваше имя"
            >
          </div>

          <div class="form-group">
            <label for="register-email">Email</label>
            <input 
              id="register-email" 
              v-model="registerForm.email" 
              type="email" 
              required
              placeholder="Введите ваш email"
            >
          </div>

          <div class="form-group">
            <label for="register-password">Пароль</label>
            <input 
              id="register-password" 
              v-model="registerForm.password" 
              type="password" 
              required
              placeholder="Придумайте пароль"
              minlength="6"
            >
          </div>

          <div class="form-group">
            <label for="register-confirm">Подтвердите пароль</label>
            <input 
              id="register-confirm" 
              v-model="registerForm.confirmPassword" 
              type="password" 
              required
              placeholder="Повторите пароль"
            >
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Зарегистрироваться</span>
            <span v-else class="loader"></span>
          </button>

          <div v-if="registerError" class="error-message">
            {{ registerError }}
          </div>
          <div v-if="registerSuccess" class="success-message">
            Регистрация прошла успешно! Теперь вы можете войти.
          </div>
        </form>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      isRegister: false,
      loading: false,
      loginForm: {
        email: '',
        password: ''
      },
      registerForm: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      loginError: '',
      registerError: '',
      registerSuccess: false
    }
  },
  methods: {
    async handleLogin() {
      this.loginError = '';
      this.loading = true;
      
      if (!this.loginForm.email || !this.loginForm.password) {
        this.loginError = 'Пожалуйста, заполните все поля';
        this.loading = false;
        return;
      }

      try {
        
        // const response = await this.mockLoginRequest();
        const params = new URLSearchParams();
        params.append('username', this.loginForm.email);
        params.append('password', this.loginForm.password);

        const response = await axios.post('https://92.100.127.109/auth/login', 
          params, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          });
        const token = response.data.access_token; // щас добавил
        document.cookie = `access_token=${token}; path=/; max-age=${60 * 60 * 24 * 7}; Secure; SameSite=Lax`; // щас добавил
        localStorage.setItem('access_token', response.data.access_token)

        
        this.$router.push('/dashboard');

      } catch (error) {
        this.loginError = 'Произошла ошибка при входе';
        console.error('Login error:', error);
      } finally {
        this.loading = false;
      }
    },

    async handleRegister() {
      this.registerError = '';
      this.registerSuccess = false;
      this.loading = true;

      // Валидация
      if (!this.registerForm.name || !this.registerForm.email || 
          !this.registerForm.password || !this.registerForm.confirmPassword) {
        this.registerError = 'Пожалуйста, заполните все поля';
        this.loading = false;
        return;
      }

      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.registerError = 'Пароли не совпадают';
        this.loading = false;
        return;
      }

      if (this.registerForm.password.length < 6) {
        this.registerError = 'Пароль должен быть не менее 6 символов';
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post('https://92.100.127.109/auth/register', 
          {
            full_name: this.registerForm.name,
            email: this.registerForm.email,
            password: this.registerForm.password,
            // password_confirm: this.registerForm.confirmPassword,
            role: "телефонист",
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        if (response.status == 200) {
          this.registerSuccess = true;
          this.registerForm = {
            name: '',
            email: '',
            password: '',
            confirmPassword: ''
          };
          // Автоматически переключаем на вкладку входа через 2 секунды
          setTimeout(() => {
            this.isRegister = false;
            this.registerSuccess = false;
          }, 2000);
        } else {
          this.registerError = response.message || 'Ошибка регистрации';
        }
      } catch (error) {
        this.registerError = 'Произошла ошибка при регистрации';
        console.error('Register error:', error);
      } finally {
        this.loading = false;
      }
    },

    // Заглушка для запроса входа
    mockLoginRequest() {
      return new Promise((resolve) => {
        setTimeout(() => {
          if (this.loginForm.email === 'test@example.com' && 
              this.loginForm.password === 'password') {
            resolve({ success: true, token: 'mock-token' });
          } else {
            resolve({ success: false, message: 'Неверный email или пароль' });
          }
        }, 1000);
      });
    },

    // Заглушка для запроса регистрации
    mockRegisterRequest() {
      return new Promise((resolve) => {
        setTimeout(() => {
          if (this.registerForm.email === 'exists@example.com') {
            resolve({ success: false, message: 'Email уже зарегистрирован' });
          } else {
            resolve({ success: true });
          }
        }, 1000);
      });
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 100vw;
  min-height: 100vh;
}

.auth-container {
  background: rgb(255, 255, 255);;
  border: black 1px solid;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  padding: 30px;
  transition: all 0.3s ease;
}

.auth-container.register-mode {
  max-width: 450px;
}

.tabs {
  display: flex;
  margin-bottom: 25px;
  border-bottom: 1px solid #eee;
}

.tab {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #666;
  position: relative;
  transition: all 0.3s ease;
}

.tab.active {
  color: #404040;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #848484;
  animation: tab-underline 0.3s ease-out;
}

@keyframes tab-underline {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

.auth-form {
  animation: fade-in 0.5s ease;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

h2 {
  margin: 0 0 25px;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
}

input {
  width: 80%;
  padding: 12px 15px;
  background: rgb(248, 248, 248);
  color: black;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 15px;
  transition: border 0.3s;
}

input:focus {
  border-color: #515151;
  outline: none;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: #e0e0e0;
  color: rgb(0, 0, 0);;
  border: none;
  outline: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.5s, transform 0.2s;
  margin-top: 10px;
}

.submit-btn:hover {
  background: #ffffff;
  color: black;
  border: 1px solid gray;
}

.submit-btn:active {
  transform: scale(0.98);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loader {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: rgb(44, 44, 44);;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background: #ffebee;
  color: #d32f2f;
  border-radius: 5px;
  font-size: 14px;
  text-align: center;
  animation: shake 0.5s;
}

.success-message {
  margin-top: 15px;
  padding: 10px;
  background: #e8f5e9;
  color: #2e7d32;
  border-radius: 5px;
  font-size: 14px;
  text-align: center;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>