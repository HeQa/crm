<template>
  <div class="form-modal">
    <div class="form-content">
      <h3>{{ employee.id ? 'Редактировать' : 'Добавить' }} сотрудника</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Имя</label>
          <input v-model="formData.name" required>
        </div>
        
        <div class="form-group">
          <label>Email</label>
          <input v-model="formData.email" type="email" required>
        </div>
        
        <div class="form-group">
          <label>Роль</label>
          <select v-model="formData.role" required>
            <option value="admin">Администратор</option>
            <option value="employee">Сотрудник</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Временный пароль</label>
          <input v-model="formData.tempPassword" required>
        </div>
        
        <div class="form-actions">
          <button type="submit">Сохранить</button>
          <button type="button" @click="$emit('cancel')">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    employee: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: this.employee 
        ? { ...this.employee } 
        : { name: '', email: '', role: 'employee', tempPassword: '' }
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('save', this.formData)
    }
  }
}
</script>

<style scoped>
.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.form-content {
  background: rgb(255, 255, 255);
  border: 1px solid black;
  padding: 30px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  outline: none;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.form-actions button {
  padding: 10px 20px;
  border: none;
  outline: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all ease 0.3s;
}

.form-actions button:hover {
  background-color: #f0f0f0;
}
</style>