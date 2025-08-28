<template>
  <div>
    <div v-if="open" class="assistant-overlay" @click="closeOnOverlay" />
    <transition name="assistant-fade">
      <div v-if="open" class="assistant-modal chatbot" @click.stop>
        <div class="assistant-header">
          <span class="font-semibold text-blue-700">Fidelo</span>
          <div class="connection-status">
            <span v-if="wsConnected" class="status-connected">●</span>
            <span v-else class="status-disconnected">○</span>
          </div>
          <button class="close-btn" @click="open = false">✕</button>
        </div>
        <div class="assistant-body chatbot-body" ref="chatBody">
          <div v-for="(msg, i) in messages" :key="i" :class="['chat-message', msg.role]">
            <div class="bubble" v-if="!msg.image" v-html="msg.content"></div>
            <div v-else class="bubble image-bubble"><img :src="msg.image" alt="Image envoyée" /></div>
          </div>
          <div v-if="isTyping" class="chat-message assistant">
            <div class="bubble typing-bubble">
              <span class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </div>
          </div>
        </div>
        <div class="assistant-footer">
          <button class="icon-btn" @click="triggerFileInput" title="Ajouter une image">
            <svg width="22" height="22" fill="none" viewBox="0 0 24 24">
              <rect x="3" y="5" width="18" height="14" rx="2" stroke="#2563eb" stroke-width="1.5"/>
              <circle cx="8.5" cy="10.5" r="1.5" fill="#2563eb"/>
              <path d="M21 19l-5.5-7-4.5 6-2.5-3-4 4" stroke="#2563eb" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onImageSelect"
          />
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Aperçu image" />
            <button class="remove-img" @click="removeImage" title="Retirer l'image">✕</button>
          </div>
          <input
            v-model="userInput"
            @keydown.enter="sendMessage"
            class="assistant-input"
            type="text"
            placeholder="Écrivez un message..."
            autocomplete="off"
            :disabled="recording || !wsConnected"
          />
          <button class="icon-btn" @click="handleMicClick" :class="{recording}" title="Enregistrer un audio" :disabled="!wsConnected">
            <svg v-if="!recording" width="24" height="24" fill="none" viewBox="0 0 24 24">
              <rect x="9" y="3" width="6" height="12" rx="3" fill="#2563eb"/>
              <path d="M5 10v2a7 7 0 0014 0v-2" stroke="#2563eb" stroke-width="1.5"/>
              <path d="M12 19v2" stroke="#2563eb" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <svg v-else width="24" height="24" fill="none" viewBox="0 0 24 24" class="mic-anim">
              <rect x="9" y="3" width="6" height="12" rx="3" fill="#2563eb"/>
              <path d="M5 10v2a7 7 0 0014 0v-2" stroke="#2563eb" stroke-width="1.5"/>
              <path d="M12 19v2" stroke="#2563eb" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="12" cy="12" r="10" stroke="#2563eb" stroke-width="1.5" opacity="0.3">
                <animate attributeName="r" values="10;12;10" dur="1s" repeatCount="indefinite"/>
              </circle>
            </svg>
          </button>
          <button class="icon-btn send-btn" @click="sendMessage" title="Envoyer" :disabled="!wsConnected">
            <svg width="22" height="22" fill="white" viewBox="0 0 24 24"><path d="M4 12l16-7-7 16-2.5-7L4 12z"/></svg>
          </button>
        </div>
        <div v-if="micDenied" class="mic-denied">
          <span>Vous avez refusé l'accès au micro. Veuillez autoriser le micro dans les paramètres de votre navigateur pour utiliser cette fonctionnalité.</span>
        </div>
        <div v-if="transcribing" class="transcribing-toast">
          <span>Transcription en cours...</span>
        </div>
        <div v-if="!wsConnected" class="connection-error">
          <span>Connexion perdue. Tentative de reconnexion...</span>
        </div>
      </div>
    </transition>
    <button class="assistant-fab" @click="open = true" v-if="!open">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="12" fill="#2563eb"/><path d="M8 10h8M8 14h5" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useCartStore } from '../pinia/cartStore.ts'

