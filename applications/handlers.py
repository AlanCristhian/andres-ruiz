default = {
    #'\/$': 'articles.controllers.list_of_articles'
    '\/$': 'home.controllers.home'
    ,'/error404': 'error.error404'
    ,'/test': 'performance.controllers.controller'
}

login = {
    '/admin/login': 'login.controllers.login',
    '/admin/login/user.*': 'admin.login.model.user'
}

admin = {
    '/admin/home': 'admin.controllers.home'
    ,'/admin/logout': 'logout.controllers.logout'
    # ,'/admin/borrar': 'admin.borrar'
    # ,'/admin/contact': 'editContact.controllers.edit_contact_info'
}

new_articles = {
    '/admin/nuevo': 'newarticle.controllers.show_new_article_form'
    ,'/admin/nuevo/validate_field': 'newarticle.controllers.validate_field'
    ,'/admin/nuevo/create': 'newarticle.controllers.create_new_article'
}

editContact = {
    '/admin/editar-contacto': 'editContact.controllers.contact'
    ,'\/admin\/get\-contact\-info.*': 'editContact.controllers.get_contact_info'
    ,'\/admin\/update\-contact\-info.*': 'editContact.controllers.update_contact_info'
}

editArticles = {
    '\/admin\/editar$': 'editArticle.controllers.show_edit_list_of_articles'
    ,'\/admin\/editar\/.+': 'editArticle.controllers.edit_article'
    ,'\/admin\/get\-article\-data.+': 'editArticle.controllers.get_article_data'
    ,'/admin/save-article-data': 'editArticle.controllers.save_article_data'
    ,'/admin/save-image-data': 'editArticle.controllers.save_image_data'
    ,'/admin/save-image': 'editArticle.controllers.save_image'
    ,'/admin/update-article-field': 'editArticle.controllers.update_article_field'
    ,'/admin/get-list-of-articles': 'editArticle.controllers.get_list_of_articles'
    ,'/admin/remove-article': 'editArticle.controllers.remove_article'
    ,'/admin/remove-image': 'editArticle.controllers.remove_image'
}

form = {
    '/send-form': 'form.send'
    ,'/get-form': 'form.get'
    ,'/form': 'form.page'
}

shared_libraries = {
    '/check-ssl-environ': 'shared.controllers.check_ssl_environ',
    '/unittest': 'specs.controllers.frontend_unittest'
}

experiments = {
    '/exp/vertical-flux': 'experiments.controllers.vertical_flux',
}

home = {
    '\/proyectos\/.+': 'home.controllers.article',
    '\/images\/.+': 'home.controllers.get_article_images',
    '/home/get_collection': 'home.controllers.get_article_collection',
}

articles = {
    #'\/proyectos\/.+': 'articles.controllers.send_article'
    '/contacto': 'contact.controllers.show_contact_page',
    '\/mas-info$': 'aboutme.controllers.aboutme',
}