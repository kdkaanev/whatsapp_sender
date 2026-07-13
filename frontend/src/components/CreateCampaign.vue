<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useCampaignStore } from '../stores/campaigns'
import { useTemplateStore } from '../stores/templates'
import router from '../router'

const campaignStore = useCampaignStore()
const templateStore = useTemplateStore()

const campaign = ref({
  name: '',
  description: '',
  status: 'draft',
  templateId: '',
})

const isSubmitting = ref(false)
const isLoadingTemplates = ref(false)
const templateError = ref('')
const submitError = ref('')
const submitMessage = ref('')

const normalizedTemplates = computed(() =>
  templateStore.templates.map((template) => ({
    ...template,
    name: template.name ?? 'Untitled template',
    content: template.content ?? '',
  })),
)

const selectedTemplate = computed(() => {
  if (!campaign.value.templateId) {
    return null
  }

  return normalizedTemplates.value.find(
    (template) => String(template.id) === String(campaign.value.templateId),
  ) ?? null
})

const selectedTemplatePreview = computed(() => {
  if (!selectedTemplate.value) {
    return 'Choose a saved template to prefill your campaign message.'
  }

  return selectedTemplate.value.content
})

const previewLength = computed(() => campaign.value.description.trim().length)
const previewLines = computed(() => {
  const text = campaign.value.description.trim()
  if (!text) {
    return 0
  }

  return text.split(/\r?\n/).length
})

const loadTemplates = async () => {
  isLoadingTemplates.value = true
  templateError.value = ''

  try {
    await templateStore.getTemplates()
  } catch (error) {
    templateError.value =
      error.response?.data?.error ?? error.message ?? 'Unable to load templates.'
  } finally {
    isLoadingTemplates.value = false
  }
}

onMounted(() => {
  loadTemplates()
})

watch(
  () => campaign.value.templateId,
  (templateId) => {
    if (!templateId) {
      return
    }

    const template = normalizedTemplates.value.find(
      (item) => String(item.id) === String(templateId),
    )

    if (template) {
      campaign.value.description = template.content
    }
  },
)

const applyTemplate = () => {
  if (!selectedTemplate.value) {
    submitError.value = 'Select a template first.'
    return
  }

  campaign.value.description = selectedTemplate.value.content
  submitError.value = ''
  submitMessage.value = `Loaded "${selectedTemplate.value.name}" into the campaign editor.`
}

const resetForm = () => {
  campaign.value = {
    name: '',
    description: '',
    status: 'draft',
    templateId: '',
  }
}