const cartStore = useCartStore()
const open = ref(false)
const userInput = ref('')
const recording = ref(false)
const micDenied = ref(false)
const transcribing = ref(false)

// Génération d'un ID de session unique
function generateSessionId(): string {
  return 'fidelo-' + Math.random().toString(36).substr(2, 9)
}

function formatMarkdownLite(text: string): string {
  if (!text) return ''
  let html = text
  // Échapper basique des chevrons pour éviter l'injection
  html = html.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  // Gras **texte**
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  // Italique *texte*
  html = html.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>')
  // Code `texte`
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>')
  // Listes - item → puces
  html = html.replace(/^\s*-\s+(.*)$/gm, '<div class="product-item">• $1</div>')
  // Titres ### / ## / # → span accentués
  html = html.replace(/^###\s+(.*)$/gm, '<span style="font-weight:600">$1</span>')
  html = html.replace(/^##\s+(.*)$/gm, '<span style="font-weight:600">$1</span>')
  html = html.replace(/^#\s+(.*)$/gm, '<span style="font-weight:700">$1</span>')
  // Retours à la ligne
  html = html.replace(/\n/g, '<br/>')
  return html
}

function removeEmojis(text: string): string {
  if (!text) return ''
  // Supprimer la plupart des emojis
  return text
    .replace(/[\u{1F1E6}-\u{1F1FF}]/gu, '') // drapeaux
    .replace(/[\u{1F300}-\u{1FAFF}]/gu, '') // pictogrammes & émoticônes
    .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols and Pictographs
    .replace(/[\u2600-\u{27BF}]/g, '') // Misc symbols
    .replace(/[\uFE0E\uFE0F\u200D]/g, '') // variation selectors + ZWJ
}

const fileInput = ref<HTMLInputElement | null>(null)
const chatBody = ref<HTMLElement | null>(null)
const imagePreview = ref<string | null>(null)
const wsConnected = ref(false)
const isTyping = ref(false)
const sessionId = ref('')
let imageFile: File | null = null
let mediaRecorder: MediaRecorder | null = null
let audioChunks: Blob[] = []
let websocket: WebSocket | null = null
let reconnectTimer: number | null = null

interface Message {
  role: 'user' | 'assistant',
  content?: string,
  image?: string
}

const messages = ref<Message[]>([
  { role: 'assistant', content: 'Bonjour ! Je suis Fidelo, votre assistant shopping. Comment puis-je vous aider ?' }
])

// Connexion WebSocket
function connectWebSocket() {
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    return
  }

  sessionId.value = generateSessionId()
  const wsUrl = `ws://localhost:8000/ws/${sessionId.value}`
  
  try {
    websocket = new WebSocket(wsUrl)
    
    websocket.onopen = () => {
      wsConnected.value = true
      console.log('WebSocket connecté')
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    }
    
    websocket.onclose = () => {
      wsConnected.value = false
      console.log('WebSocket déconnecté')
      // Tentative de reconnexion après 3 secondes
      if (reconnectTimer) clearTimeout(reconnectTimer)
      reconnectTimer = setTimeout(connectWebSocket, 3000)
    }
    
    websocket.onerror = (error) => {
      console.error('Erreur WebSocket:', error)
      wsConnected.value = false
    }
  } catch (error) {
    console.error('Erreur de connexion WebSocket:', error)
    wsConnected.value = false
  }
}

// Gestion des messages WebSocket
function handleWebSocketMessage(data: any) {
  if (data.type === 'welcome') {
    // Message de bienvenue (optionnel, on peut l'ignorer car on a déjà un message de bienvenue)
    return
  }
  
  if (data.type === 'typing') {
    isTyping.value = true
    return
  }
  
  if (data.type === 'response') {
    isTyping.value = false
    
    // Si c'est une réponse de transcription audio, afficher dans userInput
    if (data.transcribed_text) {
      userInput.value = data.transcribed_text
      // Supprimer le message temporaire d'audio
      if (messages.value.length > 0 && messages.value[messages.value.length - 1].content?.includes('[Message vocal en cours de traitement...]')) {
        messages.value.pop()
      }
      return
    }
    
    let responseContent = ''
    // Formater le message principal (markdown-lite → HTML)
    if (data.message) {
      const clean = removeEmojis(String(data.message))
      responseContent += formatMarkdownLite(clean)
    }
    
    // Ajouter les produits si disponibles (sans entête)
    if (data.products && data.products.length > 0) {
      responseContent += '<div class="products-suggestions">'
      data.products.forEach((product: any) => {
        const nameRaw = product.name ?? 'Produit'
        const name = removeEmojis(String(nameRaw))
        const price = (product.price !== undefined && product.price !== null) ? product.price : 'Prix non disponible'
        responseContent += `<div class="product-item">• ${name} - ${price}</div>`
      })
      responseContent += '</div>'
    }
    
    // Détecter si c'est une réponse de panier et ouvrir la modale
    if (data.cart && Object.keys(data.cart).length > 0) {
      // Ouvrir automatiquement la modale du panier
      setTimeout(() => {
        cartStore.cartOn()
      }, 500) // Petit délai pour que le message s'affiche d'abord
    }
    
    if (!responseContent) {
      responseContent = 'Je n\'ai pas pu formater la réponse.'
    }
    
    messages.value.push({ role: 'assistant', content: responseContent })
    scrollToBottom()
  }
  
  if (data.type === 'error') {
    isTyping.value = false
    messages.value.push({ role: 'assistant', content: 'Désolé, une erreur s\'est produite. Veuillez réessayer.' })
    scrollToBottom()
  }
}

// Envoi de message via WebSocket
function sendWebSocketMessage(message: string) {
  if (websocket && wsConnected.value) {
    websocket.send(JSON.stringify({ message }))
  } else {
    console.error('WebSocket non connecté')
    messages.value.push({ role: 'assistant', content: 'Erreur de connexion. Veuillez réessayer.' })
    scrollToBottom()
  }
}

function closeOnOverlay() {
  open.value = false
}

function sendMessage() {
  if (recording.value) {
    stopRecording()
    return
  }
  
  if (imagePreview.value) {
    messages.value.push({ role: 'user', image: imagePreview.value })
    sendWebSocketMessage('[Image envoyée]')
    imagePreview.value = null
    imageFile = null
    scrollToBottom()
    return
  }
  
  if (userInput.value.trim()) {
    messages.value.push({ role: 'user', content: userInput.value })
    sendWebSocketMessage(userInput.value)
    userInput.value = ''
    scrollToBottom()
  }
}

function triggerFileInput() {
  fileInput.value?.click()
}

function onImageSelect(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files && files[0]) {
    imageFile = files[0]
    imagePreview.value = URL.createObjectURL(imageFile)
  }
}

function removeImage() {
  imagePreview.value = null
  imageFile = null
}

function handleMicClick() {
  if (recording.value) {
    stopRecording()
    return
  }
  if (micDenied.value) {
    return
  }
  startRecording()
}

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    recording.value = true
    audioChunks = []
    mediaRecorder = new MediaRecorder(stream)
    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data)
    }
    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      
      // Convertir l'audio en base64
      const reader = new FileReader()
      reader.onload = () => {
        const base64Audio = reader.result as string
        const audioData = base64Audio.split(',')[1] // Enlever le préfixe data:audio/webm;base64,
        
        // Envoyer l'audio via WebSocket
        if (websocket && wsConnected.value) {
          websocket.send(JSON.stringify({
            message: '',
            audio_data: audioData,
            audio_format: 'webm'
          }))
          
          // Afficher un message temporaire
          messages.value.push({ role: 'user', content: '🎤 [Message vocal en cours de traitement...]' })
          scrollToBottom()
        } else {
          console.error('WebSocket non connecté')
          messages.value.push({ role: 'assistant', content: 'Erreur de connexion. Veuillez réessayer.' })
          scrollToBottom()
        }
      }
      reader.readAsDataURL(audioBlob)
    }
    mediaRecorder.start()
  }).catch(() => {
    micDenied.value = true
  })
}

