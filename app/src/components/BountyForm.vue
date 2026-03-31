<template>
  <div class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="glass w-full max-w-lg p-8 rounded-2xl animate-in fade-in zoom-in duration-300">
      <h2 class="text-3xl font-bold mb-6 gradient-text">Create New Bounty</h2>
      
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Requirement (Plain English)</label>
          <textarea 
            v-model="description" 
            placeholder="e.g. Build a Python script that scrapes a URL and summarizes it in 5 sentences..."
            class="w-full h-32 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
          ></textarea>
        </div>
        
        <div class="flex gap-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Reward Amount (GEN)</label>
            <input 
              v-model="amount" 
              type="number"
              placeholder="1.5"
              class="w-full bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
            />
          </div>
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Deadline (Optional)</label>
            <input 
              v-model="deadline" 
              type="datetime-local"
              class="w-full bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
            />
          </div>
        </div>
        
        <div class="flex gap-4 pt-4">
          <button 
            @click="handleSubmit" 
            :disabled="!isValid || loading"
            class="flex-1 btn-primary py-4 rounded-xl font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="spinner border-2 w-5 h-5"></span>
            <span>{{ loading ? 'Creating...' : 'Stake & Post Bounty' }}</span>
          </button>
          <button 
            @click="$emit('close')"
            class="px-6 py-4 bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 text-gray-800 dark:text-white rounded-xl font-bold transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  loading: Boolean
});

const emit = defineEmits(['close', 'create']);

const description = ref('');
const amount = ref('');
const deadline = ref('');

const isValid = computed(() => description.value.length > 10 && amount.value > 0);

const handleSubmit = () => {
  if (isValid.value) {
    let deadlineUnix = null;
    if (deadline.value) {
      deadlineUnix = Math.floor(new Date(deadline.value).getTime() / 1000);
    }
    emit('create', { description: description.value, amount: amount.value, deadline: deadlineUnix });
  }
};
</script>
