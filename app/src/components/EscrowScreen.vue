<template>
  <div class="min-h-screen bg-transparent transition-colors duration-500 selection:bg-violet-500/30">
    <!-- Background Decor -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-violet-600/10 blur-[120px] rounded-full"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-600/10 blur-[120px] rounded-full"></div>
    </div>

    <!-- Navbar -->
    <nav class="glass sticky top-0 z-50 px-8 py-4 flex justify-between items-center mx-4 mt-4 rounded-2xl">
      <div class="flex items-center gap-4 group cursor-pointer">
        <div class="w-12 h-12 bg-gradient-to-br from-violet-600 to-fuchsia-600 rounded-2xl flex items-center justify-center font-bold text-2xl shadow-lg shadow-violet-500/20 group-hover:scale-110 transition-transform">Æ</div>
        <div class="flex flex-col">
          <h1 class="text-2xl font-black tracking-tight gradient-text leading-tight">Agentic Escrow</h1>
          <span class="text-[10px] uppercase tracking-[0.2em] text-gray-500 font-bold">Studionet</span>
        </div>
      </div>
      
      <div class="flex items-center gap-6">
        <div v-if="userAddress" class="flex gap-3 sm:gap-4 items-center glass !rounded-2xl px-5 py-2 hover:!border-violet-500/50 transition-all backdrop-blur-xl">
          <div class="flex flex-col items-end cursor-pointer group/profile pr-1" @click="showProfileModal = true" title="Edit Profile">
            <span class="text-[9px] text-gray-500 dark:text-gray-400/80 font-black uppercase tracking-[0.2em] group-hover/profile:text-violet-500 dark:group-hover/profile:text-violet-400 transition-colors mb-0.5">Profile</span>
            <Address :address="userAddress" class="text-sm font-mono font-bold text-gray-900 dark:text-gray-100 group-hover/profile:text-violet-600 dark:group-hover/profile:text-violet-300 transition-colors" />
          </div>
          
          <div class="h-8 w-px bg-gray-200 dark:bg-white/10 mx-1"></div>
          
          <button @click="toggleTheme" class="p-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg text-gray-600 dark:text-gray-400 transition-all group" title="Toggle Theme">
            <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:text-yellow-400 transition-colors"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:text-amber-500 transition-colors"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
          </button>
          
          <button @click="disconnect" class="p-2 hover:bg-red-500/10 rounded-lg text-red-500 transition-all group" title="Disconnect">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-1 transition-transform"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          </button>
        </div>
        <button v-else @click="connect" class="btn-primary px-8 py-3 rounded-xl font-bold tracking-wide shadow-lg shadow-violet-500/10">
          Connect Identity
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 max-w-5xl mx-auto px-6 py-20">
      <!-- Welcome Header -->
      <header class="mb-20 text-center">
        <div class="inline-block px-4 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-xs font-bold uppercase tracking-widest mb-6 animate-bounce-slow">
          Decentralized AI Arbitration
        </div>
        <h2 class="text-7xl font-black mb-8 tracking-tighter leading-[1.1]">
          The Future of <br/>
          <span class="gradient-text">Autonomous Work</span>
        </h2>
        <p class="text-gray-400 text-xl max-w-2xl mx-auto leading-relaxed">
          The first escrow platform where AI agents act as incorruptible judges. 
          Post requirements in natural language and let consensus handle the rest.
        </p>
      </header>

      <!-- Network Stats Dashboard -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-24">
        <div class="glass p-8 rounded-3xl border border-white/5 hover:border-violet-500/20 transition-all group">
          <div class="flex justify-between items-start mb-4">
            <div class="p-3 bg-violet-500/10 rounded-2xl text-violet-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
            </div>
            <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">Protocol State</span>
          </div>
          <div class="text-3xl font-black mb-1 tracking-tight">{{ totalStaked }} <span class="text-sm font-bold text-gray-500">GEN</span></div>
          <p class="text-xs text-gray-500 font-medium uppercase tracking-wider">Total Value Locked</p>
        </div>

        <div class="glass p-8 rounded-3xl border border-white/5 hover:border-emerald-500/20 transition-all group">
          <div class="flex justify-between items-start mb-4">
            <div class="p-3 bg-emerald-500/10 rounded-2xl text-emerald-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            </div>
            <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">Efficiency</span>
          </div>
          <div class="text-3xl font-black mb-1 tracking-tight">{{ completedBounties }}</div>
          <p class="text-xs text-gray-500 font-medium uppercase tracking-wider">Bounties Resolved</p>
        </div>

        <div class="glass p-8 rounded-3xl border border-white/5 hover:border-fuchsia-500/20 transition-all group">
          <div class="flex justify-between items-start mb-4">
            <div class="p-3 bg-fuchsia-500/10 rounded-2xl text-fuchsia-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
            </div>
            <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">Consensus</span>
          </div>
          <div class="text-3xl font-black mb-1 tracking-tight">{{ activeReviews }}</div>
          <p class="text-xs text-gray-500 font-medium uppercase tracking-wider">AI Agents Analyzing</p>
        </div>
      </div>

      <!-- Bounty Feed -->
      <section id="feed" class="space-y-8 scroll-mt-32">
        <div class="flex justify-between items-end border-b border-white/5 pb-6">
          <div>
            <h3 class="text-3xl font-black tracking-tight">Active Opportunities</h3>
            <p class="text-gray-500 mt-1 text-sm">Verified tasks waiting for your expertise.</p>
          </div>
          <div class="flex gap-3">
            <div class="glass flex items-center px-4 py-2 rounded-xl text-xs font-bold text-gray-400">
              <span class="w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"></span>
              {{ bounties.length }} Bounties Online
            </div>
            <button @click="loadData" class="glass p-2.5 rounded-xl text-gray-400 hover:text-white group">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" :class="{ 'animate-spin': loading }" class="group-hover:rotate-180 transition-transform duration-500"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><polyline points="21 3 21 8 16 8"/></svg>
            </button>
          </div>
        </div>

        <div class="flex gap-2 mb-8 overflow-x-auto pb-4 scrollbar-hide">
          <button @click="filterStatus = 'all'" :class="filterStatus === 'all' ? 'bg-violet-600 text-white shadow-lg shadow-violet-500/20' : 'bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-gray-600 dark:text-gray-400'" class="px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-[0.15em] transition-all whitespace-nowrap border border-black/5 dark:border-white/5">📋 All</button>
          <button @click="filterStatus = 'open'" :class="filterStatus === 'open' ? 'bg-violet-500 text-white shadow-lg shadow-violet-500/20' : 'bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-gray-600 dark:text-gray-400'" class="px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-[0.15em] transition-all whitespace-nowrap border border-black/5 dark:border-white/5">🔓 Open</button>
          <button @click="filterStatus = 'review'" :class="filterStatus === 'review' ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/20' : 'bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-gray-600 dark:text-gray-400'" class="px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-[0.15em] transition-all whitespace-nowrap border border-black/5 dark:border-white/5">⚖️ In Review</button>
          <button @click="filterStatus = 'completed'" :class="filterStatus === 'completed' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-gray-600 dark:text-gray-400'" class="px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-[0.15em] transition-all whitespace-nowrap border border-black/5 dark:border-white/5">✅ Completed</button>
          <button v-if="userAddress" @click="filterStatus = 'mine'" :class="filterStatus === 'mine' ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/20 border-blue-400/50' : 'bg-blue-500/5 dark:bg-blue-500/10 hover:bg-blue-500/10 dark:hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 border border-blue-500/20'" class="px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-[0.15em] transition-all whitespace-nowrap lg:ml-auto">👤 My Bounties</button>
        </div>

        <div v-if="loading && bounties.length === 0" class="flex flex-col items-center py-32 gap-6">
          <div class="spinner w-12 h-12"></div>
          <div class="flex flex-col items-center">
            <h4 class="text-lg font-bold text-gray-300">Synchronizing GenVM</h4>
            <p class="text-sm text-gray-500">Crawling intelligent contract state...</p>
          </div>
        </div>

        <div v-else-if="sortedBounties.length === 0" class="glass p-20 text-center rounded-[2.5rem] border-dashed border-2 border-black/10 dark:border-white/5">
          <div class="text-gray-600 mb-2 italic text-2xl font-bold">{{ filterStatus === 'all' ? 'Market is quiet.' : 'No matches found.' }}</div>
          <p class="text-gray-500 max-w-sm mx-auto">{{ filterStatus === 'all' ? 'Be the pioneer of the agentic economy and post the first bounty!' : 'Try switching your filter or creating a new bounty.' }}</p>
          <button v-if="filterStatus === 'all'" @click="showCreateModal = true" class="mt-8 text-violet-600 dark:text-violet-400 font-bold hover:underline">Get started →</button>
          <button v-else @click="filterStatus = 'all'" class="mt-8 text-violet-600 dark:text-violet-400 font-bold hover:underline">Clear Filter</button>
        </div>

        <div v-else class="grid gap-6">
          <BountyCard 
            v-for="bounty in sortedBounties" 
            :key="bounty.id" 
            :bounty="bounty"
            :submissions="submissions[bounty.id] || []"
            :user-address="userAddress"
            :loading="loading"
            class="animate-in fade-in slide-in-from-bottom-10 duration-700 fill-mode-both"
            @submit="handleWorkSubmission"
            @evaluate="handleEvaluation"
            @cancel="handleCancelBounty"
          />
        </div>
      </section>
    </main>

    <!-- Create Bounty Modal -->
    <BountyForm v-if="showCreateModal" :loading="loading" @close="showCreateModal = false" @create="handleCreateBounty" />

    <!-- Profile Edit Modal -->
    <ProfileModal 
      v-if="showProfileModal" 
      :user-address="userAddress" 
      @close="showProfileModal = false" 
    />

    <!-- Overlay Notifications -->
    <Transition name="notification">
      <div v-if="txStatus" class="fixed bottom-10 right-10 z-[100]">
        <div class="glass p-6 rounded-3xl border-violet-500/30 flex items-center gap-5 shadow-2xl shadow-violet-500/20 max-w-sm">
          <div v-if="txLoading" class="spinner w-6 h-6 border-[3px]"></div>
          <div v-else class="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center text-xl shadow-lg shadow-emerald-500/20">✨</div>
          <div class="flex-1">
            <div class="font-black text-sm tracking-tight">{{ txTitle }}</div>
            <div class="text-[11px] text-gray-400 font-medium uppercase tracking-wider mt-1">{{ txStatus }}</div>
          </div>
          <button @click="txStatus = null" class="p-2 hover:bg-white/5 rounded-xl text-gray-500 transition-all">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { account, createAccount, removeAccount } from "../services/genlayer";
