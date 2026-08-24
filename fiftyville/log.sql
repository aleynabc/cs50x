-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Finding the thief
SELECT name FROM people JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute <= 25 INTERSECT SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Finding the city
SELECT city FROM airports JOIN flights ON airports.id = flights.destination_airport_id WHERE day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute LIMIT 1;

-- Finding the accomplice
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE name = 'Bruce'));