const handleSubmit = async () => {
  const payload = {
    name: campaign.value.name.trim(),
    description: campaign.value.description.trim(),
    status: campaign.value.status,
  }

  if (!payload.name) {
    submitError.value = 'Campaign name is required.'
    submitMessage.value = ''
    return
  }

  if (!payload.description) {
    submitError.value = 'Campaign description is required.'
    submitMessage.value = ''
    return
  }

  isSubmitting.value = true
  submitError.value = ''
  submitMessage.value = ''

  try {
    await campaignStore.createCampaign(payload)
    submitMessage.value = 'Campaign created successfully.'
    resetForm()
    await router.push({ name: 'Campaigns' })
  } catch (error) {
    submitError.value =
      error.response?.data?.message ?? error.message ?? 'Unable to create campaign.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="create-campaign-page">
    <header class="hero">
      <div>
        <p class="eyebrow">Campaign builder</p>
        <h1 class="title">Create Campaign</h1>
        <p class="subtitle">
          Start from a saved template, refine the message, and launch a new campaign.
        </p>
      </div>
    </header>

    <div class="card-grid">
      <article class="metric-card">
        <p class="metric-label">Saved templates</p>
        <p class="metric-value">{{ normalizedTemplates.length }}</p>
        <p class="metric-hint">Available for reuse</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">Message length</p>
        <p class="metric-value">{{ previewLength }}</p>
        <p class="metric-hint">Characters in the campaign body</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">Lines</p>
        <p class="metric-value">{{ previewLines }}</p>
        <p class="metric-hint">Visible message lines</p>
      </article>
    </div>

    <div v-if="templateError" class="notice notice--error">
      {{ templateError }}
    </div>

    <div class="content-grid">
      <form class="form-panel" @submit.prevent="handleSubmit">
        <div class="panel-header">
          <div>
            <p class="panel-eyebrow">Details</p>
            <h2 class="panel-title">Campaign setup</h2>
          </div>
          <button class="btn-secondary" type="button" @click="router.push({ name: 'Campaigns' })">
            Back to Campaigns
          </button>
        </div>

        <div class="form-grid">
          <label class="field field--full">
            <span>Campaign name</span>
            <input v-model="campaign.name" type="text" maxlength="255" placeholder="Spring offer" required />
          </label>

          <label class="field field--full">
            <span>Start from template</span>
            <select v-model="campaign.templateId" :disabled="isLoadingTemplates || normalizedTemplates.length === 0">
              <option value="">No template selected</option>
              <option v-for="template in normalizedTemplates" :key="template.id" :value="String(template.id)">
                {{ template.name }}
              </option>
            </select>
          </label>

          <div class="template-action-row field--full">
            <button class="btn-secondary" type="button" :disabled="!selectedTemplate" @click="applyTemplate">
              Use selected template
            </button>
            <span class="helper-text">
              Pick a template to prefill the campaign message, then edit it if needed.
            </span>
          </div>

          <label class="field field--full">
            <span>Campaign message</span>
            <textarea
              v-model="campaign.description"
              rows="12"
              placeholder="Write the message body or load a template above."
              required
            />
          </label>

          <label class="field field--full">
            <span>Status</span>
            <select v-model="campaign.status">
              <option value="draft">Draft</option>
              <option value="scheduled">Scheduled</option>
            </select>
          </label>

          <div v-if="submitError || submitMessage" class="notice" :class="{ 'notice--error': submitError }">
            {{ submitError || submitMessage }}
          </div>

          <div class="action-row field--full">
            <button class="btn-secondary" type="button" @click="resetForm">Reset</button>
            <button class="btn-primary" type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Creating...' : 'Create Campaign' }}
            </button>
          </div>
        </div>
      </form>

      <aside class="preview-panel">
        <div class="panel-header">
          <div>
            <p class="panel-eyebrow">Preview</p>
            <h2 class="panel-title">Message preview</h2>
          </div>
        </div>

        <div class="preview-card">
          <div class="preview-section">
            <span class="preview-label">Selected template</span>
            <strong>{{ selectedTemplate?.name ?? 'None selected' }}</strong>
          </div>

          <div class="preview-section preview-section--body">
            <span class="preview-label">Body</span>
            <p>{{ selectedTemplatePreview }}</p>
          </div>

          <div class="preview-section preview-section--meta">
            <div>
              <span class="preview-label">Characters</span>
              <strong>{{ previewLength }}</strong>
            </div>
            <div>
              <span class="preview-label">Lines</span>
              <strong>{{ previewLines }}</strong>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.create-campaign-page {
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

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.metric-card,
.form-panel,
.preview-panel,
.preview-card {
  padding: 22px;
  border-radius: 20px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
}

.metric-label,
.preview-label,
.panel-eyebrow {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 600;
}

.metric-value {
  margin: 10px 0 8px;
  font-size: clamp(1.8rem, 2.5vw, 2.4rem);
  font-weight: 800;
  color: #111827;
}

.metric-hint {
  margin: 0;
  color: #1b9a5d;
  font-weight: 600;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
  gap: 20px;
  align-items: start;
}

.form-panel,
.preview-panel {
  display: grid;
  gap: 18px;
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

.field input,
.field select,
.field textarea {
  width: 100%;
  border-radius: 14px;
  border: 1px solid #dbe3ee;
  background: #ffffff;
  padding: 12px 14px;
  font: inherit;
  color: #0f172a;
  outline: none;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.field textarea {
  resize: vertical;
  min-height: 240px;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: #1b9a5d;
  box-shadow: 0 0 0 4px rgba(27, 154, 93, 0.12);
}

.template-action-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.helper-text {
  color: #64748b;
  font-size: 0.9rem;
}

.notice {
  padding: 12px 14px;
  border-radius: 14px;
  background: #ecfdf5;
  color: #166534;
  font-weight: 600;
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

.preview-card {
  padding: 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.preview-section {
  display: grid;
  gap: 8px;
  padding: 14px 0;
  border-bottom: 1px solid #eef2f7;
}

.preview-section:last-child {
  border-bottom: 0;
}

.preview-section--body p {
  margin: 0;
  color: #334155;
  white-space: pre-wrap;
  line-height: 1.7;
}

.preview-section--meta {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.preview-section--meta strong,
.preview-section strong {
  color: #111827;
  font-size: 1.1rem;
}

@media (max-width: 1023px) {
  .hero {
    padding: 20px;
  }

  .card-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 767px) {
  .form-grid,
  .preview-section--meta {
    grid-template-columns: 1fr;
  }

  .panel-header,
  .action-row,
  .template-action-row {
    align-items: stretch;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
