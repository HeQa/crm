<template>
  <div class="call-list">
    <div class="call-list-header">
      <div class="header-item">ID</div>
      <div class="header-item">Клиент</div>
      <div class="header-item">Тип</div>
      <div class="header-item">Дата и время</div>
      <div class="header-item">Длительность</div>
      <div class="header-item">Сотрудник</div>
      <div class="header-item">Результат</div>
    </div>
    
    <div 
      v-for="call in calls" 
      :key="call.id" 
      class="call-item"
      :class="`type-${call.type}`"
    >
      <div class="call-field">{{ call.id }}</div>
      <div class="call-field">{{ getClientName(call.clientId) }}</div>
      <div class="call-field">
        <span class="type-badge">{{ call.type === 'incoming' ? 'Входящий' : 'Исходящий' }}</span>
      </div>
      <div class="call-field">{{ call.date }}</div>
      <div class="call-field">{{ call.duration }}</div>
      <div class="call-field">{{ call.employee }}</div>
      <div class="call-field">{{ call.result }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    calls: {
      type: Array,
      required: true
    }
  },
  methods: {
    getClientName(clientId) {
      // В реальном приложении здесь была бы логика получения имени клиента
      return `Клиент #${clientId}`;
    }
  }
}
</script>

<style scoped>
.call-list {
  border: 2px solid #000;
  margin-top: 20px;
}

.call-list-header {
  display: grid;
  grid-template-columns: 50px 1fr 100px 150px 100px 1fr 1fr;

  color: #000000;
  padding: 15px;
  font-weight: bold;
}

.call-item {
  display: grid;
  grid-template-columns: 50px 1fr 100px 150px 100px 1fr 1fr;
  padding: 15px;
  border-bottom: 1px solid #000;
  align-items: center;
}

.call-item:last-child {
  border-bottom: none;
}

.call-field {
  padding: 0 10px;
}

.type-badge {
  display: inline-block;
  padding: 5px 10px;
  background: #000;
  color: #fff;
  font-size: 12px;
  text-transform: uppercase;
}

.type-incoming .type-badge {
  background: #28a745;
}

.type-outgoing .type-badge {
  background: #007bff;
}

@media (max-width: 768px) {
  .call-list-header,
  .call-item {
    grid-template-columns: 1fr;
  }
  
  .header-item,
  .call-field {
    padding: 5px 0;
  }
}
</style>