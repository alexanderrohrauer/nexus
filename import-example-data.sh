curl -X POST "http://127.0.0.1:8000/import-task" \
     -H "Content-Type: application/json" \
     -d '{
       "cron_expr": "0 0 1 1 *",
       "n_batches": 5,
       "keywords": [
         "Model-driven engineering"
       ]
     }';
# Enter the keywords and count of batches for indexation below
curl -X PUT "http://127.0.0.1:8000/import-task" \
     -H "Content-Type: application/json" \
     -d '{
       "cron_expr": "0 0 1 1 *",
       "n_batches": 5,
       "keywords": [
         "Model-driven engineering"
       ]
     }';

curl -X POST "http://127.0.0.1:8000/import-task/run";
