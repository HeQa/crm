<script>
import Header from './components/Header.vue'

export default {
  components: { Header },
}
</script>

<template>
  <div class="main">
    <Header></Header>
    <RouterView/>
  </div>
</template>

<style scoped>
body {
  color: rgb(35, 35, 35);
}
</style>
