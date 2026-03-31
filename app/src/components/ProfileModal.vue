<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 overflow-y-auto backdrop-blur-md bg-black/40">
    <div 
      class="glass w-full max-w-lg rounded-[2rem] border border-white/10 dark:border-white/5 shadow-2xl relative overflow-hidden animate-in fade-in zoom-in-95 duration-300"
      @click.stop
    >
      <!-- Background elements -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-violet-500/10 blur-[80px] rounded-full pointer-events-none"></div>

      <div class="p-8 sm:p-10 relative z-10">
        <!-- Header -->
        <div class="flex justify-between items-start mb-8">
          <div>
            <h2 class="text-3xl font-black tracking-tight text-gray-900 dark:text-white">Your Profile</h2>
            <p class="text-gray-500 font-medium mt-1">Personalize your identity on the network.</p>
          </div>
          <button 
            @click="$emit('close')" 
            class="p-2 sm:p-3 hover:bg-black/5 dark:hover:bg-white/5 rounded-2xl text-gray-500 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="save" class="space-y-6">
          <div class="space-y-2">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Display Name</label>
            <input 
              v-model="form.username" 
              required
              placeholder="e.g. Satoshi"
              class="w-full bg-white dark:bg-[#030712] border border-gray-200 dark:border-white/10 rounded-2xl px-5 py-4 focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-white transition-all"
            />
          </div>

          <div class="space-y-4">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Upload Avatar (Optional)</label>
            <div class="flex items-center gap-4">
              <div 
                class="w-16 h-16 rounded-full border-2 border-dashed border-gray-300 dark:border-white/20 flex flex-shrink-0 items-center justify-center overflow-hidden bg-gray-50 dark:bg-[#030712] relative group cursor-pointer"
                @click="fileInput.click()"
              >
                <img v-if="isValidImage" :src="form.avatarUrl" class="w-full h-full object-cover" />
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 group-hover:text-violet-500 transition-colors"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                
                <div class="absolute inset-0 bg-black/50 hidden group-hover:flex items-center justify-center transition-all z-10">
                  <span class="text-[9px] font-black text-white px-2 text-center uppercase tracking-widest">Upload</span>
                </div>
              </div>
              
              <div class="flex-1">
                <input 
                  type="file" 
                  accept="image/*" 
                  class="hidden" 
                  ref="fileInput"
                  @change="handleFileUpload"
                />
                <button 
                  type="button" 
                  @click="fileInput.click()"
                  class="text-xs font-bold text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 px-4 py-2.5 rounded-xl transition-all border border-gray-200 dark:border-white/5"
                >
                  Choose Image...
                </button>
                <button 
                  v-if="form.avatarUrl"
                  type="button" 
                  @click="form.avatarUrl = ''"
                  class="text-xs font-bold text-red-500 hover:text-red-400 ml-3 transition-colors"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Social Link (Optional)</label>
            <input 
              v-model="form.socialUrl" 
              placeholder="https://x.com/username"
              class="w-full bg-white dark:bg-[#030712] border border-gray-200 dark:border-white/10 rounded-2xl px-5 py-4 focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-white text-sm transition-all"
            />
          </div>

          <div class="pt-4">
            <button 
              type="submit" 
              class="w-full btn-primary px-6 py-4 rounded-xl font-black tracking-wide flex justify-center items-center group"
            >
              Save Profile
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="ml-2 group-hover:translate-x-1 transition-transform"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getProfile, saveProfile } from '../services/profiles';

const props = defineProps({
  userAddress: { type: String, required: true }
});

const emit = defineEmits(['close']);

const form = ref({
  username: '',
  avatarUrl: '',
  socialUrl: ''
});

const fileInput = ref(null);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 2 * 1024 * 1024) {
    alert("Image size should be less than 2MB");
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    form.value.avatarUrl = e.target.result;
  };
  reader.readAsDataURL(file);
};

const isValidImage = computed(() => {
  return form.value.avatarUrl.length > 5 && (form.value.avatarUrl.startsWith('http') || form.value.avatarUrl.startsWith('data:image'));
});

onMounted(() => {
  const existing = getProfile(props.userAddress);
  if (existing) {
    form.value.username = existing.username || '';
    form.value.avatarUrl = existing.avatarUrl || '';
    form.value.socialUrl = existing.socialUrl || '';
  }
});

const save = () => {
  const payload = {
    username: form.value.username.trim(),
    avatarUrl: form.value.avatarUrl.trim(),
    socialUrl: form.value.socialUrl.trim()
  };
  
  saveProfile(props.userAddress, payload);
  emit('close');
};
</script>