function stopRecording() {
  recording.value = false
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight
    }
  })
}

// Connexion WebSocket quand le composant est monté
onMounted(() => {
  connectWebSocket()
})

// Nettoyage à la destruction du composant
onUnmounted(() => {
  if (websocket) {
    websocket.close()
  }
  if (reconnectTimer) {
    clearTimeout(reconnectTimer)
  }
})
</script>

<style scoped>
.assistant-fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #2563eb;
  border: none;
  border-radius: 50%;
  width: 80px;
  height: 80px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  cursor: pointer;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.2s;
  /* Debug styles */
  border: 3px solid red;
  opacity: 1;
}
.assistant-fab:hover {
  box-shadow: 0 4px 16px rgba(37,99,235,0.25);
}
.assistant-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.08);
  z-index: 1001;
}
.assistant-modal.chatbot {
  position: fixed;
  bottom: 7.5rem;
  right: 2rem;
  width: 500px;
  max-width: 99vw;
  height: 600px;
  max-height: 90vh;
  background: #fff;
  border-radius: 2rem;
  box-shadow: 0 8px 32px rgba(37,99,235,0.18), 0 1.5px 8px rgba(0,0,0,0.08);
  z-index: 1002;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: assistant-pop 0.18s cubic-bezier(.4,1.4,.6,1) both;
}
@keyframes assistant-pop {
  0% { transform: scale(0.95) translateY(30px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f1f5f9;
}
.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.status-connected {
  color: #10b981;
  font-size: 1.2rem;
}
.status-disconnected {
  color: #ef4444;
  font-size: 1.2rem;
}
.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #2563eb;
  cursor: pointer;
  padding: 0 0.25rem;
  line-height: 1;
}
.assistant-body.chatbot-body {
  padding: 2rem 1.5rem 1rem 1.5rem;
  background: #f8fafc;
  color: #1e293b;
  font-size: 1rem;
  flex: 1 1 auto;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}
.chat-message {
  display: flex;
  align-items: flex-end;
  gap: 0.7rem;
  margin-bottom: 0.2rem;
}
.chat-message.user {
  flex-direction: row-reverse;
}
.bubble {
  background: #fff;
  color: #1e293b;
  border-radius: 1.2rem;
  padding: 0.8rem 1.2rem;
  max-width: 70%;
  box-shadow: 0 1px 4px #2563eb11;
  font-size: 1.05rem;
  word-break: break-word;
}
.chat-message.user .bubble {
  background: #2563eb;
  color: #fff;
  border-bottom-right-radius: 0.4rem;
  border-bottom-left-radius: 1.2rem;
}
.chat-message.assistant .bubble {
  background: #fff;
  color: #2563eb;
  border-bottom-left-radius: 0.4rem;
  border-bottom-right-radius: 1.2rem;
}
.typing-bubble {
  background: #f1f5f9 !important;
  color: #64748b !important;
  padding: 0.8rem 1.2rem;
}
.typing-dots {
  display: flex;
  gap: 0.3rem;
}
.typing-dots span {
  width: 8px;
  height: 8px;
  background: #64748b;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}
.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}
.products-suggestions {
  margin-top: 1rem;
  padding: 0.8rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border-left: 3px solid #2563eb;
}
.products-suggestions h4 {
  margin: 0 0 0.5rem 0;
  color: #2563eb;
  font-size: 0.9rem;
}
.product-item {
  font-size: 0.9rem;
  margin: 0.2rem 0;
  color: #374151;
}
.cart-info {
  margin-top: 1rem;
  padding: 0.8rem;
  background: #fef3c7;
  border-radius: 0.5rem;
  border-left: 3px solid #f59e0b;
}
.cart-info h4 {
  margin: 0 0 0.5rem 0;
  color: #92400e;
  font-size: 0.9rem;
}
.cart-item {
  font-size: 0.9rem;
  margin: 0.2rem 0;
  color: #92400e;
}
.cart-total {
  font-weight: bold;
  margin-top: 0.5rem;
  color: #92400e;
}
.image-preview {
  display: flex;
  align-items: center;
  margin-right: 0.5rem;
  position: relative;
}
.image-preview img {
  max-width: 48px;
  max-height: 48px;
  border-radius: 0.5rem;
  box-shadow: 0 1px 4px #2563eb33;
}
.remove-img {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #f87171;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 4px #f87171aa;
}
.bubble.image-bubble {
  padding: 0.5rem;
  background: #fff;
  display: flex;
  align-items: center;
}
.bubble.image-bubble img {
  max-width: 180px;
  max-height: 120px;
  border-radius: 0.7rem;
  box-shadow: 0 1px 4px #2563eb33;
}
.assistant-footer {
  display: flex;
  align-items: center;
  padding: 1.2rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
  gap: 0.5rem;
}
.assistant-input {
  flex: 1 1 auto;
  border: 1px solid #cbd5e1;
  border-radius: 0.75rem;
  padding: 0.7rem 1.2rem;
  font-size: 1.08rem;
  outline: none;
  background: #fff;
  color: #1e293b;
  transition: border 0.2s;
}
.assistant-input:focus {
  border: 1.5px solid #2563eb;
}
.assistant-input:disabled {
  background: #f1f5f9;
  color: #64748b;
  cursor: not-allowed;
}
.icon-btn {
  background: none;
  border: none;
  padding: 0.4rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background 0.15s;
}
.icon-btn:hover:not(:disabled) {
  background: #e0e7ff;
}
.icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.send-btn {
  background: #2563eb;
  color: #fff;
  border-radius: 0.5rem;
  padding: 0.4rem 0.7rem;
  margin-left: 0.2rem;
  transition: background 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.send-btn svg {
  fill: white;
}
.send-btn:hover:not(:disabled) {
  background: #1d4ed8;
}
.send-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}
.recording {
  background: #fee2e2 !important;
}
.mic-anim circle {
  transform-origin: 12px 12px;
}
.mic-denied {
  background: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  margin: 1rem;
  text-align: center;
  font-size: 0.95rem;
  box-shadow: 0 1px 4px #f87171aa;
}
.connection-error {
  background: #fef3c7;
  color: #92400e;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  margin: 1rem;
  text-align: center;
  font-size: 0.95rem;
  box-shadow: 0 1px 4px #f59e0baa;
}
.transcribing-toast {
  position: absolute;
  left: 50%;
  bottom: 110px;
  transform: translateX(-50%);
  background: #2563eb;
  color: #fff;
  padding: 0.7rem 1.5rem;
  border-radius: 1rem;
  font-size: 1rem;
  box-shadow: 0 2px 8px #2563eb33;
  z-index: 3000;
  animation: fadeInOut 2s;
}
@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
@media (max-width: 900px) {
  .assistant-modal.chatbot {
    right: 0.5rem;
    left: 0.5rem;
    width: auto;
    height: 80vh;
    min-height: 350px;
    bottom: 7.5rem;
  }
  .assistant-fab {
    right: 0.5rem;
    bottom: 0.5rem;
  }
}
</style>


    websocket.close()

  }

  if (reconnectTimer) {

    clearTimeout(reconnectTimer)

  }

})

