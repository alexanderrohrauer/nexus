mongoexport --uri="mongodb://localhost:27017" --db=nexus_dev --collection=Institution --out=mongo_dumps/Institution.json ;
mongoexport --uri="mongodb://localhost:27017" --db=nexus_dev --collection=Researcher --out=mongo_dumps/Researcher.json ;
mongoexport --uri="mongodb://localhost:27017" --db=nexus_dev --collection=Work --out=mongo_dumps/Work.json ;
