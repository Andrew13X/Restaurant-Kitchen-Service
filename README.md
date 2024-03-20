# Restaurant-Kitchen-Service

Management system for improving communication 
& rules between cooks on the kitchen.

## Check it out

[Restaurant-Kitchen-Service project is deployed to render] (https://restaurant-kitchen-service-jso7.onrender.com/)

## Installation

Python must be installed 

```
git clone https://github.com/Andrew13X/Restaurant-Kitchen-Service.git
cd restaurant-kitchen-service
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py runserver
```

## Features

1. The site is available only for authenticated users.
```
You can use following user (or create another one by yourself):
login: user
password: user12345
```

2. The is one application in the project structure - catalog.

3. Three models are defined in models.py: dishtype, cook and dish.

4. All models are registered in admin.

5. Inside catalog.urls there is a path for the home page.
Path to the catalog.urls can be found in restaurant_kitchen_service.urls.

6. On the home page of the site there are link to three list: cooks, dishes and dish types.
Each element of the list can be opened when clicking the link to the detailed page.
On each detailed page elements can be created, updated or deleted.

7. Functionality is defined in views.py.

8. A custom forms to search content on the site and to create delete content on the site can be found in forms.py. 

9. Templates for pages are stored in the directory "templates".

10. Inside the directory catalog/static there are css, fonts, images, js and scss files.

11. Inside catalog/templatetags we have query_transform.py file.

