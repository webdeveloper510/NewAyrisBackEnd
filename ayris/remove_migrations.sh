#!/bin/sh


function del_migrations_folder() {
  find $app_name -path "*/migrations/*.pyc"
  find $1 -path "*/migrations/*.py" -not -name "__init__.py"
  echo "Delete $1 ?"
  read -p "To confirm? (y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
  find $1 -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find $1 -path "*/migrations/*.pyc" -delete
  echo "$1/migrations/ was delete"
}

if [[ ! -z "$1" ]]; then
  app_name="$1"
  if [[ -d $app_name ]]; then
    echo "file exist"
#    ls $1/migrations/
    del_migrations_folder $app_name

  else
    echo "folder not exist"

  fi
else 
  echo "Enter a app file"
fi


#  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
#  find . -path "*/migrations/*.pyc" -delete
