<template>
  <div class="script-editor">
    <div v-if="loading" class="loading-state">
      Загрузка сценария...
    </div>
    <div v-else-if="error" class="error-state">
      Ошибка загрузки: {{ error }}
    </div>
    <template v-else>
      <div class="editor-header">
        <h2>Редактор сценария</h2>
        <div class="editor-actions">
          <button @click="addGroup" class="action-button add-group">
            <span>+</span> Добавить группу
          </button>
          <button @click="saveScript" class="action-button save">
            Сохранить сценарий
          </button>
        </div>
      </div>

      <div class="groups-container">
        <div 
          v-for="(group, groupIndex) in localScript.groups" 
          :key="group.id" 
          class="group-card"
        >
          <div class="group-header" @click="toggleGroup(groupIndex)">
            <div class="group-title">
              <span class="collapse-icon">{{ isGroupOpen(groupIndex) ? '−' : '+' }}</span>
              <input 
                v-model="group.title" 
                placeholder="Название группы" 
                class="title-input"
                @click.stop
              >
            </div>
            <button @click.stop="removeGroup(groupIndex)" class="delete-button">
              Удалить
            </button>
          </div>

          <div v-if="isGroupOpen(groupIndex)" class="group-content">
            <div class="buttons-list">
              <div 
                v-for="(button, buttonIndex) in group.buttons" 
                :key="button.id" 
                class="button-item"
              >
                <div class="button-controls">
                  <input 
                    v-model="button.text" 
                    placeholder="Текст кнопки" 
                    class="button-input"
                  >
                  <button 
                    @click="removeButton(groupIndex, buttonIndex)" 
                    class="small-delete-button"
                  >
                    ×
                  </button>
                </div>
                
                <div class="button-destination">
                  <label>Переход:</label>
                  <select 
                    v-model="button.nextGroup" 
                    class="destination-select"
                  >
                    <option value="">Завершить разговор</option>
                    <option 
                      v-for="g in localScript.groups" 
                      :key="g.id" 
                      :value="g.id"
                      :disabled="g.id === group.id"
                    >
                      {{ g.title || `Группа ${g.id}` }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <button @click="addButton(groupIndex)" class="add-button">
              + Добавить кнопку
            </button>
          </div>
        </div>

        <div v-if="localScript.groups.length === 0" class="empty-state">
          <p>Нет добавленных групп</p>
          <button @click="addGroup" class="action-button add-group">
            <span>+</span> Создать первую группу
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      localScript: {
        groups: []
      },
      openGroups: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    // this.CreateScript();
    this.fetchScripts();
  },
  methods: {
    async CreateScript() {
      const data = {
        name: "3123124443",
        description: "312312132abob"
      };
      const token = localStorage.getItem('access_token');

      const response = await axios.post('https://92.100.127.109/scripts/create',
        data, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
      
    },
    async fetchScripts() {
      this.loading = true;
      this.error = null;
      const token = localStorage.getItem('access_token');
      try {
        const response = await axios.get('https://92.100.127.109/scripts/start',
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        console.log("response: ", response.data)
        this.localScript.groups = JSON.parse(JSON.stringify(response.data));
        console.log("scripts", this.localScript.groups)
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load scripts';
        console.error('Error fetching scripts:', err);
      } finally {
        this.loading = false;
      }
    },
    isGroupOpen(index) {
      return this.openGroups.includes(index)
    },
    toggleGroup(index) {
      if (this.isGroupOpen(index)) {
        this.openGroups = this.openGroups.filter(i => i !== index)
      } else {
        this.openGroups.push(index)
      }
    },
    addGroup() {
      const newId = this.localScript.groups.length > 0 
        ? Math.max(...this.localScript.groups.map(g => g.id)) + 1
        : 1;
      
      const newGroup = {
        id: newId,
        title: `Группа ${newId}`,
        buttons: []
      };
      
      this.localScript.groups.push(newGroup)
      this.openGroups.push(this.localScript.groups.length - 1)
    },
    removeGroup(index) {
      this.localScript.groups.splice(index, 1)
      this.openGroups = this.openGroups
        .filter(i => i !== index)
        .map(i => i > index ? i - 1 : i)
    },
    addButton(groupIndex) {
      const group = this.localScript.groups[groupIndex]
      const newId = group.buttons.length > 0 
        ? Math.max(...group.buttons.map(b => b.id)) + 1
        : 1;
      
      group.buttons.push({
        id: newId,
        text: '',
        nextGroup: ''
      })
    },
    removeButton(groupIndex, buttonIndex) {
      this.localScript.groups[groupIndex].buttons.splice(buttonIndex, 1)
    },
    saveScript() {
      this.$emit('save', this.localScript)
    }
  }
}
</script>

<style scoped>
.script-editor {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.editor-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #000;
}

.editor-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.editor-actions {
  display: flex;
  gap: 10px;
}

.action-button {
  padding: 8px 15px;
  border: 2px solid #000;
  background: white;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}

.action-button:hover {
  background: #f0f0f0;
}

.action-button.add-group span {
  font-weight: bold;
  margin-right: 5px;
}

.action-button.save {
  background: #000;
  color: white;
}

.action-button.save:hover {
  background: #333;
}

.groups-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.group-card {
  border: 2px solid #000;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: #f8f8f8;
  cursor: pointer;
  user-select: none;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-grow: 1;
}

.collapse-icon {
  font-weight: bold;
  font-size: 1.2rem;
  width: 20px;
  text-align: center;
}

.title-input {
  flex-grow: 1;
  padding: 8px;
  border: 2px solid #000;
  font-size: 1rem;
}

.title-input:focus {
  outline: none;
  border-color: #666;
}

.delete-button {
  padding: 5px 10px;
  background: #dc3545;
  border: 2px solid #000;
  color: white;
  cursor: pointer;
  margin-left: 15px;
}

.delete-button:hover {
  background: #c82333;
}

.group-content {
  padding: 15px;
  background: white;
}

.buttons-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 15px;
}

.button-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  border: 1px dashed #ccc;
}

.button-controls {
  display: flex;
  gap: 10px;
}

.button-input {
  flex-grow: 1;
  padding: 8px;
  border: 2px solid #000;
}

.small-delete-button {
  padding: 0 10px;
  background: #dc3545;
  border: 2px solid #000;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

.button-destination {
  display: flex;
  align-items: center;
  gap: 10px;
}

.button-destination label {
  white-space: nowrap;
}

.destination-select {
  flex-grow: 1;
  padding: 8px;
  border: 2px solid #000;
}

.add-button {
  width: 100%;
  padding: 10px;
  background: white;
  border: 2px dashed #000;
  cursor: pointer;
  font-weight: bold;
}

.add-button:hover {
  background: #f8f8f8;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  border: 2px dashed #ccc;
}

.empty-state p {
  margin-bottom: 20px;
  color: #666;
}

@media (max-width: 768px) {
  .editor-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .editor-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .button-item {
    padding: 10px;
  }
  
  .button-controls {
    flex-direction: column;
  }
  
  .button-destination {
    flex-direction: column;
    align-items: flex-start;
  }
}
.loading-state,
.error-state {
  padding: 40px;
  text-align: center;
  font-size: 1.2rem;
}

.error-state {
  color: #dc3545;
}

</style>