<template>
  <div class="glass p-8 rounded-[2rem] mb-6 transition-all hover:scale-[1.01] hover:shadow-2xl hover:shadow-violet-500/10 group relative overflow-hidden">
    <!-- Status Indicator Line -->
    <div :class="statusBgClass" class="absolute left-0 top-0 bottom-0 w-1.5 opacity-60"></div>

    <div class="flex flex-col md:flex-row justify-between items-start gap-8">
      <div class="flex-1">
        <div class="flex items-center gap-4 mb-4">
          <span :class="statusBadgeClass" class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.15em] border border-black/5 dark:border-white/5">
            {{ statusText }}
          </span>
          <span class="text-gray-500 text-xs font-bold font-mono">ID // {{ bounty.id }}</span>
          <span v-if="timeRemainingText" :class="isExpired ? 'text-red-500 bg-red-500/10 border-red-500/20' : 'text-amber-500 bg-amber-500/10 border-amber-500/20'" class="px-3 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border ml-3 flex items-center gap-1.5 inline-flex">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ timeRemainingText }}
          </span>
        </div>
        
        <h3 class="text-2xl font-bold mb-4 leading-snug group-hover:text-violet-900 dark:hover:text-violet-100 transition-colors">
          {{ parsedData.cleanDescription }}
        </h3>

        <div class="flex flex-wrap items-center gap-6 text-xs font-bold uppercase tracking-widest text-gray-500">
          <div class="flex items-center gap-2">
            <span class="text-violet-500/50">Creator</span>
            <Address :address="bounty.client" class="text-gray-700 dark:text-gray-300 hover:text-violet-400 transition-colors cursor-pointer" />
          </div>
          <div v-if="hasFreelancer" class="flex items-center gap-2">
            <span class="text-emerald-500/50">Winner</span>
            <Address :address="bounty.freelancer" class="text-gray-700 dark:text-gray-300" />
          </div>
        </div>
      </div>

      <div class="bg-black/5 dark:bg-white/5 p-6 rounded-3xl border border-black/5 dark:border-white/5 text-center min-w-[160px] backdrop-blur-md">
        <div class="text-[10px] text-gray-500 font-black uppercase tracking-widest mb-1">Locked Reward</div>
        <div class="text-3xl font-black gradient-text">{{ formatAmount(bounty.reward) }}</div>
        <div class="text-[10px] text-violet-500 font-bold uppercase tracking-widest mt-1">GEN Tokens</div>
      </div>
    </div>

    <!-- Interaction Area -->
    <div class="mt-10 flex flex-col md:flex-row gap-4 pt-8 border-t border-black/5 dark:border-white/5">
      <!-- Submission Input -->
      <div v-if="canSubmit" class="flex-1 flex gap-3">
        <div class="relative flex-1">
          <input 
            v-model="submissionUrl" 
            placeholder="GitHub Raw URL / Production Link"
            class="w-full bg-[#030712] border border-white/10 rounded-2xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-sm font-medium transition-all placeholder:text-gray-600"
          />
        </div>
        <button 
          @click="submitWork" 
          :disabled="!isValidUrl || loading || isExpired"
          class="btn-primary px-8 rounded-2xl font-black text-sm uppercase tracking-wider disabled:opacity-30 disabled:grayscale transition-all"
        >
          {{ isExpired ? 'Expired' : 'Submit' }}
        </button>
      </div>

      <div class="flex items-center gap-3">
        <button 
          @click="showSubmissions = !showSubmissions"
          class="px-6 py-4 bg-black/5 dark:bg-white/5 hover:bg-white/10 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border border-black/5 dark:border-white/5"
        >
          {{ showSubmissions ? 'Close Review' : 'History (' + bounty.submissions_count + ')' }}
        </button>

        <button 
          v-if="isOwner && isOpen"
          @click="$emit('cancel', bounty.id)"
          class="px-6 py-4 border border-red-500/30 hover:bg-red-500/10 text-red-500 rounded-2xl text-xs font-black uppercase tracking-widest transition-all"
        >
          Retract
        </button>
      </div>
    </div>

    <!-- Submission History (AI Review Logs) -->
    <Transition name="expand">
      <div v-if="showSubmissions" class="mt-8 space-y-4 overflow-hidden">
        <div v-if="submissions.length === 0" class="flex flex-col items-center py-12 bg-black/20 rounded-3xl border border-dashed border-black/5 dark:border-white/5">
          <p class="text-gray-500 text-sm font-medium italic">No evaluation logs found in the GenVM state.</p>
        </div>
        
        <div v-for="(sub, i) in submissions" :key="i" class="bg-white/[0.02] p-6 rounded-3xl border border-black/5 dark:border-white/5 hover:bg-white/[0.04] transition-colors group/sub">
          <div class="flex flex-col sm:flex-row justify-between items-start gap-4 mb-4">
            <div class="flex items-center gap-4">
              <div :class="subCategoryBgClass(sub.category)" class="px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest">
                {{ subCategoryText(sub.category) }}
              </div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Node Proof</span>
                <Address :address="sub.freelancer" class="text-xs font-mono text-gray-400" />
              </div>
            </div>
            <a :href="sub.url" target="_blank" class="text-[10px] font-black uppercase tracking-widest text-violet-400 hover:text-white transition-colors bg-violet-500/5 px-3 py-1.5 rounded-xl border border-violet-500/10">Inspect Artifact →</a>
          </div>
          
          <div class="space-y-4">
            <div class="flex gap-4">
               <div class="w-1 bg-gray-300 dark:bg-white/5 rounded-full"></div>
               <div class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed py-1 prose dark:prose-invert max-w-none prose-p:my-1 prose-headings:my-2 prose-ol:my-1 prose-ul:my-1" v-html="renderMarkdown(sub.reason)"></div>
            </div>

            <!-- AI Consensus Feedback -->
            <div v-if="sub.feedback" class="ml-5 bg-violet-50 dark:bg-violet-500/[0.03] border border-violet-200 dark:border-violet-500/10 p-4 rounded-2xl relative overflow-hidden">
              <div class="absolute top-0 right-0 p-2 opacity-10">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
              </div>
              <div class="flex items-center gap-2 mb-2 text-violet-600 dark:text-violet-400">
                <span class="text-[9px] font-black uppercase tracking-[0.2em]">Consensus Feedback</span>
              </div>
              <div class="text-[13px] text-violet-900 dark:text-violet-200/80 prose dark:prose-invert prose-sm max-w-none prose-p:my-1 prose-headings:my-2 prose-ol:my-1 prose-ul:my-1" v-html="renderMarkdown(sub.feedback)"></div>
            </div>
          </div>

          <!-- Re-evaluation if needed -->
          <div v-if="sub.category !== 0 && canSubmit" class="mt-6 pt-4 border-t border-black/5 dark:border-white/5 flex justify-end">
            <button 
              @click="evaluate(sub.url)"
              class="px-4 py-2 text-[9px] font-black uppercase tracking-widest text-gray-500 hover:text-violet-400 hover:bg-violet-500/5 rounded-xl border border-black/5 dark:border-white/5 hover:border-violet-500/20 transition-all"
            >
              Request AI Re-evaluation
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import Address from './Address.vue';

