<template>
  <div class="simple-chat">
    <div class="chat-header">
      <h3>Chat Simple</h3>
    </div>
    <div class="chat-messages">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <strong>{{ message.role }}:</strong> {{ message.content }}
      </div>
    </div>
    <div class="chat-input">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Tapez votre message..." />
      <button @click="sendMessage">Envoyer</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const messages = ref([
  { role: 'Assistant', content: 'Bonjour ! Comment puis-je vous aider ?' }
])
const newMessage = ref('')

function sendMessage() {
  if (newMessage.value.trim()) {
    messages.value.push({ role: 'Utilisateur', content: newMessage.value })
    newMessage.value = ''
  }
}
</script>

<style scoped>
.simple-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  height: 400px;
  background: white;
  border: 2px solid #2563eb;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  z-index: 10000;
}

.chat-header {
  background: #2563eb;
  color: white;
  padding: 10px;
  text-align: center;
  border-radius: 8px 8px 0 0;
}

.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background: #f8f9fa;
}

.message {
  margin-bottom: 8px;
  padding: 5px;
  background: white;
  border-radius: 5px;
}

.chat-input {
  padding: 10px;
  display: flex;
  gap: 5px;
}

.chat-input input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.chat-input button {
  padding: 5px 10px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
</style>
