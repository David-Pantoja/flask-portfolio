#!/bin/sh
curl -X POST http://localhost:5000/api/timeline_post -d "name=TEST_NAME&email=TEST_EMAIL&content=TEST_CONTENT" | jq '{id}' > post_result.json
curl http://localhost:5000/api/timeline_post | jq '.timeline_posts | .[0] | {id}' > get_result.json
IDP=$(jq '.id' post_result.json)
IDG=$(jq '.id' get_result.json)
echo "TEST Get ID: $IDG TEST POST ID: $IDP "
rm post_result.json
rm get_result.json
