#!/bin/bash
clear
SERVER="http://localhost:5000"
TEST_USER="testuser_$RANDOM"
TEST_PASS="testpass_$RANDOM"
TEST_EMAIL="test_$RANDOM@example.com"

# Helper function to encrypt like versleutel_tekst
versleutel_tekst() {
    local tekst="$1"
    # Base64 encode
    local base64_str=$(echo -n "$tekst" | base64)
    # Shift each character by 3 ASCII values
    local verschoven=""
    for ((i=0; i<${#base64_str}; i++)); do
        char="${base64_str:$i:1}"
        ascii_val=$(printf "%d" "'$char")
        new_ascii=$((ascii_val + 3))
        verschoven+=$(printf "\\$(printf '%03o' "$new_ascii")")
    done
    echo -n "$verschoven"
}

echo "Starting API tests..."
echo "Using test user: $TEST_USER"
echo "Server: $SERVER"

# Test account creation
echo -e "\n=== Testing account creation ==="
create_response=$(curl -s "${SERVER}/maak_acount_V2/${TEST_USER}/${TEST_PASS}/${TEST_EMAIL}")
if [ "$create_response" == "account aangemaakt" ]; then
    echo "Account creation successful"
else
    echo "Account creation failed: $create_response"
    exit 1
fi

# Test duplicate account creation
echo -e "\n=== Testing duplicate account ==="
duplicate_response=$(curl -s "${SERVER}/maak_acount_V2/${TEST_USER}/${TEST_PASS}/${TEST_EMAIL}")
if [ "$duplicate_response" == "gebruiker bestaat al" ]; then
    echo "Duplicate account prevention working"
else
    echo "Duplicate account check failed: $duplicate_response"
    exit 1
fi



# Test successful login
echo -e "\n=== Testing login ==="
login_response=$(curl -s "${SERVER}/login/${TEST_USER}/${TEST_PASS}")
if [[ "$login_response" == * ]]; then
    USER_KEY="$login_response"
    echo "Login successful. User key: $USER_KEY"
else
    echo "Login failed: $login_response"
    exit 1
fi


# Test score update
echo -e "\n=== Testing score update ==="
SCORE_TO_SET=150
PASTA=$(versleutel_tekst "$SCORE_TO_SET")
update_response=$(curl -s "${SERVER}/set_score/${USER_KEY}/${SCORE_TO_SET}/${PASTA}")
if [ "$update_response" == 0 ]; then
    echo "Score update successful (0 -> 150)"
else
    echo "Score update failed: $update_response"
    exit 1
fi

# Verify updated score
echo -e "\n=== Verifying updated score ==="
updated_score=$(curl -s "${SERVER}/get_score/${TEST_USER}")
if [ "$updated_score" == "150" ]; then
    echo "Score verification successful (150)"
else
    echo "Score verification failed: $updated_score"
    exit 1
fi

# Test leaderboard
echo -e "\n=== Testing leaderboard ==="
leaderboard=$(curl -s "${SERVER}/leaderboard")
if echo "$leaderboard" | grep -q "$TEST_USER"; then
    echo "User found in leaderboard"
else
    echo "User not found in leaderboard"
    exit 1
fi

# Test invalid score format
echo -e "\n=== Testing invalid score ==="
invalid_response=$(curl -s "${SERVER}/set_score/${USER_KEY}/invalid/${PASTA}")
if [[ "$invalid_response" == *"Ongeldige score"* ]]; then
    echo "Invalid score handling working"
else
    echo "Invalid score handling failed: $invalid_response"
    exit 1
fi

# Test score too high
echo -e "\n=== Testing score limit ==="
high_score_response=$(curl -s "${SERVER}/set_score/${USER_KEY}/10001/${PASTA}")
if [[ "$high_score_response" == *"boos"* ]]; then
    echo "High score prevention working"
else
    echo "High score check failed: $high_score_response"
    exit 1
fi

echo -e "\n=== All tests passed successfully ==="
exit 0
