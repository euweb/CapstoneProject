# Table visit

| Column                 | Dtype        | Description                                                                           |
|------------------------|--------------|---------------------------------------------------------------------------------------|
| year_of_arrival        | SMALLINT     | 4 digit year                                                                          |
| month_of_arrival       | SMALLINT     | numeric month                                                                         |
| country_of_citizenship | INTEGER      | 3 digit country code                                                                  |
| country_of_residence   | INTEGER      | 3 digit country code                                                                  |
| port_of_entry          | varchar(256) | 3 chars port                                                                          |
| arrival_date           | DATE         | date of arrival                                                                       |
| arrivid_by             | INTEGER      | 1 digit (air,  sea,  land,  not reported)                                             |
| state_of_arrival       | varchar(256) | state code                                                                            |
| departure_date         | DATE         | date of departure                                                                     |
| age                    | SMALLINT     | age of the visitor                                                                    |
| visa                   | SMALLINT     | visa codes collapsed into three categories: (1 = Business; 2 = Pleasure; 3 = Student) |
| birth_year             | SMALLINT     | 4 digit year of birth                                                                 |
| gender                 | varchar(256) | gender                                                                                |
| visatype               | varchar(256) | class of admission legally admitting the non-immigrant to temporarily stay in U.S.    |


# Table country_mapping

| Column      | Dtype        | Description          |
|-------------|--------------|----------------------|
| id          | INTEGER      | 3 digit country code |
| description | varchar(256) | name of the country  |


# Table port

| Column | Dtype        | Description      |
|--------|--------------|------------------|
| port   | varchar(256) | 3 chars port     |
| state  | varchar(256) | state code       |
| city   | varchar(256) | name of the city |


# Table port_city

| Column                            | Dtype         | Description                                                      |
|-----------------------------------|---------------|------------------------------------------------------------------|
| city                              | varchar(256)  | name of the city                                                 |
| state                             | varchar(256)  | name of the state                                                |
| median_age                        | numeric(18,0) | the median of the age of the population                          |
| male_population                   | INTEGER       | number of the male population                                    |
| female_population                 | INTEGER       | number of the female population                                  |
| total_population                  | INTEGER       | number of the total population                                   |
| number_of_veterans                | INTEGER       | number of veterans living in the city                            |
| foreign_born                      | INTEGER       | number of residents of the city that were not born in the city   |
| average_household_size            | numeric(18,0) | average number of people livin in one household                  |
| state_code                        | varchar(256)  | code of the state                                                |
| white                             | INTEGER       | count of White residents of the city                             |
| american_indian_and_alaska_native | INTEGER       | count of American Indian and Alaska Native residents of the city |
| hispanic_or_latino                | INTEGER       | count of Hispanic or Latino residents of the city                |
| black_or_african_american         | INTEGER       | count of Black or African-American residents of the city         |
| asian                             | INTEGER       | count of Asian residents of the city                             |


# Table mode_mapping
| Column      | Dtype        | Description                            |
|-------------|--------------|----------------------------------------|
| id          | INTEGER      | 1 digit                                |
| description | varchar(256) | one of air,  sea,  land,  not reported |

# Table state
| Column      | Dtype        | Description       |
|-------------|--------------|-------------------|
| id          | varchar(256) | code of the state |
| description | varchar(256) | name of the state |

# Table visa_mapping
| Column      | Dtype        | Description                             |
|-------------|--------------|-----------------------------------------|
| id          | INTEGER      | visa code                               |
| description | varchar(256) | visa type (Business, Pleasure, Student) |


# Table date

| Column  | Dtype    | Description     |
|---------|----------|-----------------|
| date    | date     | date            |
| day     | smallint | day             |
| week    | smallint | week            |
| month   | smallint | month           |
| year    | smallint | year            |
| weekday | smallint | day of the week |
