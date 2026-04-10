#!/bin/bash
# Example: Run PIPA pipeline on the included Bacillus anthracis test data
#
# This example skips trimming and assembly (we already have an assembled genome)
# and runs the prediction stage directly.
#
# Usage:
#   With Docker:  docker-compose up -d && bash examples/run_example.sh
#   Without Docker: bash examples/run_example.sh

set -euo pipefail

API_URL="${PIPA_API_URL:-http://localhost:5000/api}"
TEST_FILE="back-end/test_data/Bacillus_anthracis_str_ames.fna"

echo "=== PIPA Example Pipeline Run ==="
echo "API: $API_URL"
echo "Test file: $TEST_FILE"
echo ""

# Step 1: Upload the test file as a nanopore read (it's actually assembled, but
# this demonstrates the upload flow)
echo ">> Uploading test file..."
UPLOAD_RESPONSE=$(curl -s -X POST "$API_URL/upload" \
  -F "illumina=@$TEST_FILE")

JOB_ID=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "   Job ID: $JOB_ID"

# Step 2: Start the pipeline
echo ">> Starting pipeline..."
curl -s -X POST "$API_URL/run" \
  -H "Content-Type: application/json" \
  -d "{
    \"job_id\": \"$JOB_ID\",
    \"genus\": \"Bacillus\",
    \"species\": \"anthracis\",
    \"sample_name\": \"test_bacillus\",
    \"genome_size\": \"5.2m\"
  }" | python3 -m json.tool

# Step 3: Poll for status
echo ""
echo ">> Polling pipeline status..."
while true; do
  STATUS_RESPONSE=$(curl -s "$API_URL/status/$JOB_ID")
  STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  PROGRESS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['progress'])")
  MESSAGE=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['message'])")

  echo "   [$PROGRESS%] $STATUS - $MESSAGE"

  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "completed_with_errors" ] || [ "$STATUS" = "failed" ]; then
    break
  fi
  sleep 5
done

# Step 4: Fetch results
echo ""
echo ">> Fetching results..."
curl -s "$API_URL/results/$JOB_ID" | python3 -m json.tool

echo ""
echo "=== Done ==="
