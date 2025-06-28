import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { generateItinerary } from '../services/travelService';

const ItineraryScreen = () => {
  const [location, setLocation] = useState('');
  const [duration, setDuration] = useState('');
  const [interests, setInterests] = useState('');
  const [otherPrefs, setOtherPrefs] = useState('');
  const [itineraryResult, setItineraryResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!location || !duration || !interests) {
      Alert.alert("Missing Info", "Please fill in Location, Duration, and Interests.");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setItineraryResult(null);

    try {
      const result = await generateItinerary(location, duration, interests, otherPrefs);
      setItineraryResult(result.itinerary);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to generate itinerary. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Itinerary Generator</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Destination (e.g., Bali, Japan)"
        value={location}
        onChangeText={setLocation}
      />
      
      <TextInput
        style={styles.input}
        placeholder="Duration (number of days)"
        value={duration}
        onChangeText={setDuration}
        keyboardType="numeric"
      />
      
      <TextInput
        style={styles.input}
        placeholder="Interests (e.g., beaches, hiking, culture)"
        value={interests}
        onChangeText={setInterests}
      />
      
      <TextInput
        style={styles.input}
        placeholder="Additional Preferences (optional)"
        value={otherPrefs}
        onChangeText={setOtherPrefs}
      />
      
      <Button 
        title="Generate Itinerary" 
        onPress={handleGenerate} 
        disabled={isLoading}
      />
      
      {isLoading && (
        <View style={styles.loader}>
          <ActivityIndicator size="large" color="#0000ff" />
          <Text>Generating your perfect itinerary...</Text>
        </View>
      )}
      
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
      
      {itineraryResult && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Your Personalized Itinerary</Text>
          <Text style={styles.resultText}>{itineraryResult}</Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: 'stretch',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 15,
    borderRadius: 5,
    fontSize: 16,
  },
  loader: {
    marginTop: 20,
    alignItems: 'center',
  },
  errorText: {
    marginTop: 15,
    color: 'red',
    textAlign: 'center',
  },
  resultContainer: {
    marginTop: 30,
    padding: 15,
    backgroundColor: '#f0f0f0',
    borderRadius: 5,
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  resultText: {
    fontSize: 16,
    lineHeight: 24,
  }
});

export default ItineraryScreen; 