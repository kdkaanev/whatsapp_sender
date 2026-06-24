<script setup >
import { h } from 'vue';

</script>

<template>
    <div>
        <h1>WhatsApp Outreach Hub</h1>
        <h2>Reach your customers with WhatsApp campaigns in minutes</h2>
        <p>Import contacts, create campaigns, track delivery, and automate communication with ease.</p>

        <button @click="$router.push('/login')">Get Started</button>
        <button @click="$router.push('/register')">Sign Up</button>  
    </div>
</template>