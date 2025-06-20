<template>
  <div class="admin-view">
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
        <h2>Главная панель</h2>
        <div class="script-buttons">
          <div v-for="(group, index) in scriptGroups" :key="index" class="button-group">
            <h3>{{ group.title }}</h3>
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

      <!-- Сотрудники -->
      <div v-if="activeTab === 'employees'" class="employee-management">
        <div class="filters">
          <input 
            v-model="searchQuery" 
            placeholder="Поиск по ФИО, email, телефону..." 
            class="search-input"
          >
          
          <select v-model="roleFilter" class="filter-select">
            <option value="">Все роли</option>
            <option value="admin">Администратор</option>
            <option value="employee">Сотрудник</option>
          </select>
          
          <select v-model="telegramFilter" class="filter-select">
            <option value="">Все</option>
            <option value="linked">С привязанным Telegram</option>
            <option value="unlinked">Без Telegram</option>
          </select>
          
          <button @click="resetFilters" class="reset-button">Сбросить</button>
          <button @click="showCreateForm = true" class="add-button">+ Добавить</button>
        </div>
        
        <EmployeeList 
          :employees="filteredEmployees" 
          @edit="editEmployee" 
          @delete="deleteEmployee"
        />
      </div>
      
      <!-- Логи -->
      <div v-if="activeTab === 'logs'" class="logs-tab">
        <h2>Логи системы</h2>
        <div class="log-filters">
          <select v-model="logType" class="filter-select">
            <option value="all">Все</option>
            <option value="error">Ошибки</option>
            <option value="warning">Предупреждения</option>
            <option value="info">Информация</option>
          </select>
          <input 
            type="date" 
            v-model="logDate" 
            class="filter-select"
          >
        </div>
        <div class="log-list">
          <div v-for="(log, index) in filteredLogs" :key="index" class="log-item">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-type" :class="log.type">{{ log.type }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>

      <!-- Отчеты -->
      <div v-if="activeTab === 'reports'" class="reports-tab">
        <h2>Отчеты</h2>
        <div class="report-types">
          <button 
            v-for="report in reportTypes" 
            :key="report.id"
            @click="generateReport(report.id)"
            class="report-button"
          >
            {{ report.name }}
          </button>
        </div>
      </div>

      <!-- Клиенты -->
      <div v-if="activeTab === 'clients'" class="clients-tab">
        <h2>Клиентская база</h2>
        <div class="client-filters">
          <input 
            v-model="clientSearch" 
            placeholder="Поиск клиентов..." 
            class="search-input"
          >
          <select v-model="clientStatus" class="filter-select">
            <option value="all">Все статусы</option>
            <option value="new">Новые</option>
            <option value="active">Активные</option>
            <option value="inactive">Неактивные</option>
          </select>
        </div>
        <ClientList :clients="filteredClients" />
      </div>

      <!-- Звонки -->
      <div v-if="activeTab === 'calls'" class="calls-tab">
        <h2>История звонков</h2>
        <div class="call-filters">
          <input 
            type="date" 
            v-model="callDate" 
            class="filter-select"
          >
          <select v-model="callType" class="filter-select">
            <option value="all">Все</option>
            <option value="incoming">Входящие</option>
            <option value="outgoing">Исходящие</option>
          </select>
        </div>
        <CallList :calls="filteredCalls" />
      </div>

      <!-- Настройки -->
      <SettingsForm 
        v-if="activeTab === 'settings'" 
        :settings="settings" 
        @update="updateSettings"
      />

      <!-- Настройки скрипта продаж -->
      <div v-if="activeTab === 'script-settings'" class="script-settings">
        <h2>Настройки скрипта продаж</h2>
        <ScriptEditor :script="salesScript" @save="saveScript" />
      </div>

      <!-- Форма сотрудника -->
      <EmployeeForm 
        v-if="showCreateForm || editingEmployee" 
        :employee="editingEmployee" 
        @save="saveEmployee" 
        @cancel="cancelEdit"
      />
    </div>
  </div>
</template>

<script>
import EmployeeList from './EmployeeList.vue'
import SettingsForm from './SettingsForm.vue'
import EmployeeForm from './EmployeeForm.vue'
import ClientList from './ClientList.vue'
import CallList from './CallList.vue'
import ScriptEditor from './ScriptEditor.vue'

