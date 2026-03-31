const PROFILES_KEY = "agentic_escrow_profiles";

/**
 * Fetch all profiles from local storage
 */
export const getAllProfiles = () => {
  try {
    const data = localStorage.getItem(PROFILES_KEY);
    return data ? JSON.parse(data) : {};
  } catch (e) {
    console.error("Error reading profiles", e);
    return {};
  }
};

/**
 * Get a specific profile by address
 * @param {string} address The user's GenLayer address
 * @returns {object|null} The profile object or null if not found
 */
export const getProfile = (address) => {
  if (!address) return null;
  const profiles = getAllProfiles();
  return profiles[address.toLowerCase()] || null;
};

/**
 * Save or update a profile
 * @param {string} address The user's GenLayer address
 * @param {object} profileData { username, avatarUrl, socialUrl }
 */
export const saveProfile = (address, profileData) => {
  if (!address) return;
  const profiles = getAllProfiles();
  profiles[address.toLowerCase()] = profileData;
  localStorage.setItem(PROFILES_KEY, JSON.stringify(profiles));
  
  // Dispatch a custom event so other components (like Address.vue) can reactively update
  window.dispatchEvent(new CustomEvent('profile-updated', {
    detail: { address: address.toLowerCase(), profile: profileData }
  }));
};
