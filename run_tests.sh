export ENV=test
export PYTHONDONTWRITEBYTECODE=1

# Create and re-create the test database
sh ./db/create_db.sh
cd db               
npm i
NODE_ENV=$ENV npm run refresh     # hotels_test this will drop tables, re-create them
NODE_ENV=$ENV npm run seed  

cd ..
find . -name "__pycache__" -exec rm -r {} +
python -m pytest
