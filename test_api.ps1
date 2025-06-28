# Test root endpoint
Write-Host "Testing root endpoint..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://localhost:5000/" -Method Get

# Test itinerary endpoint
Write-Host "`nTesting itinerary endpoint..." -ForegroundColor Green
$body = @{
    location = "Paris"
    duration = "3"
    interests = "art, food"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/itinerary" -Method Post -ContentType "application/json" -Body $body
$response

# Test guide endpoint
Write-Host "`nTesting guide endpoint..." -ForegroundColor Green
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/guide?location=Rome&topic=history" -Method Get
$response

# Test gems endpoint
Write-Host "`nTesting hidden gems endpoint..." -ForegroundColor Green
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/gems?location=Tokyo&preferences=food" -Method Get
$response 