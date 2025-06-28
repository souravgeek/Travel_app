import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import ItineraryScreen from '../screens/ItineraryScreen';
import GuideScreen from '../screens/GuideScreen';
import GemsScreen from '../screens/GemsScreen';

const Tab = createBottomTabNavigator();

const AppNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Itinerary') {
            iconName = focused ? 'map' : 'map-outline';
          } else if (route.name === 'Guide') {
            iconName = focused ? 'book' : 'book-outline';
          } else if (route.name === 'Gems') {
            iconName = focused ? 'diamond' : 'diamond-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#5048E5',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen 
        name="Itinerary" 
        component={ItineraryScreen} 
        options={{ 
          title: 'Plan Trip',
          headerShown: true,
          headerStyle: {
            backgroundColor: '#5048E5',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      />
      <Tab.Screen 
        name="Guide" 
        component={GuideScreen} 
        options={{ 
          title: 'Digital Guide',
          headerShown: true,
          headerStyle: {
            backgroundColor: '#5048E5',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      />
      <Tab.Screen 
        name="Gems" 
        component={GemsScreen} 
        options={{ 
          title: 'Hidden Gems',
          headerShown: true,
          headerStyle: {
            backgroundColor: '#5048E5',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      />
    </Tab.Navigator>
  );
};

export default AppNavigator; 