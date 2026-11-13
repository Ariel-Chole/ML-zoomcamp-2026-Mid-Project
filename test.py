import requests

url = url = "http://localhost:9696/life_expectancy"

sample_data = {
    "country": "Eritrea",
    "year": 2003,
    "status": "Developing",
    "adult_mortality": 343.0,
    "infant_deaths": 7,
    "alcohol": 0.56,
    "percentage_expenditure": 6.913998013,
    "hepatitis_b": 91.0,
    "measles": 376,
    "bmi": 13.3,
    "under-five_deaths": 10,
    "polio": 95.0,
    "total_expenditure": 3.5,
    "diphtheria": 93.0,
    "hiv/aids": 1.9,
    "gdp": 232.7945459,
    "population": 3738265.0,
    "thinness__1-19_years": 9.7,
    "thinness_5-9_years": 9.7,
    "income_composition_of_resources": 0.0,
    "schooling": 4.7
}

response = requests.post(url, json=sample_data)
print("Status Code:", response.status_code)
print("Response:", response.json())