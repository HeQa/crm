<template>
  <div class="employee-view">
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id" 
        :class="{ active: activeTab === tab.id }"
      >
        {{ tab.name }}
      </button>
    </div>

    <div class="tab-content">
      <!-- Главная -->
      <div v-if="activeTab === 'main'" class="main-tab">
        <h2>Добро пожаловать, {{ employeeName }}!</h2>
        
        <div v-if="!shiftStarted" class="shift-control">
          <button @click="startShift" class="shift-button">Начать смену</button>
        </div>
        <div v-else class="shift-control">
          <p>Смена начата: {{ shiftStartTime }}</p>
          <button @click="endShift" class="shift-button">Завершить смену</button>
        </div>

        <h2>Напоминания</h2>
        <div class="calendar-controls">
          <button @click="prevMonth" class="nav-button">&lt;</button>
          <h3>{{ currentMonthName }} {{ currentYear }}</h3>
          <button @click="nextMonth" class="nav-button">&gt;</button>
        </div>
        
        <div class="calendar-grid">
          <div 
            v-for="day in calendarDays" 
            :key="day.date"
            @click="selectDay(day)"
            :class="[
              'calendar-day', 
              { 
                'current-month': day.isCurrentMonth,
                'today': day.isToday,
                'selected': selectedDay && day.date === selectedDay.date,
                'has-notes': hasNotes(day.date)
              }
            ]"
          >
            <div class="day-number">{{ day.day }}</div>
          </div>
        </div>
        
        <div v-if="selectedDay" class="day-notes">
          <h3>Напоминания на {{ selectedDay.date }}</h3>
          <div v-if="getNotesForDay(selectedDay.date).length === 0" class="no-notes">
            Нет напоминаний на этот день
          </div>
          <div v-else>
            <div v-for="(note, index) in getNotesForDay(selectedDay.date)" :key="index" class="note">
              {{ note }}
            </div>
            <button @click="addNote(selectedDay.date)" class="add-note-button">+ Добавить напоминание</button>
          </div>
        </div>
        <div v-else class="select-day-prompt">
          Выберите день для просмотра напоминаний
        </div>

        <Notification @activity-verified="handleActivityVerification" />
      </div>
      

      <div v-if="activeTab === 'script'">
        <div class="script-section">
          <h3>Скрипт продаж</h3>
          <div class="script-buttons">
            <div v-for="(group, index) in scriptGroups" :key="index" class="button-group">
              <h4>{{ group.title }}</h4>
              <div class="buttons-row">
                <button 
                  v-for="(btn, btnIndex) in group.buttons" 
                  :key="btnIndex"
                  @click="selectScriptButton(btn)"
                  class="script-button"
                >
                  {{ btn.text }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="client-form-section">
          <h3>Добавить клиента</h3>
          <form @submit.prevent="addClient" class="client-form">
            <div class="form-group">
              <label>ФИО:</label>
              <input v-model="newClient.full_name" required class="form-input">
            </div>
            
            <div class="form-group">
              <label>Телефон:</label>
              <input v-model="newClient.phone" required class="form-input">
            </div>
            
            <div class="form-group">
              <label>Email:</label>
              <input v-model="newClient.email" type="email" class="form-input">
            </div>
            
            <div class="form-group">
              <label>Статус:</label>
              <select v-model="newClient.status_id" required class="form-input">
                <option v-for="status in statuses" :key="status.id" :value="status.id">
                  {{ status.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Источник:</label>
              <input v-model="newClient.source" class="form-input">
            </div>
            
            <button type="submit" class="save-button">Добавить клиента</button>
          </form>
        </div>
      </div>


      <div v-if="activeTab === 'my_clients'" class="my-clients-section">
        <h3>Мои клиенты</h3>
        <div v-if="myClients.length === 0" class="empty-state">
          <p>Нет добавленных клиентов</p>
        </div>
        <div v-else class="clients-list">
          <div v-for="client in myClients" :key="client.id" class="client-card">
            <div class="client-info">
              <p><strong>ФИО:</strong> {{ client.full_name }}</p>
              <p><strong>Телефон:</strong> {{ client.phone }}</p>
              <p v-if="client.email"><strong>Email:</strong> {{ client.email }}</p>
              <p><strong>Статус:</strong> {{ getStatusName(client.status_id) }}</p>
              <p v-if="client.source"><strong>Источник:</strong> {{ client.source }}</p>
            </div>
            <button @click="sendToManager(client)" class="send-button">Отправить менеджеру</button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'events'">
        <Event></Event>
      </div>
      <!-- Настройки профиля -->
      <div v-if="activeTab === 'profile'" class="profile-tab">
        <h2>Настройки профиля</h2>
        
        <div class="profile-form">
          <div class="form-group">
            <label>ФИО:</label>
            <input v-model="employeeData.name" class="form-input">
          </div>
          
          <div class="form-group">
            <label>Email:</label>
            <input v-model="employeeData.email" type="email" class="form-input">
          </div>
          
          <div class="form-group">
            <label>Телефон:</label>
            <input v-model="employeeData.phone" class="form-input">
          </div>
          
          <div class="form-group">
            <label>Новый пароль:</label>
            <input v-model="employeeData.newPassword" type="password" class="form-input">
          </div>
          
          <div class="telegram-section">
            <div v-if="!employeeData.telegramLinked" class="telegram-unlinked">
              <p>Привяжите Telegram для получения уведомлений</p>
              <button @click="startTelegramLinking" class="link-button">Привязать Telegram</button>
              <div v-if="linkingCode" class="linking-code">
                <p>Ваш код для привязки: <strong>{{ linkingCode }}</strong></p>
                <p>Отправьте этот код боту @CompanyBot</p>
              </div>
            </div>
            <div v-else class="telegram-linked">
              <p>Telegram привязан: @{{ employeeData.telegramUsername }}</p>
              <button @click="unlinkTelegram" class="unlink-button">Отвязать</button>
            </div>
          </div>
          
          <button @click="saveProfile" class="save-button">Сохранить изменения</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Notification from './Notification.vue'
import Event from './EventModal.vue'
import axios from 'axios'
export default {
  components: { Notification, Event },
  data() {
    return {
      activeTab: 'main',
      tabs: [
        { id: 'main', name: 'Главная' },
        { id: 'script', name: 'Скрипт продаж' },
        { id: 'my_clients', name: 'Мои клиенты' },
        { id: 'events', name: 'Напоминания' },
        { id: 'profile', name: 'Настройки профиля' }
      ],
      shiftStarted: false,
      shiftStartTime: '',
      employeeData: {
        name: 'Иван Иванов',
        email: 'ivan@example.com',
        phone: '+79123456789',
        newPassword: '',
        telegramLinked: false,
        telegramUsername: ''
      },
      linkingCode: '',
      scriptGroups: [
        {
          id: 1,
          title: 'Приветствие',
          buttons: [
            { id: 1, text: 'Здравствуйте!', nextGroup: 2 },
            { id: 2, text: 'Добрый день!', nextGroup: 2 }
          ]
        },
        {
          id: 2,
          title: 'Ответ клиента',
          buttons: [
            { id: 3, text: 'Да, я слушаю', nextGroup: 3 },
            { id: 4, text: 'Кто это?', nextGroup: 4 },
            { id: 5, text: 'Я занят', nextGroup: 5 }
          ]
        }
      ],
      currentDate: new Date(),
      selectedDay: null,
      notes: {
        '2025-06-12': ['Позвонить клиенту горяч. Роуз', 'Позвонить 10 клиентам'],
        '2025-06-13': ['Созвон с коллегой', 'Обзвонить горячих клиентов'],
        '2025-06-14': ['Подвести статистику за неделю', 'Позвонить 10 клиентам']
      },
      newClient: {
        full_name: '',
        phone: '',
        email: '',
        status_id: 1,
        source: ''
      },
      statuses: [
        { id: 1, name: 'Новый' },
        { id: 2, name: 'Горячий' },
        { id: 3, name: 'В работе' },
        { id: 4, name: 'Успешно' },
        { id: 5, name: 'Отказ' }
      ],
      myClients: []
    }
  },
  computed: {
    employeeName() {
      return this.employeeData.name.split(' ')[0] || 'Сотрудник';
    },
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    currentMonthName() {
      return this.currentDate.toLocaleString('ru-RU', { month: 'long' });
    },
    calendarDays() {
      const year = this.currentYear;
      let month = this.currentMonth;
      // Первый день месяца
      const firstDay = new Date(year, month, 1);
      // Последний день месяца
      const lastDay = new Date(year, month + 1, 0);
      
      // Дни предыдущего месяца для заполнения сетки
      const prevMonthDays = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
      // Дни следующего месяца для заполнения сетки
      const nextMonthDays = 6 - lastDay.getDay();
      
      const days = [];
      
      // Добавляем дни предыдущего месяца
      const prevMonthLastDay = new Date(year, month, 0).getDate();
      for (let i = prevMonthDays; i > 0; i--) {
        const day = prevMonthLastDay - i + 1;
        days.push({
          day,
          date: `${year}-${month}-${day}`,
          isCurrentMonth: false
        });
      }
      
      // Добавляем дни текущего месяца
      const today = new Date();
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = `${year}-${month + 1}-${i}`;
        days.push({
          day: i,
          date,
          isCurrentMonth: true,
          isToday: today.getFullYear() === year && 
                   today.getMonth() === month && 
                   today.getDate() === i
        });
      }
      
      // Добавляем дни следующего месяца
      for (let i = 1; i <= nextMonthDays; i++) {
        days.push({
          day: i,
          date: `${year}-${month + 2}-${i}`,
          isCurrentMonth: false
        });
      }

      return days;
    }
  },
  mounted() {
    this.getClients();
  },
  methods: {
    prevMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
      this.selectedDay = null;
    },
    
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
      this.selectedDay = null;
    },
    
    selectDay(day) {
      this.selectedDay = day;
    },
    
    hasNotes(date) {
      let date_split = date.split("-")
      if (date_split[2].length == 1) {
        date = date_split[0] + "-" + date_split[1] + "-" + "0" + date_split[2]
      }
      date_split = date.split("-")
      if (date_split[1].length == 1) {
        date = date_split[0] + "-" + "0" + date_split[1] + "-" + date_split[2]
      }
      return this.notes[date] && this.notes[date].length > 0;
    },
    
    getNotesForDay(date) {
      let date_split = date.split("-")
      if (date_split[2].length == 1) {
        date = date_split[0] + "-" + date_split[1] + "-" + "0" + date_split[2]
      }
      date_split = date.split("-")
      if (date_split[1].length == 1) {
        date = date_split[0] + "-" + "0" + date_split[1] + "-" + date_split[2]
      }
      return this.notes[date] || [];
    },
    
    addNote(date) {
      const noteText = prompt('Введите напоминание:');
      if (noteText) {
        if (!this.notes[date]) {
          this.$set(this.notes, date, []);
        }
        this.notes[date].push(noteText);
      }
    },
    async getClients() {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        'http://127.0.0.1:8000/clients/',
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      console.log(response)
    },
    async addClient() {
      const client = {
        ...this.newClient,
        id: this.myClients.length > 0 ? Math.max(...this.myClients.map(c => c.id)) + 1 : 1,
        responsible_employee_id: 1 // В реальном приложении - ID текущего сотрудника
      };
      const token = localStorage.getItem('access_token');
      console.log(client)
      const response = await axios.post(
        'http://127.0.0.1:8000/clients/sync_clients',
        {
          clients: [client]
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      console.log(response)
      this.myClients.push(client);
      this.resetClientForm();
      
      // Здесь должна быть логика отправки на сервер
      console.log('Добавлен клиент:', client);
    },
    
    resetClientForm() {
      this.newClient = {
        full_name: '',
        phone: '',
        email: '',
        status_id: 1,
        source: ''
      };
    },
    
    getStatusName(statusId) {
      const status = this.statuses.find(s => s.id === statusId);
      return status ? status.name : 'Неизвестно';
    },
    
    sendToManager(client) {
      // Здесь должна быть логика отправки менеджеру
      // console.log('Отправлено менеджеру:', client);
      alert(`Клиент ${client.full_name} отправлен менеджеру`);
    },
    startShift() {
      this.shiftStarted = true;
      this.shiftStartTime = new Date().toLocaleTimeString();
      // Здесь должна быть логика отправки на сервер
    },
    endShift() {
      this.shiftStarted = false;
      this.shiftStartTime = '';
      // Здесь должна быть логика отправки на сервер
    },
    startTelegramLinking() {
      this.linkingCode = Math.random().toString(36).substring(2, 8).toUpperCase();
      // Эмуляция успешной привязки через 5 секунд
      setTimeout(() => {
        this.employeeData.telegramLinked = true;
        this.employeeData.telegramUsername = 'example_user';
        this.linkingCode = '';
      }, 5000);
    },
    unlinkTelegram() {
      this.employeeData.telegramLinked = false;
      this.employeeData.telegramUsername = '';
    },
    saveProfile() {
      // Логика сохранения профиля
      alert('Изменения сохранены');
    },
    handleActivityVerification() {
      console.log('Активность сотрудника подтверждена');
    },
    selectScriptButton(button) {
      const nextGroup = this.scriptGroups.find(g => g.id === button.nextGroup);
      if (nextGroup) {
        // В реальном приложении здесь будет переход к следующей группе
        console.log('Выбрана кнопка:', button.text, 'Переход к:', nextGroup.title);
      }
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  color: #000;
}

.employee-view {
  padding: 20px;
  background: #fff;
  min-height: 100vh;
}

.tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 2px solid #000;
  flex-wrap: wrap;
}

.tabs button {
  padding: 15px 25px;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  position: relative;
  margin-right: 5px;
  transition: all 0.3s;
}

.tabs button:hover {
  background: #f0f0f0;
}

.tabs button.active {
  color: #000000;
  border-bottom: 2px solid black;
  border-radius: 0;
}

.tab-content {
  background: #fff;
  padding: 30px;
  border: 2px solid #000;
  border-radius: 0;
  box-shadow: none;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

h3 {
  font-size: 20px;
  margin-bottom: 15px;
}

h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.shift-control {
  margin-bottom: 30px;
  padding: 20px;
  border: 2px solid #000;
}

.shift-button {
  padding: 15px 25px;
  border: 2px solid #000;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.shift-button:hover {
  background: #f0f0f0;
}

.calendar-table {
  width: 100%;
}

.calendar-row {
  display: flex;
}

.calendar-row .day {
  width: 10%;
  border: 1px solid black;
  align-items: center;
  display: flex;
  justify-content: center;
}

.calendar-row .notes {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  border: 1px solid black;
}

.calendar-row .notes .note {
  text-decoration: underline;
  text-align: left;
  padding: 5px;
}

.script-section {
  margin-top: 30px;
}

.script-buttons {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.button-group {
  border: 2px solid #000;
  padding: 20px;
}

.buttons-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 15px;
}

.script-button {
  padding: 15px 25px;
  background: #fff;
  border: 2px solid #000;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.script-button:hover {
  background: #f0f0f0;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 600px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-input {
  padding: 15px;
  border: 2px solid #000;
  font-size: 16px;
}

.telegram-section {
  margin-top: 20px;
  padding: 20px;
  border: 2px solid #000;
}

.link-button, .unlink-button {
  padding: 15px 25px;
  background: #fff;
  border: 2px solid #000;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.link-button:hover, .unlink-button:hover {
  background: #f0f0f0;
}

.linking-code {
  margin-top: 15px;
  padding: 15px;
  border: 2px solid #000;
  background: #f0f0f0;
}

.save-button {
  padding: 15px 25px;
  border: 2px solid #000;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  align-self: flex-start;
}

.save-button:hover {
  background: #f0f0f0;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
  }
  
  .tabs button {
    width: 100%;
    margin-bottom: 5px;
  }
  
  .buttons-row {
    flex-direction: column;
  }
  
  .script-button {
    width: 100%;
  }
}

.client-form-section {
  margin-top: 30px;
  border: 2px solid #000;
  padding: 20px;
}

.client-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.my-clients-section {
  margin-top: 30px;
  border: 2px solid #000;
  padding: 20px;
}

.empty-state {
  padding: 20px;
  text-align: center;
  border: 2px dashed #000;
}

.clients-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.client-card {
  border: 2px solid #000;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.client-info {
  flex-grow: 1;
}

.client-info p {
  margin-bottom: 5px;
}

.send-button {
  padding: 10px 15px;
  border: 2px solid #000;
  background: #fff;
  cursor: pointer;
  white-space: nowrap;
  margin-left: 15px;
}

.send-button:hover {
  background: #f0f0f0;
}


.events-tab {
  padding: 20px;
}

.calendar-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-controls h3 {
  margin: 0 20px;
  text-align: center;
  min-width: 200px;
}

.nav-button {
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 16px;
}

.nav-button:hover {
  background: #e0e0e0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.calendar-day {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.calendar-day.current-month {
  background: white;
}

.calendar-day:not(.current-month) {
  background: #f9f9f9;
  color: #aaa;
}

.calendar-day.today {
  border-color: #4CAF50;
  font-weight: bold;
}

.calendar-day.selected {
  background: #e3f2fd;
  border-color: #2196F3;
}

.calendar-day.has-notes::after {
  content: '';
  position: absolute;
  bottom: 2px;
  width: 6px;
  height: 6px;
  background: #2196F3;
  border-radius: 50%;
}

.day-notes {
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  background: #f9f9f9;
}

.no-notes {
  color: #777;
  font-style: italic;
}

.note {
  padding: 8px;
  margin-bottom: 5px;
  background: white;
  border-radius: 4px;
  border-left: 3px solid #2196F3;
}

.add-note-button {
  margin-top: 10px;
  background: #e3f2fd;
  border: 1px solid #bbdefb;
  color: #0d47a1;
  outline: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.add-note-button:hover {
  background: #bbdefb;
}

.select-day-prompt {
  color: #777;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

@media (max-width: 768px) {
  .client-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .send-button {
    margin-left: 0;
    margin-top: 10px;
    width: 100%;
  }
}
</style>