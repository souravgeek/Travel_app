import apiClient from '../config/api';

export const generateItinerary = async (location, duration, interests, otherPrefs) => {
  try {
    const response = await apiClient.post('/itinerary', {
      location,
      duration,
      interests,
      other_prefs: otherPrefs,
    });
    return response.data;
  } catch (error) {
    console.error("Error generating itinerary:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchDigitalGuide = async (location, topic) => {
  try {
    const response = await apiClient.get('/guide', {
      params: { location, topic }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching digital guide:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchHiddenGems = async (location, preferences) => {
  try {
    const response = await apiClient.get('/gems', {
      params: { location, preferences }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching hidden gems:", error.response?.data || error.message);
    throw error;
  }
}; 