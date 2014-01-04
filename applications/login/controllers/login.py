from framework import core


class Login(metaclass=core.Main):
    def setUp(self):
        self.loginTemplate = 'applications/login/views/login.html'
        self.redirectTemplate = 'applications/login/views/redirect.html'
        self.response.set_expires(0)

    def show_login_page(self):
        self.unlogged(
            context={
                'title': 'Iniciar sesión'
                ,'salir': False
                ,'userLabel': ''
                ,'passLabel': ''}
            ,templatePath=self.loginTemplate)

    def get_user_data(self, user):
        """return a list of dict with the user data into database."""
        self.users = self.serverCollection.get('users')
        return self.users.get(
            fields=('user_name', 'password')
            ,where="user_name=?"
            ,params=user
            ,format='object')

    def create_new_session(self):
        """Init a new user session into database and
        set a cookie session into user web browser."""
        # fix the path if the shared ssl protocol is enabled
        if self.clientModel.protocol == "https"\
        and self.config.enableSharedSSL:
            _secure, _httponly, _path = True, True, '/~andresru/admin/'
        else:
            _secure, _httponly, _path = False, False, '/'
        self.session.create()
        self.response.set_cookie(
                value=self.session.get_cookie_value()
                ,max_age=self.session.get_max_age()
                ,path=_path
                ,secure=_secure
                ,httponly=_httponly)
        self.unlogged(
            context={
                'title': 'Autentificación correcta'
                ,'salir': False
                ,'user': self.serverData['user_name']}
            ,templatePath=self.redirectTemplate)

    def redirect_to_admin_home(self):
        self.logged(
            content=''
            ,redirect='/admin/home')

    def show_not_valid_password(self):
        self.unlogged(
            context={
                'title': 'Iniciar sesión'
                ,'salir': False
                ,'userLabel': ''
                ,'passLabel': 'Contraseña no válida'}
            ,templatePath=self.loginTemplate)

    def show_not_valid_user(self):
        self.unlogged(
            context={
                'title': 'Iniciar sesión'
                ,'salir': False
                ,'userLabel': 'No existe ese usuario'
                ,'passLabel': ''}
            ,templatePath=self.loginTemplate)

    def handler(self):
        self.form = self.clientModel.form
        # check the user and password key because
        # the form can has arbiry datas
        if 'user' in self.form and 'password' in self.form:
            self.user = self.get_user_data(self.form.get('user'))
            if self.user:
                self.serverData = self.user[0]
                if self.serverData['password'] == self.form.get('password'):
                    self.create_new_session()
                else:
                    self.show_not_valid_password()
            else:
                self.show_not_valid_user()
        else:
            if self.session.validate():
                self.redirect_to_admin_home()
            else:
                self.show_login_page()