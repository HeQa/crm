<template>
  <div class="modal">
    <div class="modal-header">
      <h3>Добавить напоминание</h3>
    </div>
    
    <div class="modal-body">
      <div class="form-group">
        <label>Дата и время:</label>
        <VueDatePicker
          v-model="event.date"
          :min-date="new Date()"
          :enable-time-picker="true"
          :is-24="true"
          auto-apply
          placeholder="Выберите дату и время"
          text-input
          :class="['custom-datepicker']"
        />
      </div>
      
      <div class="form-group">
        <label>Описание:</label>
        <textarea 
          v-model="event.description" 
          rows="3"
          placeholder="Введите описание напоминания"
        ></textarea>
      </div>
    </div>
    
    <div class="modal-footer">
      <button @click="saveReminder" class="save-button" :disabled="!isFormValid">
        {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </div>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import axios from 'axios';
import '@vuepic/vue-datepicker/dist/main.css';

export default {
  components: { VueDatePicker },
  emits: ['saved'],
  
  data() {
    return {
      event: {
        date: null,
        description: '',
      },
      isLoading: false
    }
  },
  
  computed: {
    isFormValid() {
      return this.event.date && this.event.description.trim();
    }
  },
  
  methods: {
    async saveReminder() {
      if (!this.isFormValid) return;
      
      this.isLoading = true;
      
      try {
        const payload = {
          datetime: this.event.date.toISOString(),
          description: this.event.description,
          status: 'pending'
        };
        
        const response = await axios.post('/api/reminders', payload, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        
        this.$emit('saved', response.data);
        
      } catch (error) {
        console.error('Ошибка сохранения напоминания:', error);
        alert('Не удалось сохранить напоминание');
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.modal {

  width: 100%;

  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
}

textarea {
  width: 100%;
  border: 1px solid #ddd;
  background-color: #fff;
  color: black;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  min-height: 80px;
}

textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px 20px;
  border-top: 1px solid #eee;
  gap: 12px;
}

.save-button {
  padding: 10px 20px;
  background: #4a90e2;
  border: none;
  outline: none;
  border-radius: 4px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.save-button:hover:not(:disabled) {
  background: #3a7bc8;
}

.save-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
</style>

<style>
/* Глобальные стили для DatePicker */
.custom-datepicker {
  width: 100%;
}

.custom-datepicker .dp__input {
  height: 44px;
  border: 1px solid #ddd;
  width: 100%;
}

.custom-datepicker .dp__input:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.dp__theme_light {
  --dp-background-color: white;
  --dp-text-color: #333;
  --dp-primary-color: #4a90e2;
  --dp-border-radius: 4px;
}
</style>