export default {
  components: { 
    EmployeeList, 
    SettingsForm, 
    EmployeeForm,
    ClientList,
    CallList,
    ScriptEditor
  },
  data() {
    return {
      activeTab: 'main',
      showCreateForm: false,
      editingEmployee: null,
      searchQuery: '',
      roleFilter: '',
      telegramFilter: '',
      clientSearch: '',
      clientStatus: 'all',
      logType: 'all',
      logDate: '',
      callDate: '',
      callType: 'all',
      tabs: [
        { id: 'main', name: 'Главная' },
        { id: 'employees', name: 'Сотрудники' },
        { id: 'clients', name: 'Клиенты' },
        { id: 'calls', name: 'Звонки' },
        { id: 'logs', name: 'Логи' },
        { id: 'reports', name: 'Отчеты' },
        { id: 'script-settings', name: 'Скрипт продаж' },
        { id: 'settings', name: 'Настройки' }
      ],
      employees: [
        { 
          id: 1, 
          name: 'Иван Иванов', 
          email: 'ivan@example.com', 
          phone: '+79123456789',
          company: 'ООО "Ромашка"',
          role: 'admin', 
          tempPassword: 'temp123',
          telegramLinked: true,
          telegramUsername: 'ivan_telegram',
          status: 'active'
        },
        { 
          id: 2, 
          name: 'Петр Петров', 
          email: 'petr@example.com',
          phone: '+79876543210',
          company: 'ИП Петров',
          role: 'employee', 
          tempPassword: 'temp456',
          telegramLinked: false,
          telegramUsername: '',
          status: 'active'
        },
        { 
          id: 3, 
          name: 'Сидор Сидоров', 
          email: 'sidor@example.com',
          phone: '+79012345678',
          company: 'ООО "Лютик"',
          role: 'employee', 
          tempPassword: 'temp789',
          telegramLinked: true,
          telegramUsername: 'sidor_tg',
          status: 'inactive'
        }
      ],
      clients: [
        { id: 1, name: 'ООО "ТехноПром"', phone: '+79123456789', email: 'info@techprom.ru', status: 'active', lastContact: '2023-05-20' },
        { id: 2, name: 'ИП Смирнов А.А.', phone: '+79876543210', email: 'smirnov@mail.ru', status: 'new', lastContact: '2023-05-18' },
        { id: 3, name: 'ЗАО "СтройГарант"', phone: '+79012345678', email: 'office@stroigarant.ru', status: 'inactive', lastContact: '2023-04-15' }
      ],
      calls: [
        { id: 1, clientId: 1, type: 'incoming', date: '2023-05-20 10:30', duration: '5:23', employee: 'Иван Иванов', result: 'Договор заключен' },
        { id: 2, clientId: 2, type: 'outgoing', date: '2023-05-18 14:15', duration: '12:45', employee: 'Петр Петров', result: 'Перезвонить' },
        { id: 3, clientId: 3, type: 'incoming', date: '2023-05-15 09:05', duration: '3:12', employee: 'Сидор Сидоров', result: 'Отказ' }
      ],
      logs: [
        { id: 1, time: '2023-05-20 10:30:45', type: 'info', message: 'Система запущена' },
        { id: 2, time: '2023-05-20 10:31:12', type: 'warning', message: 'Медленное соединение с базой данных' },
        { id: 3, time: '2023-05-20 10:35:23', type: 'error', message: 'Ошибка авторизации пользователя petr@example.com' }
      ],
      reportTypes: [
        { id: 'sales', name: 'Отчет по продажам' },
        { id: 'calls', name: 'Отчет по звонкам' },
        { id: 'employees', name: 'Отчет по сотрудникам' },
        { id: 'clients', name: 'Отчет по клиентам' }
      ],
      settings: {
        notificationEnabled: true,
        shiftControlEnabled: true,
        lunchStart: '13:00',
        lunchEnd: '14:00',
        statuses: ['Новый', 'Горячий', 'В работе', 'Успешно', 'Отказ']
      },
      salesScript: {
        groups: [
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
        ]
      },
      scriptGroups: [
        {
          id: 1,
          title: 'Приветствие',
          buttons: [
            { id: 1, text: 'Здравствуйте!', nextGroup: 2 },
            { id: 2, text: 'Добрый день!', nextGroup: 2 }
          ]
        }
      ]
    }
  },
  computed: {
    filteredEmployees() {
      return this.employees.filter(employee => {
        const matchesSearch = !this.searchQuery || 
          employee.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          employee.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          employee.phone.includes(this.searchQuery) ||
          (employee.company && employee.company.toLowerCase().includes(this.searchQuery.toLowerCase()));
        
        const matchesRole = !this.roleFilter || employee.role === this.roleFilter;
        
        let matchesTelegram = true;
        if (this.telegramFilter === 'linked') {
          matchesTelegram = employee.telegramLinked;
        } else if (this.telegramFilter === 'unlinked') {
          matchesTelegram = !employee.telegramLinked;
        }
        
        return matchesSearch && matchesRole && matchesTelegram;
      });
    },
    filteredClients() {
      return this.clients.filter(client => {
        const matchesSearch = !this.clientSearch || 
          client.name.toLowerCase().includes(this.clientSearch.toLowerCase()) ||
          client.phone.includes(this.clientSearch) ||
          client.email.toLowerCase().includes(this.clientSearch.toLowerCase());
        
        const matchesStatus = this.clientStatus === 'all' || client.status === this.clientStatus;
        
        return matchesSearch && matchesStatus;
      });
    },
    filteredCalls() {
      return this.calls.filter(call => {
        const matchesDate = !this.callDate || call.date.startsWith(this.callDate);
        const matchesType = this.callType === 'all' || call.type === this.callType;
        return matchesDate && matchesType;
      });
    },
    filteredLogs() {
      return this.logs.filter(log => {
        const matchesType = this.logType === 'all' || log.type === this.logType;
        const matchesDate = !this.logDate || log.time.startsWith(this.logDate);
        return matchesType && matchesDate;
      });
    }
  },
  methods: {
    editEmployee(employee) {
      this.editingEmployee = { ...employee }
    },
    deleteEmployee(id) {
      this.employees = this.employees.filter(e => e.id !== id)
    },
    saveEmployee(employee) {
      if (employee.id) {
        const index = this.employees.findIndex(e => e.id === employee.id)
        this.employees.splice(index, 1, employee)
      } else {
        employee.id = Math.max(...this.employees.map(e => e.id), 0) + 1
        this.employees.push(employee)
      }
      this.cancelEdit()
    },
    cancelEdit() {
      this.editingEmployee = null
      this.showCreateForm = false
    },
    updateSettings(updatedSettings) {
      this.settings = { ...this.settings, ...updatedSettings }
    },
    resetFilters() {
      this.searchQuery = '';
      this.roleFilter = '';
      this.telegramFilter = '';
    },
    generateReport(type) {
      alert(`Генерация отчета: ${type}`)
    },
    saveScript(script) {
      this.salesScript = script
      alert('Скрипт продаж сохранен')
    },
    selectScriptButton(button) {
      const nextGroup = this.salesScript.groups.find(g => g.id === button.nextGroup)
      if (nextGroup) {
        this.scriptGroups = [nextGroup]
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

.admin-view {
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
  background: #ffffff;
  color: #000000;
  border-bottom: 2px solid black;
  border-radius: 0;
}

.tabs button.active::after {
  display: none;
}

.tab-content {
  height: 100vh;
  background: #fff;
  padding: 30px;
  border: 2px solid #000;
  border-radius: 0;
  box-shadow: none;
}

.filters, .log-filters, .client-filters, .call-filters {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  align-items: center;
}

.search-input, .filter-select {
  flex: 1;
  min-width: 300px;
  padding: 15px;
  background: #fff;
  border: 2px solid #000;
  border-radius: 0;
  font-size: 16px;
}

.filter-select {
  max-width: 250px;
}

.reset-button, .add-button {
  padding: 15px 25px;
  border: 2px solid #000;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.reset-button:hover, .add-button:hover {
  background: #f0f0f0;
}

.add-button {
  background: #fff;
  color: #000;
}

.add-button:hover {
  background: #f0f0f0;
}

.employee-management, .logs-tab, .reports-tab, .clients-tab, .calls-tab, .script-settings {
  display: flex;
  flex-direction: column;
  gap: 30px;
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
  width: 250px;
  height: 80px;
  border: 2px solid #000;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.script-button:hover {
  background: #e5e5e5;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.log-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  border: 1px solid #000;
  align-items: center;
}

.log-time {
  font-weight: bold;
  min-width: 150px;
}

.log-type {
  padding: 5px 10px;
  font-weight: bold;
  min-width: 100px;
  text-align: center;
}

.log-type.info {
  background: #f0f0f0;
}

.log-type.warning {
  background: #fff3cd;
}

.log-type.error {
  background: #f8d7da;
}

.log-message {
  flex: 1;
}

.report-types {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.report-button {
  padding: 15px 25px;
  background: #fff;
  border: 2px solid #000;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.report-button:hover {
  background: #000;
  color: #fff;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
  }
  
  .tabs button {
    width: 100%;
    margin-bottom: 5px;
  }
  
  .filters, .log-filters, .client-filters, .call-filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input, .filter-select {
    min-width: 100%;
  }
}
</style>