#! /bin/bash

set -e

echo "PostgreSQL starting..!"
until pg_isready -h postgres_db -p 5432 -U "$POSTGRES_USER"; do
    sleep 2
done

echo "PostgreSQL started"

echo "Checking if the Table exists: "
Table=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT to_regclass('public.news_articles');")

if [ "$Table" != "news_articles" ];then
    echo "Table does not exist. Creating table..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
    CREATE TABLE news_articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        pub_timestamp TIMESTAMP NOT NULL,
        weblink TEXT NOT NULL,
        image BYTEA,
        tags TEXT[],
        summary TEXT
    );
EOF
    echo "Table created successfully."
else
    echo "Table already exists. Skipping creation."
fi

echo "Database and tables are set up!"