<template>
  <div class="settings-form">
    <h3>Настройки системы</h3>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="formData.notificationEnabled">
          Уведомления включены
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="formData.shiftControlEnabled">
          Контроль смен включен
        </label>
      </div>
      
      <div class="form-group">
        <label>Обеденный перерыв</label>
        <div class="time-range">
          <input type="time" v-model="formData.lunchStart">
          <span>—</span>
          <input type="time" v-model="formData.lunchEnd">
        </div>
      </div>
      
      <div class="form-group">
        <label>Статусы клиентов</label>
        <StatusForm 
          :statuses="formData.statuses" 
          @update="formData.statuses = $event"
        />
      </div>
      
      <button type="submit">Сохранить настройки</button>
    </form>
  </div>
</template>

<script>
import StatusForm from './StatusForm.vue'

export default {
  components: { StatusForm },
  props: {
    settings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      formData: { ...this.settings }
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('update', this.formData)
    }
  }
}
</script>

<style scoped>
.settings-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.time-range {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.time-range input {
  border: 1px solid gray;
  outline: none;
  background: rgb(232, 232, 232);
  padding: 8px;
}

button {
  padding: 10px 20px;
  background: rgb(255, 255, 255);
  outline: none;
  border-radius: 4px;
  border: 1px solid black;
  color: rgb(25, 25, 25);
  cursor: pointer;
  font-size: 16px;
}
</style>