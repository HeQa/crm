<template>
  <header class="header">
    <h1>Система управления</h1>
    <div class="role-switcher">
      <button 
        @click="roleAdmin()" 
        :class="{ active: role === 'admin' }"
      >
        Администратор
      </button>
      <button 
        @click="roleEmployee()" 
        :class="{ active: role === 'employee' }"
      >
        Сотрудник
      </button>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
        role: "admin"
    }
  },
  methods: {
    roleAdmin() {
        if (this.role == "employee") {
            this.$router.push("/admin")
            this.role = 'admin'
        }
    },
    roleEmployee() {
        if (this.role == "admin") {
            this.$router.push("/employee")
            this.role = 'employee'
        }
    }
  }
}
</script>

<style scoped>
* {
    color:rgb(44, 44, 44);;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 30px;
}

.role-switcher button {
  padding: 8px 16px;
  margin-left: 10px;
  border: 1px solid #ddd;
  color: rgb(63, 63, 63);
  background: #fff;
  outline: none;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}


.role-switcher button:hover {
  background: #f5f5f5;
}

.role-switcher button.active:hover {
  background: #dddddd;
}
</style>