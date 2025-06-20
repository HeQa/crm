<template>
  <div class="employee-stats">
    <h3>Статистика рабочего времени</h3>
    
    <div class="filters">
      <div class="filter-group">
        <label>Сотрудник:</label>
        <select v-model="selectedEmployee">
          <option v-for="emp in employees" :key="emp.id" :value="emp.id">
            {{ emp.name }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Дата:</label>
        <input type="date" v-model="selectedDate">
      </div>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.totalWorked || '--:--:--' }}</div>
        <div class="stat-label">Отработано</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-value">{{ stats.breaks || '0' }}</div>
        <div class="stat-label">Перерывы</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-value">{{ stats.breakTime || '--:--:--' }}</div>
        <div class="stat-label">Время перерывов</div>
      </div>
    </div>
    
    <div class="time-logs">
      <h4>История активности</h4>
      <table>
        <thead>
          <tr>
            <th>Время</th>
            <th>Событие</th>
            <th>Детали</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.timestamp">
            <td>{{ formatTime(log.timestamp) }}</td>
            <td>{{ getActionName(log.action) }}</td>
            <td>{{ log.duration ? `Длительность: ${formatSeconds(log.duration)}` : '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedEmployee: null,
      selectedDate: new Date().toISOString().split('T')[0],
      stats: {},
      logs: []
    }
  },
  watch: {
    selectedEmployee() {
      this.loadStats();
    },
    selectedDate() {
      this.loadStats();
    }
  },
  methods: {
    loadStats() {
      // В реальном приложении здесь будет запрос к API
      // Для демонстрации используем localStorage
      const allLogs = JSON.parse(localStorage.getItem('timeLogs') || '[]');
      
      // Фильтруем логи по выбранному сотруднику и дате
      this.logs = allLogs.filter(log => {
        const logDate = new Date(log.timestamp).toISOString().split('T')[0];
        return log.userId === this.selectedEmployee && logDate === this.selectedDate;
      });
      
      // Рассчитываем статистику
      this.calculateStats();
    },
    calculateStats() {
      let totalWorked = 0;
      let breaks = 0;
      let breakTime = 0;
      
      // Простая логика расчета - в реальном приложении будет сложнее
      let shiftStart = null;
      let lastBreakStart = null;
      
      this.logs.forEach(log => {
        if (log.action === 'shift_start') {
          shiftStart = new Date(log.timestamp);
        }
        else if (log.action === 'shift_end' && shiftStart) {
          totalWorked += (new Date(log.timestamp) - shiftStart) / 1000;
          shiftStart = null;
        }
        else if (log.action === 'break_start') {
          lastBreakStart = new Date(log.timestamp);
          breaks++;
        }
        else if (log.action === 'break_end' && lastBreakStart) {
          breakTime += (new Date(log.timestamp) - lastBreakStart) / 1000;
          lastBreakStart = null;
        }
      });
      
      this.stats = {
        totalWorked: this.formatSeconds(totalWorked),
        breaks,
        breakTime: this.formatSeconds(breakTime)
      };
    },
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString();
    },
    formatSeconds(seconds) {
      if (!seconds) return '00:00:00';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    getActionName(action) {
      const names = {
        'shift_start': 'Начало смены',
        'shift_end': 'Конец смены',
        'break_start': 'Начало перерыва',
        'break_end': 'Конец перерыва'
      };
      return names[action] || action;
    }
  },
  mounted() {
    if (this.employees.length > 0) {
      this.selectedEmployee = this.employees[0].id;
    }
  }
}
</script>

<style scoped>
.employee-stats {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filters {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-weight: 600;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin: 20px 0;
}

.stat-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.time-logs {
  margin-top: 30px;
}

.time-logs table {
  width: 100%;
  border-collapse: collapse;
}

.time-logs th,
.time-logs td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.time-logs th {
  background-color: #f5f5f5;
  font-weight: 600;
}
</style>