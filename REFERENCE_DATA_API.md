# Reference Data API Endpoint

This endpoint provides all reference data for sports and intensity levels used in workout tracking in a **single API call**. **No authentication required**.

## Single Consolidated Endpoint

### Get All Reference Data
**GET** `/api/reference-data/`

Returns all reference data needed for workout tracking in one response. This eliminates the need for multiple API calls.

**Response:**
```json
{
  "sports": [
    {
      "id": 1,
      "name": "Running"
    },
    {
      "id": 2,
      "name": "Cycling"
    },
    {
      "id": 3,
      "name": "Swimming"
    }
  ],
  "intensity_levels": [
    {
      "id": 1,
      "name": "Light"
    },
    {
      "id": 2,
      "name": "Moderate"
    },
    {
      "id": 3,
      "name": "High"
    }
  ],
  "mappings": [
    {
      "sport_id": 1,
      "sport_name": "Running",
      "intensity_id": 1,
      "intensity_name": "Light",
      "km_per_hour": 6.0
    },
    {
      "sport_id": 1,
      "sport_name": "Running",
      "intensity_id": 2,
      "intensity_name": "Moderate",
      "km_per_hour": 9.0
    },
    {
      "sport_id": 1,
      "sport_name": "Running",
      "intensity_id": 3,
      "intensity_name": "High",
      "km_per_hour": 12.0
    },
    {
      "sport_id": 2,
      "sport_name": "Cycling",
      "intensity_id": 1,
      "intensity_name": "Light",
      "km_per_hour": 15.0
    }
  ]
}
```

## Response Structure

The response contains three arrays:

1. **sports**: List of all available sports with their IDs and names
2. **intensity_levels**: List of intensity levels (Light, Moderate, High)
3. **mappings**: All sport-intensity combinations with their km/hour conversion rates

## Usage in Frontend

### Example: Load All Reference Data on App Start

```javascript
// Single API call to get everything needed
const response = await fetch('http://127.0.0.1:8000/api/reference-data/');
const refData = await response.json();

// Store in your state management (Redux, Context, etc.)
const { sports, intensity_levels, mappings } = refData;

// Populate sport dropdown
const sportOptions = sports.map(sport => ({
  value: sport.id,
  label: sport.name
}));

// Populate intensity dropdown
const intensityOptions = intensity_levels.map(intensity => ({
  value: intensity.id,
  label: intensity.name
}));
```

### Example: Calculate Estimated Distance

```javascript
// User selects: Running (id=1), High intensity (id=3), 30 minutes
const sportId = 1;
const intensityId = 3;
const timeInMinutes = 30;

// Find the mapping using the flattened structure
const mapping = refData.mappings.find(m => 
  m.sport_id === sportId && m.intensity_id === intensityId
);

// Calculate distance
if (mapping) {
  const estimatedDistance = (mapping.km_per_hour * timeInMinutes) / 60;
  console.log(`Estimated distance: ${estimatedDistance} km`);
  // Output: Estimated distance: 6 km
}
```

### Example: Cache Reference Data

```javascript
// Load once on app initialization and cache
let cachedReferenceData = null;

async function getReferenceData() {
  if (cachedReferenceData) {
    return cachedReferenceData;
  }
  
  const response = await fetch('http://127.0.0.1:8000/api/reference-data/');
  cachedReferenceData = await response.json();
  
  // Optional: Store in localStorage for offline access
  localStorage.setItem('referenceData', JSON.stringify(cachedReferenceData));
  
  return cachedReferenceData;
}

// Use throughout your app
const refData = await getReferenceData();
```

## Benefits

✅ **Single API call** instead of 3 separate calls  
✅ **Faster loading** - Reduced network overhead  
✅ **Simplified code** - One fetch instead of three  
✅ **Easier caching** - Single object to cache  
✅ **No authentication required** - Public endpoint  

## Notes

- Data is relatively static and should be cached on the frontend
- Consider loading this data once on app initialization
- Can be stored in localStorage for offline access
- Sports and intensity levels are managed through Django admin
