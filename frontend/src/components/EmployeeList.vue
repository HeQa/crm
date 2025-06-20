<template>
  <div>
    <div class="header">
      <h3>Список сотрудников</h3>
      <button @click="$emit('create')">Добавить сотрудника</button>
    </div>
    
    <table class="employee-table">
      <thead>
        <tr>
          <th>Имя</th>
          <th>Email</th>
          <th>Роль</th>
          <th>Временный пароль</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employees" :key="employee.id">
          <td>{{ employee.name }}</td>
          <td>{{ employee.email }}</td>
          <td>{{ employee.role }}</td>
          <td>{{ employee.tempPassword }}</td>
          <td class="actions">
            <button @click="$emit('edit', employee)">Редактировать</button>
            <button @click="$emit('delete', employee.id)" class="delete">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      employees: []
    }
  },
  mounted() {
    this.GetEmployees();
  },
  methods: {
    async GetEmployees() {
      const token = localStorage.getItem('access_token');

      const response = await axios.get('http://127.0.0.1:8000/employee/',
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      console.log(response.data)
    },
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.employee-table {
  width: 100%;
  border-collapse: collapse;
}

.employee-table th, 
.employee-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.employee-table th {
  font-weight: 600;
}

.actions button {
  margin-right: 5px;
  padding: 5px 10px;
  border: none;
  outline: none;
  border-radius: 3px;
  cursor: pointer;
}

.actions button.delete {
  background-color: #ff6b6b;
  color: rgb(44, 44, 44);;
}
</style>