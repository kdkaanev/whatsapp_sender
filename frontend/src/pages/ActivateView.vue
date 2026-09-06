<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const success = ref(false)

onMounted(async () => {
    try {
        await axios.get(
            `/api/auth/activate/${route.params.uidb64}/${route.params.token}/`
        )

        success.value = true

    } catch (error) {
        console.error('Activation error:', error)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="activation-page">

        <div v-if="loading">
            <h2>Activating your account...</h2>
            <p>Please wait.</p>
        </div>

        <div v-else-if="success">
            <h2>Account activated! 🎉</h2>

            <p>
                Your CampaignFlow account has been successfully activated.
            </p>

            <button @click="router.push('/login')">
                Go to Login
            </button>
        </div>

        <div v-else>
            <h2>Activation failed</h2>

            <p>
                This activation link is invalid or has expired.
            </p>

            <button @click="router.push('/register')">
                Register again
            </button>
        </div>

    </div>
</template>