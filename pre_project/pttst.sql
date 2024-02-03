-- Create a new database
CREATE DATABASE IF NOT EXISTS test_flaskr;

-- Use the newly created database
USE test_flaskr;

-- Create a table for entries
CREATE TABLE IF NOT EXISTS entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    text TEXT
);

-- Insert some sample data
INSERT INTO entries (title, text) VALUES
    ('First Entry', 'This is the text for the first entry.'),
    ('Second Entry', 'This is the text for the second entry.'),
    ('Third Entry', 'This is the text for the third entry.');