</script>



<style scoped>

.assistant-fab {

  position: fixed;

  bottom: 2rem;

  right: 2rem;

  background: transparent;

  border: none;

  border-radius: 50%;

  width: 80px;

  height: 80px;

  box-shadow: 0 2px 8px rgba(0,0,0,0.15);

  cursor: pointer;

  z-index: 1000;

  display: flex;

  align-items: center;

  justify-content: center;

  transition: box-shadow 0.2s;

}

.assistant-fab:hover {

  box-shadow: 0 4px 16px rgba(37,99,235,0.25);

}

.assistant-overlay {

  position: fixed;

  inset: 0;

  background: rgba(0,0,0,0.08);

  z-index: 1001;

}

.assistant-modal.chatbot {

  position: fixed;

  bottom: 7.5rem;

  right: 2rem;

  width: 500px;

  max-width: 99vw;

  height: 600px;

  max-height: 90vh;

  background: #fff;

  border-radius: 2rem;

  box-shadow: 0 8px 32px rgba(37,99,235,0.18), 0 1.5px 8px rgba(0,0,0,0.08);

  z-index: 1002;

  display: flex;

  flex-direction: column;

  overflow: hidden;

  animation: assistant-pop 0.18s cubic-bezier(.4,1.4,.6,1) both;

}

