import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { fetchDigitalGuide } from '../services/travelService';

const GuideScreen = () => {
  const [location, setLocation] = useState('');
  const [topic, setTopic] = useState('');
  const [guideResult, setGuideResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGetGuide = async () => {
    if (!location || !topic) {
      Alert.alert("Missing Info", "Please fill in Location and Topic.");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setGuideResult(null);

    try {
      const result = await fetchDigitalGuide(location, topic);
      setGuideResult(result.guide_info);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch guide information. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Digital Guide</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Location (e.g., Kyoto, Rome)"
        value={location}
        onChangeText={setLocation}
      />
      
      <TextInput
        style={styles.input}
        placeholder="Topic (e.g., temples, markets, museums)"
        value={topic}
        onChangeText={setTopic}
      />
      
      <Button 
        title="Get Guide Information" 
        onPress={handleGetGuide} 
        disabled={isLoading}
      />
      
      {isLoading && (
        <View style={styles.loader}>
          <ActivityIndicator size="large" color="#0000ff" />
          <Text>Fetching guide information...</Text>
        </View>
      )}
      
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
      
      {guideResult && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Your Digital Guide</Text>
          <Text style={styles.resultText}>{guideResult}</Text>
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

export default GuideScreen; 