<script setup>
import { ref } from 'vue'
import { useContactStore } from '../stores/contacts'

const contactStore = useContactStore()
const contact = ref({
  name: '',
  email: '',
  phone: '',
})

const isSubmitting = ref(false)
const submitError = ref('')
const submitMessage = ref('')

const resetForm = () => {
  contact.value = { name: '', email: '', phone: '' }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  submitError.value = ''
  submitMessage.value = ''

  try {
    await contactStore.createContact(contact.value)
    submitMessage.value = 'Contact created successfully.'
    resetForm()
  } catch (error) {
    submitError.value =
      error?.response?.data?.message ?? error?.message ?? 'Unable to create contact.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="create-contacts-page">
    <header class="hero">
      <div>
        <p class="eyebrow">Contact management</p>
        <h1 class="title">Create Contact</h1>
        <p class="subtitle">
          Add a new contact by filling in the details below.
        </p>
      </div>
    </header>

    <div class="content-grid">
      <form class="form-panel" @submit.prevent="handleSubmit">
        <div class="panel-header">
          <div>
            <p class="panel-eyebrow">Details</p>
            <h2 class="panel-title">Contact information</h2>
          </div>
        </div>

        <div class="form-grid">
          <label class="field field--full">
            <span>Name</span>
            <input v-model="contact.name" type="text" id="name" placeholder="John Doe" required />
          </label>

          <label class="field field--full">
            <span>Email</span>
            <input v-model="contact.email" type="email" id="email" placeholder="john@example.com" required />
          </label>

          <label class="field field--full">
            <span>Phone</span>
            <input v-model="contact.phone" type="tel" id="phone" placeholder="+1 555 000 0000" required />
          </label>

          <div v-if="submitError || submitMessage" class="notice" :class="{ 'notice--error': submitError }">
            {{ submitError || submitMessage }}
          </div>

          <div class="action-row field--full">
            <button class="btn-secondary" type="button" @click="resetForm">Reset</button>
            <button class="btn-primary" type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Creating...' : 'Create Contact' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.create-contacts-page {
  display: grid;
  gap: 20px;
}

.hero {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 20px;
  padding: 28px;
  border-radius: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f1f7f3 100%);
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

.eyebrow {
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  font-weight: 700;
  color: #1b9a5d;
}

.title {
  margin: 0;
  font-size: clamp(2rem, 3vw, 3rem);
  line-height: 1.05;
  color: #111827;
}

.subtitle {
  max-width: 56ch;
  margin: 12px 0 0;
  color: #4b5563;
  font-size: 1rem;
  line-height: 1.6;
}

.content-grid {
  display: grid;
  gap: 20px;
}

.form-panel {
  padding: 22px;
  border-radius: 20px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
  display: grid;
  gap: 18px;
}

.panel-eyebrow {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 600;
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.panel-title {
  margin: 4px 0 0;
  font-size: 1.35rem;
  color: #111827;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: grid;
  gap: 8px;
}

.field--full {
  grid-column: 1 / -1;
}

.field span {
  font-size: 0.88rem;
  font-weight: 700;
  color: #334155;
}

.field input {
  width: 100%;
  border-radius: 14px;
  border: 1px solid #dbe3ee;
  background: #ffffff;
  padding: 12px 14px;
  font: inherit;
  color: #0f172a;
  outline: none;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
  box-sizing: border-box;
}

.field input:focus {
  border-color: #1b9a5d;
  box-shadow: 0 0 0 4px rgba(27, 154, 93, 0.12);
}

.notice {
  padding: 12px 14px;
  border-radius: 14px;
  background: #ecfdf5;
  color: #166534;
  font-weight: 600;
  grid-column: 1 / -1;
}

.notice--error {
  background: #fef2f2;
  color: #b91c1c;
}

.action-row {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  border: none;
  border-radius: 12px;
  padding: 12px 18px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  background: #1b9a5d;
  color: #fff;
}

.btn-secondary {
  background: #f3f4f6;
  color: #334155;
}

.btn-primary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

@media (max-width: 767px) {
  .hero {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .panel-header,
  .action-row {
    align-items: stretch;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>