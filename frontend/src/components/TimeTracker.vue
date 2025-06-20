<template>
  <div class="time-tracker">
    <h3>Учёт рабочего времени</h3>
    <div class="tracker-display">
      <div class="time">{{ formattedTime }}</div>
      <div class="status">{{ statusMessage }}</div>
    </div>
    
    <div class="tracker-controls">
      <button 
        v-if="!isWorking" 
        @click="startShift"
        class="start-btn"
      >
        Начать смену
      </button>
      
      <template v-else>
        <button 
          v-if="!isOnBreak" 
          @click="startBreak"
          class="pause-btn"
        >
          Обеденный перерыв
        </button>
        <button 
          v-else 
          @click="endBreak"
          class="resume-btn"
        >
          Завершить обед
        </button>
        
        <button 
          @click="endShift"
          class="stop-btn"
        >
          Завершить смену
        </button>
      </template>
    </div>
    
    <div v-if="todaySummary" class="summary">
      <h4>Сегодняшняя статистика:</h4>
      <p>Отработано: {{ todaySummary.worked }} (из {{ todaySummary.scheduled }})</p>
      <p>Обеденные перерывы: {{ todaySummary.breaks }} ({{ todaySummary.breakTime }})</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isWorking: false,
      isOnBreak: false,
      startTime: null,
      breakStart: null,
      totalWorked: 0,
      todayWorked: 0,
      todayBreaks: 0,
      todayBreakTime: 0,
      timer: null
    }
  },
  computed: {
    formattedTime() {
      const seconds = this.totalWorked;
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    statusMessage() {
      if (this.isOnBreak) return 'На обеде';
      if (this.isWorking) return 'Работаю';
      return 'Смена не начата';
    },
    todaySummary() {
      if (!this.isWorking && this.todayWorked > 0) {
        return {
          worked: this.formatTime(this.todayWorked),
          scheduled: '8:00:00',
          breaks: this.todayBreaks,
          breakTime: this.formatTime(this.todayBreakTime)
        }
      }
      return null;
    }
  },
  methods: {
    startShift() {
      this.isWorking = true;
      this.startTime = new Date();
      this.startTimer();
      this.sendLog('shift_start');
    },
    endShift() {
      this.isWorking = false;
      this.isOnBreak = false;
      clearInterval(this.timer);
      this.todayWorked = this.totalWorked;
      this.totalWorked = 0;
      this.sendLog('shift_end');
    },
    startBreak() {
      this.isOnBreak = true;
      this.breakStart = new Date();
      this.sendLog('break_start');
    },
    endBreak() {
      this.isOnBreak = false;
      const breakDuration = Math.floor((new Date() - this.breakStart) / 1000);
      this.todayBreakTime += breakDuration;
      this.todayBreaks++;
      this.sendLog('break_end', { duration: breakDuration });
    },
    startTimer() {
      this.timer = setInterval(() => {
        if (!this.isOnBreak) {
          this.totalWorked++;
        }
      }, 1000);
    },
    formatTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    sendLog(action, data = {}) {
      // В реальном приложении здесь будет отправка на сервер
      console.log('Time log:', { action, ...data });
      
      // Эмуляция отправки на сервер
      const logEntry = {
        userId: 'employee123',
        action,
        timestamp: new Date().toISOString(),
        ...data
      };
      
      // Сохраняем в localStorage для демонстрации
      const logs = JSON.parse(localStorage.getItem('timeLogs') || '[]');
      logs.push(logEntry);
      localStorage.setItem('timeLogs', JSON.stringify(logs));
    }
  },
  beforeUnmount() {
    clearInterval(this.timer);
  }
}
</script>

<style scoped>
.time-tracker {
  background: rgb(181, 180, 180);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.tracker-display {
  text-align: center;
  margin: 20px 0;
}

.time {
  font-size: 2.5rem;
  font-weight: bold;
  font-family: monospace;
  color: #ffffff;
}

.status {
  font-size: 1.2rem;
  color: #666;
  margin-top: 5px;
}

.tracker-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

button {
  padding: 10px 20px;
  border: none;
  outline: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}

.start-btn {
  background: rgb(212, 212, 212);
  color: rgb(44, 44, 44);;
}

.pause-btn {
  background: #f6d09b;
  color: rgb(44, 44, 44);;
}

.resume-btn {
  background: #a2e6fb;
  color: rgb(44, 44, 44);;
}

.stop-btn {
  background: #ff8d70;
  color: rgb(44, 44, 44);;
}

.summary {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.summary h4 {
  margin-top: 0;
  color: #555;
}

.summary p {
  margin: 5px 0;
  color: #666;
}
</style>