import AgenticEscrow from "../logic/AgenticEscrow";
import Address from "./Address.vue";
import BountyCard from "./BountyCard.vue";
import BountyForm from "./BountyForm.vue";
import ProfileModal from "./ProfileModal.vue";

// GenLayer Core
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const studioUrl = import.meta.env.VITE_STUDIO_URL;
const userAccount = ref(account);
const userAddress = computed(() => userAccount.value?.address);
const escrow = new AgenticEscrow(contractAddress, account, studioUrl);

// State
const bounties = ref([]);
const submissions = ref({});
const loading = ref(false);
const showCreateModal = ref(false);
const showProfileModal = ref(false);
const filterStatus = ref('all');

const isDark = ref(localStorage.getItem('theme') !== 'light');
const toggleTheme = () => {
  isDark.value = !isDark.value;
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
  if (isDark.value) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
};

// UI Notifications
const txStatus = ref(null);
const txTitle = ref("");
const txLoading = ref(false);

// Computeds
const sortedBounties = computed(() => {
  let list = bounties.value;
  
  if (filterStatus.value === 'open') {
    list = list.filter(b => b.status === 0);
  } else if (filterStatus.value === 'review') {
    list = list.filter(b => b.status === 1);
  } else if (filterStatus.value === 'completed') {
    list = list.filter(b => b.status === 2);
  } else if (filterStatus.value === 'mine' && userAddress.value) {
    list = list.filter(b => 
      b.client.toLowerCase() === userAddress.value.toLowerCase() || 
      (b.freelancer && b.freelancer.toLowerCase() === userAddress.value.toLowerCase())
    );
  }
  
  return [...list].sort((a, b) => Number(b.id) - Number(a.id));
});

