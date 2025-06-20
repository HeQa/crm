<template>
  <div class="modal-overlay">
    <div class="modal">
      <h3>Детали звонка</h3>
      <div class="form-group">
        <label>Дата и время:</label>
        <input type="datetime-local" v-model="localCall.date">
      </div>
      <div class="form-group">
        <label>Результат:</label>
        <input v-model="localCall.result">
      </div>
      <div class="form-group">
        <label>Подробности:</label>
        <textarea v-model="localCall.details" rows="3"></textarea>
      </div>
      <div class="form-group">
        <label>Следующий звонок:</label>
        <input type="datetime-local" v-model="localCall.nextCall">
      </div>
      <div class="modal-actions">
        <button @click="$emit('close')" class="cancel-button">Отмена</button>
        <button @click="save" class="save-button">Сохранить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['call'],
  data() {
    return {
      localCall: { ...this.call }
    }
  },
  methods: {
    save() {
      // Преобразование строк даты в объекты Date
      if (typeof this.localCall.date === 'string') {
        this.localCall.date = new Date(this.localCall.date);
      }
      if (typeof this.localCall.nextCall === 'string') {
        this.localCall.nextCall = this.localCall.nextCall ? new Date(this.localCall.nextCall) : null;
      }
      this.$emit('save', this.localCall);
    }
  }
}
</script>

<style scoped>
.modal-overlay {
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

.modal {
  background: rgb(181, 180, 180);
  padding: 20px;
  border-radius: 4px;
  width: 400px;
  max-width: 90%;
}

.modal h3 {
  margin-top: 0;
  color: rgb(44, 44, 44);;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: rgb(44, 44, 44);;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 8px;
  background: #b9b9b9;
  border: 1px solid rgb(44, 44, 44);;
  border-radius: 3px;
  color: rgb(44, 44, 44);;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-button {
  padding: 8px 16px;
  background: #ff6b6b;
  border: none;
  outline: none;
  border-radius: 3px;
  color: rgb(44, 44, 44);;
  cursor: pointer;
}

.save-button {
  padding: 8px 16px;
  background: rgb(176, 176, 176);
  border: 1px solid gray;
  outline: none;
  border-radius: 3px;
  color: rgb(44, 44, 44);;
  cursor: pointer;
}
</style>