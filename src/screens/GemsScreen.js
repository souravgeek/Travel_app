import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { fetchHiddenGems } from '../services/travelService';

const GemsScreen = () => {
  const [location, setLocation] = useState('');
  const [preferences, setPreferences] = useState('');
  const [gemsResult, setGemsResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGetGems = async () => {
    if (!location) {
      Alert.alert("Missing Info", "Please fill in Location.");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setGemsResult(null);

    try {
      const result = await fetchHiddenGems(location, preferences);
      setGemsResult(result.gems);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to find hidden gems. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Hidden Gems</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Location (e.g., Prague, Melbourne)"
        value={location}
        onChangeText={setLocation}
      />
      
      <TextInput
        style={styles.input}
        placeholder="Preferences (e.g., food, art, nature) - Optional"
        value={preferences}
        onChangeText={setPreferences}
      />
      
      <Button 
        title="Discover Hidden Gems" 
        onPress={handleGetGems} 
        disabled={isLoading}
      />
      
      {isLoading && (
        <View style={styles.loader}>
          <ActivityIndicator size="large" color="#0000ff" />
          <Text>Finding hidden gems...</Text>
        </View>
      )}
      
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
      
      {gemsResult && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Discovered Hidden Gems</Text>
          <Text style={styles.resultText}>{gemsResult}</Text>
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
  },
});

export default GemsScreen; 