@keyframes assistant-pop {

  0% { transform: scale(0.95) translateY(30px); opacity: 0; }

  100% { transform: scale(1) translateY(0); opacity: 1; }

}

.assistant-header {

  display: flex;

  justify-content: space-between;

  align-items: center;

  padding: 1.5rem 2rem;

  border-bottom: 1px solid #e5e7eb;

  background: #f1f5f9;

}

.connection-status {

  display: flex;

  align-items: center;

  gap: 0.5rem;

}

.status-connected {

  color: #10b981;

  font-size: 1.2rem;

}

.status-disconnected {

  color: #ef4444;

  font-size: 1.2rem;

}

.close-btn {

  background: none;

  border: none;

  font-size: 1.25rem;

  color: #2563eb;

  cursor: pointer;

  padding: 0 0.25rem;

  line-height: 1;

}

.assistant-body.chatbot-body {

  padding: 2rem 1.5rem 1rem 1.5rem;

  background: #f8fafc;

  color: #1e293b;

  font-size: 1rem;

  flex: 1 1 auto;

  overflow-y: auto;

  display: flex;

  flex-direction: column;

  gap: 0.7rem;

}

.chat-message {

  display: flex;

  align-items: flex-end;

  gap: 0.7rem;

  margin-bottom: 0.2rem;

}

