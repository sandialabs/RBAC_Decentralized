<template>
  <div>
    <b-alert dismissible show variant="success" fade>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
