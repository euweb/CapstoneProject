class SqlQueries:

    i94imm_table_insert = ("""
        SELECT 
            CAST(i94yr as INTEGER) as year_of_arrival,
            CAST(i94mon as INTEGER) as month_of_arrival,
            CAST(i94cit as INTEGER) as country_of_citizenship,
            CAST(i94res as INTEGER) as country_of_residence,
            i94port as port_of_entry,
            '1960-1-1'::date + (arrdate * interval '1 day') as arrival_date,
            CAST(i94mode as INTEGER) as arrivid_by,
            i94addr as state_of_arrival, 
            '1960-1-1'::date + (arrdate * interval '1 day') as departure_date,
            CAST(i94bir as INTEGER) as age,
            CAST(i94visa as INTEGER) as visa,
            CAST(biryear as INTEGER) as birth_year,
            gender as gender,
            visatype as visatype
        FROM
            i94imm_staging
    """)
    
    date_table_insert = ("""
        SELECT DISTINCT arrival_date,
            extract(day from arrival_date) AS day,
            extract(week from arrival_date) AS week,
            extract(month from arrival_date) AS month,
            extract(year from arrival_date) AS year,
            extract(dow from arrival_date) AS weekday
        FROM
            visit

        UNION

        SELECT DISTINCT departure_date,
            extract(day from departure_date) AS day,
            extract(week from departure_date) AS week,
            extract(month from departure_date) AS month,
            extract(year from departure_date) AS year,
            extract(dow from departure_date) AS weekday
        FROM
            visit
    """)

    airport_table_insert = ("""
        WITH ports AS (		
            SELECT
                ident AS port,
                SPLIT_PART(iso_region, '-', 2) AS state,
                municipality AS city
            FROM airport_codes_staging
            WHERE iso_country = 'US' AND ident IS NOT NULL
            
            UNION
            
            SELECT
                iata_code AS port,
                SPLIT_PART(iso_region, '-', 2) AS state,
                municipality AS city
            FROM airport_codes_staging
            WHERE iso_country = 'US' AND iata_code IS NOT NULL
            
            UNION
            
            SELECT
                local_code AS port,
                SPLIT_PART(iso_region, '-', 2) AS state,
                municipality AS city
            FROM airport_codes_staging
            WHERE iso_country = 'US' AND local_code IS NOT NULL
        )

        SELECT
			id AS port,
			CASE
				WHEN b.city='' THEN
					trim(SPLIT_PART(description, ',', 2))
		    	ELSE
		    		b.state
		    END AS state,
		    CASE
				WHEN b.city='' THEN
		    		SPLIT_PART(description, ',', 1)
		    	ELSE
		    		b.city
		    END AS city
		FROM i94port_mapping a
		JOIN
		    ports b on a.id=b.port
    """)


    port_city_table_insert = ("""
        SELECT DISTINCT a.city,
            a.state, 
            a.median_age, 
            a.male_population, 
            a.female_population, 
            a.total_population, 
            a.number_of_veterans, 
            a.foreign_born, 
            a.average_household_size, 
            a.state_code,
            f.race_count AS white,
            b.race_count AS american_indian_and_alaska_native,
            c.race_count AS hispanic_or_latino,
            d.race_count AS black_or_african_american,
            e.race_count AS asian
        FROM us_cities_demographics_staging a
        JOIN us_cities_demographics_staging b ON a.city = b.city AND a.state = b.state AND
            b.race = 'American Indian and Alaska Native'
        JOIN us_cities_demographics_staging c ON a.city = c.city AND a.state = c.state 
            AND c.race = 'Hispanic or Latino'
        JOIN us_cities_demographics_staging d ON a.city = d.city AND a.state = d.state 
            AND d.race = 'Black or African-American'
        JOIN us_cities_demographics_staging e ON a.city = e.city AND a.state = e.state 
            AND e.race = 'Asian'
        JOIN us_cities_demographics_staging f ON a.city = f.city AND a.state = f.state 
            AND f.race = 'White'
        GROUP BY a.city, a.state, a.median_age, a.male_population, a.female_population, 
        	a.total_population, a.number_of_veterans, a.foreign_born, a.average_household_size, a.state_code, 
         	white, american_indian_and_alaska_native, hispanic_or_latino, black_or_african_american, asian
    """)