const totalStaked = computed(() => {
  const totalWei = bounties.value.reduce((sum, b) => sum + BigInt(b.reward), BigInt(0));
  return Number(totalWei).toFixed(1);
});

const completedBounties = computed(() => {
  return bounties.value.filter(b => b.status === 2).length;
});

const activeReviews = computed(() => {
  return bounties.value.filter(b => b.status === 1).length;
});

// Auth
const connect = () => {
  userAccount.value = createAccount();
  escrow.updateAccount(userAccount.value);
};

const disconnect = () => {
  userAccount.value = null;
  removeAccount();
};

// Data Fetching
const loadData = async () => {
  loading.value = true;
  try {
    const list = await escrow.getAllBounties();
    bounties.value = list;
    
    // Load submissions for each bounty
    for (const b of list) {
       submissions.value[b.id] = await escrow.getSubmissions(b.id);
    }
  } catch (e) {
    console.error("Fetch failed", e);
  } finally {
    loading.value = false;
  }
};

// Transaction Handlers
const notify = (title, status, isLoading = false) => {
  txTitle.value = title;
  txStatus.value = status;
  txLoading.value = isLoading;
};

const handleCreateBounty = async ({ description, amount, deadline }) => {
  loading.value = true;
  let finalDescription = description.trim();
  if (deadline) finalDescription += ` ||DEADLINE:${deadline}||`;

  notify("Posting Bounty", "Submitting to GenVM...", true);
  try {
    await escrow.createBounty(finalDescription, amount);
    notify("Bounty Created", "Bounty posted on-chain!");
    showCreateModal.value = false;
    await loadData();
  } catch (e) {
    notify("Error", e.message);
  } finally {
    loading.value = false;
  }
};

const handleWorkSubmission = async ({ id, url }) => {
  notify("Submitting Work", "Proof link pending...", true);
  try {
    await escrow.submitWork(id, url);
    notify("Work Submitted", "Evaluating submission...");
    await handleEvaluation({ id, url }); // Auto-trigger evaluation for better DX
  } catch (e) {
    notify("Error", e.message);
  }
};

const handleEvaluation = async ({ id, url }) => {
  notify("AI Arbiter Reasoning", "Reaching Consensus...", true);
  try {
    await escrow.evaluateSubmission(id, url);
    notify("Evaluation Complete", "Consensus reached!");
    await loadData();
  } catch (e) {
    notify("Error", e.message);
  }
};

const handleCancelBounty = async (id) => {
  notify("Cancelling", "Processing refund...", true);
  try {
    await escrow.cancelBounty(id);
    notify("Cancelled", "Bounty removed, funds returned.");
    await loadData();
  } catch (e) {
    notify("Error", e.message);
  }
};

onMounted(() => {
  if (isDark.value) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
  loadData();
});
</script>

<style scoped>
.bounce-slow {
  animation: bounce 3s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.notification-enter-from {
  opacity: 0;
  transform: translateX(100px) scale(0.9);
}
.notification-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