.chat-message.user {

  flex-direction: row-reverse;

}

.bubble {

  background: #fff;

  color: #1e293b;

  border-radius: 1.2rem;

  padding: 0.8rem 1.2rem;

  max-width: 70%;

  box-shadow: 0 1px 4px #2563eb11;

  font-size: 1.05rem;

  word-break: break-word;

}

.chat-message.user .bubble {

  background: #2563eb;

  color: #fff;

  border-bottom-right-radius: 0.4rem;

  border-bottom-left-radius: 1.2rem;

}

.chat-message.assistant .bubble {

  background: #fff;

  color: #2563eb;

  border-bottom-left-radius: 0.4rem;

  border-bottom-right-radius: 1.2rem;

}

.typing-bubble {

  background: #f1f5f9 !important;

  color: #64748b !important;

  padding: 0.8rem 1.2rem;

}

.typing-dots {

  display: flex;

  gap: 0.3rem;

}

.typing-dots span {

  width: 8px;

  height: 8px;

  background: #64748b;

  border-radius: 50%;

  animation: typing 1.4s infinite ease-in-out;

}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }

.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {

  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }

  40% { transform: scale(1); opacity: 1; }

}

.products-suggestions {

  margin-top: 1rem;

  padding: 0.8rem;

  background: #f8fafc;

  border-radius: 0.5rem;

  border-left: 3px solid #2563eb;

}

.products-suggestions h4 {

  margin: 0 0 0.5rem 0;

  color: #2563eb;

  font-size: 0.9rem;

}

.product-item {

  font-size: 0.9rem;

  margin: 0.2rem 0;

  color: #374151;

}

.cart-info {

  margin-top: 1rem;

  padding: 0.8rem;

  background: #fef3c7;

  border-radius: 0.5rem;

  border-left: 3px solid #f59e0b;

}

.cart-info h4 {

  margin: 0 0 0.5rem 0;

  color: #92400e;

  font-size: 0.9rem;

}

.cart-item {

  font-size: 0.9rem;

  margin: 0.2rem 0;

  color: #92400e;

}

.cart-total {

  font-weight: bold;

  margin-top: 0.5rem;

  color: #92400e;

}

.image-preview {

  display: flex;

  align-items: center;

  margin-right: 0.5rem;

  position: relative;

}

