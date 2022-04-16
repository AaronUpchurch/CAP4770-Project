import os
import json
import csv
import re

def get_country_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        country_id = file_path[-7:-5].upper()
        return data, country_id

def get_country_id_map():
    countries_json_path = os.path.join(os.path.dirname(__file__), 'countries.json')
    with open(countries_json_path) as country_json_file:
        country_map = json.load(country_json_file)
        return country_map
        

def make_new_json(data, country):
    _geography = data.get("Geography")
    _area = _geography.get("Area")
    _people = data.get("People and Society")
    _climate = _geography.get("Climate")
    _population = _people.get("Population")
    _env = data.get("Environment",{})
    _econ = data.get("Economy")
    
    fault = {'fault' : None}
    new_data = {
        "country" : country,
        "total_area_sq_km" : _area.get("total",fault),
        "land_area_sq_km" : _area.get("land",fault),
        "water_area_sq_km" : _area.get("water",fault),
        
        "land_boundaries_km" : _geography.get("Land boundaries",fault).get("total",fault),
        "coastline_km" : _geography.get("Coastline",fault),
        "elevation_mean_m" : _geography.get("Elevation",fault).get("mean elevation",fault),
        "agricultural_land_percent" : _geography.get("Land use",fault).get("agricultural land",fault),
        "forest_land_percent" : _geography.get("Land use",fault).get("forest",fault),
        
        "total_dependency_ratio" : _people.get("Dependency ratios",fault).get("total dependency ratio",fault),
        "youth_dependency_ratio" : _people.get("Dependency ratios",fault).get("youth dependency ratio",fault),
        "elderly_dependency_ratio" : _people.get("Dependency ratios",fault).get("elderly dependency ratio",fault),
        "median_age" : _people.get("Median age",fault).get("total",fault),
        "population_growth_rate" : _people.get("Population growth rate",fault),
        "birth_rate" : _people.get("Birth rate",fault),
        "death_rate" : _people.get("Death rate",fault),
        "net_migration_rate" : _people.get("Net migration rate",fault),
        "urban_population" : _people.get("Urbanization",fault).get("urban population",fault),
        "rate_urbanization" : _people.get("Urbanization",fault).get("rate of urbanization",fault),
        "sex_ratio" : _people.get("Sex ratio",fault).get("total population",fault),
        "maternal_mortality_ratio" : _people.get("Maternal mortality ratio",fault),
        "infant_mortality_rate" : _people.get("Infant mortality rate",fault).get("total",fault),
        "life_expectancy" : _people.get("Life expectancy at birth",fault).get("total population",fault),
        "fertility_rate" : _people.get("Total fertility rate",fault),
        "contraceptive_prevalence" : _people.get("Contraceptive prevalence rate",fault),
        "health_expenditure" : _people.get("Current Health Expenditure",fault),
        "physician_density" : _people.get("Physicians density",fault),
        "education_expenditure" : _people.get("Education expenditures", fault),
        
        "particulate_emisions" : _env.get("Air pollutants",fault).get("particulate matter emissions",fault),
        "methane_emissions" : _env.get("Air pollutants",fault).get("methane emissions",fault),
        "urban_population_percent" : _env.get("Urbanization",fault).get("urban population",fault),
        "urbanization_rate" : _env.get("Urbanization",fault).get("rate of urbanization",fault),
        
        "real_gdp" : _econ.get("Real GDP (purchasing power parity)",fault).get("Real GDP (purchasing power parity) 2020",fault),
        "real_gdp_growth_rate" : _econ.get("Real GDP growth rate",fault).get("Real GDP growth rate 2019",fault),
        "real_gdp_per_capita" : _econ.get("Real GDP per capita",fault).get("Real GDP per capita 2020",fault),
        "gdp" : _econ.get("GDP (official exchange rate)", fault),
        "unemployment_rate" : _econ.get("Unemployment rate", {}).get("Unemployment rate 2019",{}),
        "population_below_poverty_line" : _econ.get("Population below poverty line",{})
    }
    return new_data
        
        
def clean(data):
    powers = {'billion': 10 ** 9, 'million': 10 ** 6}
    
    for k,v in data.items():
        if k == 'country':
            continue
        value = v.get("text")
        if value:
            value = value.replace(',','').replace('%','').replace('$','')
            number_match = re.search(r"([0-9\.]+)\s?(million|billion)", value)
            if number_match:
                number = number_match.group(1)
                magnitude = number_match.group(2)
                value = str(float(number) * powers[magnitude])
            else:
                value = value.split(" ")[0]
            if any(c.isalpha() for c in value):
                value = -1
        else:
            value = -1
        value = float(value)
        data[k] = value
    return data
            
def make_csv(use_unknown_countries=True):
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        country_map = get_country_id_map()
        data_dir_path = os.path.join(os.path.dirname(__file__), 'data')
        region_folders = os.listdir(data_dir_path)
        
        header = False
        for region_folder in region_folders:
            region_path = os.path.join(data_dir_path, region_folder)
            countries = os.listdir(region_path)
            for country in countries:
                country_json, country_id = get_country_json(os.path.join(region_path, country))    
                country_name = country_map.get(country_id, None)
                if not country_name:
                    if not use_unknown_countries:
                        continue
                    else:
                        country_name = country_id
                data = make_new_json(country_json, country_name)
                data = clean(data)
                if not header:
                    header = data.keys()
                    csv_writer.writerow(header)
                    header = True
                content = data.values()
                csv_writer.writerow(content)    

if __name__ == '__main__':
    make_csv()