const props = defineProps({
  bounty: Object,
  submissions: Array,
  userAddress: String,
  loading: Boolean
});

const emit = defineEmits(['submit', 'evaluate', 'cancel']);

const renderMarkdown = (text) => {
  if (!text) return '';
  return DOMPurify.sanitize(marked.parse(text));
};

const submissionUrl = ref('');
const showSubmissions = ref(false);

const statusText = computed(() => {
  const codes = { 0: 'Open Bounty', 1: 'Analyzing', 2: 'Goal Reached', 3: 'Withdrawn' };
  return codes[props.bounty.status] || 'Unknown';
});

const statusBadgeClass = computed(() => {
  const classes = {
    0: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
    1: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    2: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    3: 'bg-red-500/10 text-red-500 border-red-500/20'
  };
  return classes[props.bounty.status] || 'bg-gray-500/10 text-gray-400';
});

const statusBgClass = computed(() => {
  const classes = { 0: 'bg-violet-600', 1: 'bg-amber-500', 2: 'bg-emerald-500', 3: 'bg-red-500' };
  return classes[props.bounty.status] || 'bg-gray-600';
});

const isOpen = computed(() => props.bounty.status === 0 || props.bounty.status === 1);

const parsedData = computed(() => {
  const desc = props.bounty.description;
  const match = desc.match(/\|\|DEADLINE:(\d+)\|\|/);
  if (match) {
    return {
      cleanDescription: desc.replace(match[0], '').trim(),
      deadline: parseInt(match[1], 10)
    };
  }
  return { cleanDescription: desc, deadline: null };
});

const isExpired = computed(() => {
  if (!parsedData.value.deadline) return false;
  return Date.now() / 1000 > parsedData.value.deadline;
});

const timeRemainingText = computed(() => {
  if (!parsedData.value.deadline) return null;
  const now = Date.now() / 1000;
  const diff = parsedData.value.deadline - now;
  
  if (diff <= 0) return 'Expired';
  
  const days = Math.floor(diff / (24 * 3600));
  if (days > 0) return `${days}d left`;
  
  const hours = Math.floor(diff / 3600);
  if (hours > 0) return `${hours}h left`;
  
  const minutes = Math.floor(diff / 60);
  return `${minutes}m left`;
});

const canSubmit = computed(() => isOpen.value && props.userAddress && !isExpired.value);
const isOwner = computed(() => props.bounty.client.toLowerCase() === props.userAddress?.toLowerCase());
const hasFreelancer = computed(() => props.bounty.freelancer !== '0x0000000000000000000000000000000000000000');
const isValidUrl = computed(() => submissionUrl.value.length > 5);

const formatAmount = (amt) => {
  return (Number(amt) / 1e18).toFixed(2);
};

const subCategoryText = (cat) => {
  return { 0: 'Artifact Verified', 1: 'Fault Detected', 2: 'Critial Failure' }[cat] || 'Rejected';
};

const subCategoryBgClass = (cat) => {
  return { 
    0: 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20', 
    1: 'bg-amber-500/10 text-amber-500 border border-amber-500/20', 
    2: 'bg-red-500/10 text-red-500 border border-red-500/20' 
  }[cat] || 'bg-gray-500/10 text-gray-500';
};

const submitWork = () => {
  if (isValidUrl.value) {
    emit('submit', { id: props.bounty.id, url: submissionUrl.value });
    submissionUrl.value = '';
  }
};

const evaluate = (url) => {
  emit('evaluate', { id: props.bounty.id, url });
};
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 1000px;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-20px);
}
</style>
