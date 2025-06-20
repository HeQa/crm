<template>
  <div class="status-form">
    <div v-for="(status, index) in statuses" :key="index" class="status-item">
      <input v-model="statuses[index]">
      <button @click="removeStatus(index)">×</button>
    </div>
    
    <button @click="addStatus" class="add-button">+ Добавить статус</button>
  </div>
</template>

<script>
export default {
  props: {
    statuses: {
      type: Array,
      required: true
    }
  },
  methods: {
    addStatus() {
      this.$emit('update', [...this.statuses, 'Новый статус'])
    },
    removeStatus(index) {
      const newStatuses = [...this.statuses]
      newStatuses.splice(index, 1)
      this.$emit('update', newStatuses)
    }
  }
}
</script>

<style scoped>
.status-form {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 4px;
}

.status-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.status-item input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ddd;
  outline: none;
  border-radius: 4px;
}

.status-item button {
  margin-left: 10px;
  border: none;
  outline: none;
  background: #ff5353;
  border-radius: 10%;
  cursor: pointer;
}

.add-button {
  margin-top: 10px;
  padding: 8px 15px;
  background: rgb(255, 255, 255);
  color: black;
  border: 1px solid black;
  outline: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>