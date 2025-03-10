# MDE YellowPages

This repository includes the source code for the prototype _Nexus_ of my Bachelor's thesis "MDE YellowPages" at the Institut für Wirtschaftsinformatik - Software Engineering at the University of Linz.

## Installation
1. Install Docker
2. If cached example-data is needed you can copy the *.sqlite cache files from `caches` folder into the `app` folder of this repository
3. Make sure, nothing runs on ports 3000, 8000 and 27017 on your machine
4. Run `docker compose up -d`
5. After the startup was complete (~10sec), you can access the UI at `http://localhost:3000` and the REST-API at `http://localhost:8000`

The OpenAPI REST-API documentation is available at `http://localhost:8000/docs`

## Load example-data
1. Run `./import-example-data.sh` (after marking the file as executable)
2. After the process has finished (you can see this information in the container logs of the backend), you can do the next step
3. Run `curl -X POST "http://127.0.0.1:8000/import-task/run-duplicate-detection"` for duplication-detection. This may take a while depending on the amount of data imported in the first step.
4. After the process has finished (you can see this information in the container logs of the backend), you can do the next step
5. Run `curl -X POST "http://127.0.0.1:8000/import-task/run-duplicate-elimination"`. This may take a while depending on the amount of data imported in the first step.
6. Any duplicates which require manual duplicate elimination can be filtered in the Overview visualization with the filter set to `duplication_key not equals null`

You can reset the cursor for the import-process with:
```
curl -X PUT "http://127.0.0.1:8000/import-task/reset-cursors" \
     -H "Content-Type: application/json" \
     -d '{
        "jobs": ["openalex_import_job", "dblp_import_job"]
     }';
```
Alternatively, you can insert example-data directly into your mongo database with the dumps at https://jkulinz-my.sharepoint.com/:f:/g/personal/k12105578_students_jku_at/Eo__4iwSOtpJrOX4FQy8ANEBVuVVOYmvlhB0KZM4oy7wGA?e=SWnF6f. Use the script `mongo_import.sh` and adapt it to the name of your used database schema (modify `--db` argument).
## Citation
```
@mastersthesis{Rohrauer_2025a,
	title        = {MDE YellowPages},
	author       = {Rohrauer, Alexander},
	year         = 2025,
	type         = {Bachelor's Thesis}
}
```
