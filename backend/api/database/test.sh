echo "WARNING: Continuing will ERASE the database. Type 'y' to continue:"
read -r confirm
if [[ "$confirm" != "y" ]]; then
  echo "Aborting..."
  exit 1
fi

../env/bin/python3 -m coverage run -m pytest ./tests/*
../env/bin/python3 -m coverage html
