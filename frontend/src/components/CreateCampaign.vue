<script setup>

import { ref } from 'vue'
import { useCampaignStore } from '../stores/campaigns'
import router from '../router'

const campaignStore = useCampaignStore()
const campaign = ref({
    name: '',
    description: ''
})

const handleSubmit = () => {
    campaignStore.createCampaign(campaign.value)
    router.push({ name: 'Campaigns' })

}
</script>

<template>
    <div>
        <h1 class="title">Create Campaign</h1>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="name">Name</label>
                <input v-model="campaign.name" type="text" id="name" required />    
        </div>
            <div class="form-group">
                <label for="description">Description</label>
                <textarea v-model="campaign.description" id="description" required></textarea>
            </div>
            <button type="submit" class="btn-primary">Create Campaign</button>
        </form>
    </div>

</template>


<style scoped>

</style>