SHELL := /bin/bash
# Asume que el env está en el directorio padre
VENV := ../env
# Comando para activar el entorno virtual
ACTIVATE_VENV := call $(VENV)/scripts/activate

run:
	$(ACTIVATE_VENV) && python manage.py runserver 8000

migration:
	$(ACTIVATE_VENV) && python manage.py makemigrations
	$(ACTIVATE_VENV) && python manage.py migrate

newapp:
	$(ACTIVATE_VENV) && python manage.py startapp $(arg)

superuser:
	$(ACTIVATE_VENV) && python manage.py createsuperuser

test:
	$(ACTIVATE_VENV) && pytest --showlocals -p no:warnings -vv

install:
	$(ACTIVATE_VENV) && pip install -r requirements.txt

loaddata:
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/campus.json
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/group.json 
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/user.json
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/semester.json
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/event_type.json
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/event.json
	$(ACTIVATE_VENV) && python manage.py loaddata seeds/prize.json

collectstatic:
	$(ACTIVATE_VENV) &&  python manage.py collectstatic

database:
	docker run --name sumate-mysql -e MYSQL_ROOT_PASSWORD=4WgBJpxw5apq -e MYSQL_DATABASE=sumate_v2 -e MYSQL_USER=administrator -e MYSQL_PASSWORD=4WgBJpxw5apq -p 3306:3306 -d mysql:latest

restart: migration loaddata run
