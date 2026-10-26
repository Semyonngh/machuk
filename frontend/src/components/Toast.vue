<script setup>
import { ref } from 'vue'

const message = ref('')
const visible = ref(false)

function show(msg) {
    message.value = msg
    visible.value = true
    setTimeout(() => {
        visible.value = false
    }, 3000)
}

defineExpose({ show })
</script>

<template>
    <div v-if="visible" class="toast">
        {{ message }}
    </div>
</template>

<style scoped>
.toast {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #000;
    color: #fff;
    padding: 20px 40px;
    border-radius: 15px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    z-index: 9999;
    font-size: 20px;
    font-weight: bold;
    animation: fadeInScale 0.3s ease;
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.8);
    }
    to {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }
}
</style>