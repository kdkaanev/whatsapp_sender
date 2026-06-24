<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
	email: '',
	password: '',
})

const isLoading = ref(false)
const errorMessage = ref('')

const onSubmit = async () => {
	errorMessage.value = ''
	isLoading.value = true

	try {
		await authStore.login(form.email, form.password)
		router.push('/')
	} catch (error) {
		errorMessage.value =
			error?.detail ||
			error?.message ||
			'Login failed. Please check your credentials.'
	} finally {
		isLoading.value = false
	}
}
</script>

<template>
	<section class="login-card">
		<h2>Sign in</h2>
		<p class="subtitle">Enter your account details to continue.</p>

		<form class="login-form" @submit.prevent="onSubmit">
			<label for="email">Email</label>
			<input
				id="email"
				v-model="form.email"
				type="email"
				autocomplete="email"
				placeholder="you@example.com"
				required
			/>

			<label for="password">Password</label>
			<input
				id="password"
				v-model="form.password"
				type="password"
				autocomplete="current-password"
				placeholder="Your password"
				required
			/>

			<p v-if="errorMessage" class="error">{{ errorMessage }}</p>

			<button type="submit" :disabled="isLoading">
				{{ isLoading ? 'Signing in...' : 'Login' }}
			</button>
		</form>
	</section>
</template>

<style scoped>
.login-card {
	width: 100%;
	max-width: 420px;
	padding: 24px;
	border: 1px solid #e6e5ed;
	border-radius: 12px;
	background: #ffffff;
	box-shadow: 0 8px 24px rgba(17, 10, 33, 0.06);
}

h2 {
	margin: 0 0 8px;
}

.subtitle {
	margin: 0 0 18px;
	color: #5e5a69;
}

.login-form {
	display: flex;
	flex-direction: column;
	gap: 10px;
}

label {
	font-size: 14px;
	font-weight: 600;
}

input {
	width: 100%;
	padding: 10px 12px;
	border: 1px solid #ccc8d8;
	border-radius: 8px;
	outline: none;
	transition: border-color 0.2s ease;
}

input:focus {
	border-color: #2563eb;
}

button {
	margin-top: 8px;
	padding: 11px 14px;
	border: 0;
	border-radius: 8px;
	background: #2563eb;
	color: #ffffff;
	font-weight: 600;
	cursor: pointer;
}

button:disabled {
	opacity: 0.65;
	cursor: not-allowed;
}

.error {
	margin: 4px 0 0;
	color: #c0392b;
	font-size: 14px;
}
</style>
