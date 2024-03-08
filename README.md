"Restaurant-Kitchen-Service" 
Management system for improving communication 
& rules between cooks on the kitchen.

The site is available only for authenticated users.
To login you can use following superuser:
    Login: Bob
    Password: Qwerty@123
The is one application in the project structure - catalog.
Three models are defined in models.py: dishtype, cook and dish.
All models are registered in admin.
Inside catalog.urls there is a path for the home page.
Path to the catalog.urls can be found in restaurant_kitchen_service.urls.
On the home page of the site there are link to three list: cooks, dishes and dish types.
Each element of the list can be opened when clicking the link to the detailed page.
On each detailed page elements can be created, updated or deleted.
Functionality is defined in views.py.
A custom forms to search content on the site and to create delete content on the site can be found in forms.py. 
Templates for pages are stored in the directory "templates".
Inside the directory catalog/static there are css, fonts, images, js and scss files.
Inside catalog/templatetags we have query_transform.py file.
