<template>
  <div class="notification-container">
    <transition-group name="notification">
      <div 
        v-for="notification in activeNotifications" 
        :key="notification.id"
        class="notification"
        :class="notification.type"
      >
        <div class="notification-content">
          <h4>{{ notification.title }}</h4>
          <p>{{ notification.message }}</p>
          <button 
            v-if="notification.action" 
            @click="handleAction(notification)"
            class="action-button"
          >
            {{ notification.actionText }}
          </button>
        </div>
        <button @click="dismissNotification(notification.id)" class="close-button">
          &times;
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeNotifications: [],
      notificationInterval: null,
      notificationTypes: [
        {
          type: 'verification',
          title: 'Проверка активности',
          message: 'Подтвердите вашу активность',
          action: true,
          actionText: 'Подтвердить',
          duration: 10000
        }
      ]
    }
  },
  methods: {
    showRandomNotification() {
      const randomType = Math.floor(Math.random() * this.notificationTypes.length);
      const notification = {
        id: Date.now(),
        ...this.notificationTypes[randomType]
      };
      
      this.activeNotifications.push(notification);
      
      setTimeout(() => {
        this.dismissNotification(notification.id);
      }, notification.duration);
    },
    dismissNotification(id) {
      this.activeNotifications = this.activeNotifications.filter(n => n.id !== id);
    },
    handleAction(notification) {
      if (notification.type === 'verification') {
        this.$emit('activity-verified');
      }
      this.dismissNotification(notification.id);
    },
    startNotificationInterval() {
      // Случайный интервал между 5 и 15 минутами
      const getRandomInterval = () => Math.floor(Math.random() * 10 * 60000) + 5 * 60000;
      
      this.notificationInterval = setInterval(() => {
        this.showRandomNotification();
      }, getRandomInterval());
      
      // Первое уведомление через 1-3 минуты
      setTimeout(() => {
        this.showRandomNotification();
      }, Math.floor(Math.random() * 2 * 60000) + 60000);
    }
  },
  mounted() {
    this.startNotificationInterval();
  },
  beforeDestroy() {
    clearInterval(this.notificationInterval);
  }
}
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.notification {
  display: flex;
  align-items: center;
  width: 300px;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 4px;
  color: rgb(44, 44, 44);;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

.notification-enter-active, .notification-leave-active {
  transition: all 0.5s ease;
}
.notification-enter, .notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-content {
  flex: 1;
}

.notification h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.notification p {
  margin: 0;
  font-size: 14px;
}

.verification {
  background: #ff6b6b;
}

.info {
  background: rgb(44, 44, 44);;
}

.warning {
  background: #ffc87b;
}

.action-button {
  margin-top: 10px;
  padding: 5px 10px;
  background: rgba(255,255,255,0.2);
  border: none;
  outline: none;
  border-radius: 3px;
  color: rgb(44, 44, 44);;
  cursor: pointer;
}

.close-button {
  margin-left: 10px;
  background: none;
  border: none;
  outline: none;
  color: rgb(44, 44, 44);;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}
</style>