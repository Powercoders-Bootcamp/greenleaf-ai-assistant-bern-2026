-- ============================================
-- GreenLeaf Beat-Bot Logging Database Schema
-- ============================================

-- 1. Conversations Table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Messages Table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
);

-- 3. Tool Calls Table
CREATE TABLE tool_calls (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    message_id INTEGER,

    tool_name VARCHAR(100) NOT NULL,
    tool_arguments JSONB,
    tool_response JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (message_id)
        REFERENCES messages(id)
        ON DELETE SET NULL
);

-- 4. Interaction Logs Table
CREATE TABLE interaction_logs (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,

    user_question TEXT NOT NULL,
    final_answer TEXT NOT NULL,

    used_tools TEXT[],
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,

    response_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
);

-- 5. Indexes
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_tool_calls_conversation ON tool_calls(conversation_id);
CREATE INDEX idx_interaction_logs_conversation ON interaction_logs(conversation_id);
