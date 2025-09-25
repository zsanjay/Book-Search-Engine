# Book Search API

This is a *Book Search API Project* implemented using *Java, Maven, and Spring Boot with PostgreSQL and Docker*.

---
## Module 1: Setting Up Java, Maven, and Spring Boot

### Install Java Development Kit (JDK)

#### Install SDKMAN

```bash
curl -s "https://get.sdkman.io" | bash
```

Open a new terminal tab and run:

```bash
sdk version
```

#### List available Java versions

```bash
sdk list java | grep -i open
```

Example output:

```
Java.net      |     | 24.ea.16     | open    |            | 24.ea.16-open
              |     | 21.0.2       | open    |            | 21.0.2-open
```

#### Install specific Java version

```bash
sdk install java 24.ea.16-open
sdk install java 21.0.2-open
```

#### Use a specific version

```bash
sdk use java 24.ea.16-open
```

Verify installation:

```bash
java -version
```

---

### Install Maven

```bash
brew install maven
```

Verify:

```bash
mvn -version
```

---

### Create a New Maven Project

```bash
mvn archetype:generate \
  -DgroupId=com.h2 \
  -DartifactId=book-search \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

Build & test:

```bash
cd book-search && mvn clean install
```

---

## Module 2: Dockerizing the Project with PostgreSQL

### Start container

```bash
docker-compose up -d
```

### Connect to database

```bash
docker exec -it library-db psql -U admin -d library
```

### Verify version

```sql
SELECT version();
```

### List databases

```sql
\l
```

### Stop container

```bash
docker-compose down
```

### Run application

```bash
mvn spring-boot:run
```

---

## Module 3: Designing the Database Schema & Full-Text Search

### Create network

```bash
docker network create db-network
docker network connect db-network library-db
```

### Setup PGAdmin

```bash
docker run -p 80:80 \
  -e PGADMIN_DEFAULT_EMAIL=user@domain.com \
  -e PGADMIN_DEFAULT_PASSWORD=SuperSecret \
  --name pgadmin \
  --network db-network \
  -d dpage/pgadmin4
```

Visit: [http://localhost:80](http://localhost:80)

---

### Create tables & relationships

```bash
docker cp db/create_schema.sql library-db:/create_schema.sql
docker exec -it library-db psql -U admin -d library -f /create_schema.sql
```

---

### Example queries

#### Case-insensitive search

```sql
SELECT * FROM books WHERE title ILIKE '%algorithms%' OR description ILIKE '%algorithms%';
```

#### Full-text search

```sql
SELECT title, ts_rank(search_vector, to_tsquery('english', 'algorithms')) AS rank
FROM books
WHERE search_vector @@ to_tsquery('english', 'algorithms')
ORDER BY rank DESC;
```

---

## Module 4: Ingesting & Validating Data

Check row counts:

```sql
SELECT count(*) FROM authors;
SELECT count(*) FROM books;
SELECT count(*) FROM book_authors;
```

Join query:

```sql
SELECT b.*, a.name AS author_name
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
WHERE a.name = 'Steve Wozniak';
```

---

## Module 5: Designing & Creating APIs

### Search books (test with curl)

```bash
curl -X GET "http://localhost:8080/books/search?searchTerm=algorithms" -H "accept: application/json"
```
