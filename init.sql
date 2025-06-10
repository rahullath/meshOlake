-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Habits definition table
CREATE TABLE habits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    question TEXT,
    description TEXT,
    position INTEGER,
    num_repetitions INTEGER DEFAULT 1,
    interval_days INTEGER DEFAULT 1,
    color VARCHAR(7) DEFAULT '#3b82f6',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily habit checkmarks (0-3 scale from Loop Habits)
CREATE TABLE habit_checkmarks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    habit_id INTEGER REFERENCES habits(id),
    date DATE NOT NULL,
    value INTEGER CHECK (value IN (0, 1, 2, 3)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(habit_id, date)
);

-- Calculated habit scores (Loop Habits algorithm)
CREATE TABLE habit_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    habit_id INTEGER REFERENCES habits(id),
    date DATE NOT NULL,
    score DECIMAL(6,4) CHECK (score >= 0 AND score <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(habit_id, date)
);

-- Financial transactions
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    value_date DATE,
    particulars TEXT NOT NULL,
    transaction_type VARCHAR(50),
    cheque_details VARCHAR(255),
    withdrawals DECIMAL(10,2),
    deposits DECIMAL(10,2),
    balance DECIMAL(10,2),
    dr_cr VARCHAR(2) CHECK (dr_cr IN ('Dr', 'Cr')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_habit_checkmarks_date ON habit_checkmarks(date DESC);
CREATE INDEX idx_habit_scores_date ON habit_scores(date DESC);
CREATE INDEX idx_transactions_date ON transactions(date DESC);
CREATE INDEX idx_habits_user ON habits(user_id);

-- Insert sample user
INSERT INTO users (username, email) VALUES ('meshuser', 'user@meshos.dev');

-- Insert habits from Habits.csv structure
INSERT INTO habits (user_id, name, question, description, position, num_repetitions, interval_days, color) VALUES
(1, 'Vaping', 'How many puffs today', '', 1, 1, 1, '#5D4037'),
(1, 'Quit Valorant', 'Did you game', '', 2, 1, 1, '#F9A825'),
(1, 'Walk', 'Go for a walk', '', 3, 1, 1, '#00897B'),
(1, 'Wake Up Early', 'Did you wake up early', '', 4, 1, 1, '#7CB342'),
(1, 'No Pot', 'Avoided smoking pot', '', 5, 1, 1, '#8BC34A'),
(1, 'No Energy Drink', 'Avoided energy drinks', '', 6, 1, 1, '#FF9800'),
(1, 'Coding', 'Did programming work', '', 7, 1, 1, '#2196F3'),
(1, 'Shower', 'Took a shower', '', 8, 1, 1, '#03DAC6'),
(1, 'University', 'Attended university', '', 9, 1, 1, '#9C27B0'),
(1, 'Gym', 'Went to gym', '', 10, 1, 1, '#FF5722');

-- Sample checkmarks data (from actual CSV)
INSERT INTO habit_checkmarks (user_id, habit_id, date, value) VALUES
-- April 18, 2025 data
(1, 1, '2025-04-18', 0), -- Vaping
(1, 2, '2025-04-18', 2), -- Quit Valorant
(1, 3, '2025-04-18', 2), -- Walk
(1, 4, '2025-04-18', 3), -- Wake Up Early
(1, 5, '2025-04-18', 2), -- No Pot
(1, 6, '2025-04-18', 2), -- No Energy Drink
(1, 7, '2025-04-18', 2), -- Coding
(1, 8, '2025-04-18', 2), -- Shower
(1, 9, '2025-04-18', 2), -- University
(1, 10, '2025-04-18', 2), -- Gym
-- Continue with more dates...
;

-- Sample scores data (from actual CSV)
INSERT INTO habit_scores (user_id, habit_id, date, score) VALUES
-- April 18, 2025 scores
(1, 1, '2025-04-18', 0.9876), -- Vaping
(1, 2, '2025-04-18', 0.9704), -- Quit Valorant
(1, 3, '2025-04-18', 0.9270), -- Walk
(1, 4, '2025-04-18', 0.9174), -- Wake Up Early
(1, 5, '2025-04-18', 0.9043), -- No Pot
(1, 6, '2025-04-18', 0.8750), -- No Energy Drink
(1, 7, '2025-04-18', 0.8682), -- Coding
(1, 8, '2025-04-18', 0.8682), -- Shower
(1, 9, '2025-04-18', 0.7979), -- University
(1, 10, '2025-04-18', 0.5960), -- Gym
-- Continue with more dates...
;