.image-preview img {

  max-width: 48px;

  max-height: 48px;

  border-radius: 0.5rem;

  box-shadow: 0 1px 4px #2563eb33;

}

.remove-img {

  position: absolute;

  top: -8px;

  right: -8px;

  background: #f87171;

  color: #fff;

  border: none;

  border-radius: 50%;

  width: 20px;

  height: 20px;

  font-size: 1rem;

  cursor: pointer;

  display: flex;

  align-items: center;

  justify-content: center;

  box-shadow: 0 1px 4px #f87171aa;

}

.bubble.image-bubble {

  padding: 0.5rem;

  background: #fff;

  display: flex;

  align-items: center;

}

.bubble.image-bubble img {

  max-width: 180px;

  max-height: 120px;

  border-radius: 0.7rem;

  box-shadow: 0 1px 4px #2563eb33;

}

.assistant-footer {

  display: flex;

  align-items: center;

  padding: 1.2rem 1.5rem;

  border-top: 1px solid #e5e7eb;

  background: #f8fafc;

  gap: 0.5rem;

}

.assistant-input {

  flex: 1 1 auto;

  border: 1px solid #cbd5e1;

  border-radius: 0.75rem;

  padding: 0.7rem 1.2rem;

  font-size: 1.08rem;

  outline: none;

  background: #fff;

  color: #1e293b;

  transition: border 0.2s;

}

.assistant-input:focus {

  border: 1.5px solid #2563eb;

}

.assistant-input:disabled {

  background: #f1f5f9;

  color: #64748b;

  cursor: not-allowed;

}

.icon-btn {

  background: none;

  border: none;

  padding: 0.4rem;

  border-radius: 0.5rem;

  cursor: pointer;

  display: flex;

  align-items: center;

  transition: background 0.15s;

}

.icon-btn:hover:not(:disabled) {

  background: #e0e7ff;

}

.icon-btn:disabled {

  opacity: 0.5;

  cursor: not-allowed;

}

.send-btn {

  background: #2563eb;

  color: #fff;

  border-radius: 0.5rem;

  padding: 0.4rem 0.7rem;

  margin-left: 0.2rem;

  transition: background 0.15s;

  display: flex;

  align-items: center;

  justify-content: center;

}

.send-btn svg {

  fill: white;

}

.send-btn:hover:not(:disabled) {

  background: #1d4ed8;

}

.send-btn:disabled {

  background: #94a3b8;

  cursor: not-allowed;

}

.recording {

  background: #fee2e2 !important;

}

.mic-anim circle {

  transform-origin: 12px 12px;

}

.mic-denied {

  background: #fee2e2;

  color: #b91c1c;

  padding: 0.75rem 1rem;

  border-radius: 0.75rem;

  margin: 1rem;

  text-align: center;

  font-size: 0.95rem;

  box-shadow: 0 1px 4px #f87171aa;

}

.connection-error {

  background: #fef3c7;

  color: #92400e;

  padding: 0.75rem 1rem;

  border-radius: 0.75rem;

  margin: 1rem;

  text-align: center;

  font-size: 0.95rem;

  box-shadow: 0 1px 4px #f59e0baa;

}

.transcribing-toast {

  position: absolute;

  left: 50%;

  bottom: 110px;

  transform: translateX(-50%);

  background: #2563eb;

  color: #fff;

  padding: 0.7rem 1.5rem;

  border-radius: 1rem;

  font-size: 1rem;

  box-shadow: 0 2px 8px #2563eb33;

  z-index: 3000;

  animation: fadeInOut 2s;

}

@keyframes fadeInOut {

  0% { opacity: 0; }

  10% { opacity: 1; }

  90% { opacity: 1; }

  100% { opacity: 0; }

}

@media (max-width: 900px) {

  .assistant-modal.chatbot {

    right: 0.5rem;

    left: 0.5rem;

    width: auto;

    height: 80vh;

    min-height: 350px;

    bottom: 7.5rem;

  }

  .assistant-fab {

    right: 0.5rem;

    bottom: 0.5rem;

  }

}

</style>


