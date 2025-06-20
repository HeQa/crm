<template>
  <div class="client-list">
    <div class="client-list-header">
      <div class="header-item">ID</div>
      <div class="header-item">Имя</div>
      <div class="header-item">Телефон</div>
      <div class="header-item">Email</div>
      <div class="header-item">Статус</div>
      <div class="header-item">Последний контакт</div>
    </div>
    
    <div 
      v-for="client in clients" 
      :key="client.id" 
      class="client-item"
      :class="`status-${client.status}`"
    >
      <div class="client-field">{{ client.id }}</div>
      <div class="client-field">{{ client.name }}</div>
      <div class="client-field">{{ client.phone }}</div>
      <div class="client-field">{{ client.email }}</div>
      <div class="client-field">
        <span class="status-badge">{{ client.status }}</span>
      </div>
      <div class="client-field">{{ client.lastContact }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      clients: [],
    }
  },
  mounted() {
    this.CreateClient();
    this.getClients();
  },
  methods: {
    async CreateClient() {
      const data = {
        full_name: "3123124443",
        phone: "89999999999",
        email: "31231@gmail.com",  // Can be null
        status_id: 0,
        responsible_employee_id: 1,
        source: "idk"  // Can be null
      };
      const token = localStorage.getItem('access_token');

      const response = await axios.post('/clients/create',
        data, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
      console.log(response.data)
      this.clients = response.data;
    },
    async getClients() {
      const token = localStorage.getItem('access_token')
      const response = await axios.get('/clients/', 
        {
          headers: {
              Authorization: `Bearer ${token}`
          }
        }
      );
      console.log(response.data)
    }
  }
}
</script>

<style scoped>
.client-list {
  border: 2px solid #000;
  margin-top: 20px;
}

.client-list-header {
  display: grid;
  grid-template-columns: 50px 1fr 1fr 1fr 100px 120px;

  color: #000000;
  border-bottom: 1px solid black;
  padding: 15px;
  font-weight: bold;
}

.client-item {
  display: grid;
  grid-template-columns: 50px 1fr 1fr 1fr 100px 120px;
  padding: 15px;
  border-bottom: 1px solid #000;
  align-items: center;
}

.client-item:last-child {
  border-bottom: none;
}

.client-field {
  padding: 0 10px;
}

.status-badge {
  display: inline-block;
  padding: 5px 10px;
  background: #000;
  color: #fff;
  font-size: 12px;
  text-transform: uppercase;
}

.status-new .status-badge {
  background: #ffc107;
  color: #000;
}

.status-active .status-badge {
  background: #28a745;
}

.status-inactive .status-badge {
  background: #dc3545;
}

@media (max-width: 768px) {
  .client-list-header,
  .client-item {
    grid-template-columns: 1fr;
  }
  
  .header-item,
  .client-field {
    padding: 5px 0;
  }
}
</style>