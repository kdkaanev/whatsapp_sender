<template>
    <div>
        <h1 class="title">Create Contacts</h1>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="name">Name</label>
                <input v-model="contact.name" type="text" id="name" required />
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input v-model="contact.email" type="email" id="email" required />  
            </div>
            <div class="form-group">
                <label for="phone">Phone</label>
                <input v-model="contact.phone" type="tel" id="phone" required />
            </div>
            <button type="submit" class="btn-primary">Create Contact</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useContactStore } from '../stores/contacts'

const contactStore = useContactStore()
const contact = ref({
  name: '',
  email: '',
  phone: ''
})

const handleSubmit = () => {
    
    contactStore.createContact(contact.value)
    // Reset the form
    contact.value = { name: '', email: '', phone: '' }
  
}

</script>