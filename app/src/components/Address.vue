<template>
  <span :title="fullAddress" class="inline-flex items-center gap-1.5 focus:outline-none">
    <template v-if="profile?.username">
      <img v-if="profile.avatarUrl" :src="profile.avatarUrl" class="w-4 h-4 rounded-full object-cover inline-block border border-white/10" />
      <div v-else class="w-4 h-4 rounded-full bg-gradient-to-tr from-violet-500 to-fuchsia-500 inline-block border border-white/10"></div>
      
      <a v-if="profile.socialUrl" :href="profile.socialUrl" target="_blank" class="hover:underline hover:text-white transition-colors">
        @{{ profile.username }}
      </a>
      <span v-else>@{{ profile.username }}</span>
    </template>
    
    <template v-else>
      <span class="font-mono">{{ shortenedAddress }}</span>
    </template>
  </span>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { getProfile } from '../services/profiles';

const props = defineProps({
  address: {
    type: String,
    required: true,
  },
  maxLength: {
    type: Number,
    default: 12,
  },
});

const profile = ref(null);

const fetchProfile = () => {
  if (!props.address) return;
  profile.value = getProfile(props.address);
};

// Listen for global profile updates so it instantly updates everywhere
const profileUpdatedHandler = (e) => {
  if (e.detail?.address === props.address?.toLowerCase()) {
    profile.value = e.detail.profile;
  }
};

watch(() => props.address, () => {
  fetchProfile();
}, { immediate: true });

onMounted(() => {
  window.addEventListener('profile-updated', profileUpdatedHandler);
});

onUnmounted(() => {
  window.removeEventListener('profile-updated', profileUpdatedHandler);
});

const fullAddress = computed(() => props.address);

const shortenedAddress = computed(() => {
  if (!props.address) return "";
  if (props.address.length <= props.maxLength) return props.address;
  
  const halfLength = Math.floor((props.maxLength - 3) / 2);
  const start = props.address.slice(0, halfLength);
  const end = props.address.slice(-halfLength);
  return `${start}...${end}`;
});
</script>
