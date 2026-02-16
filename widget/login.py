class LoginPage:

    widget = None
    controller = None
    pageIndex = 0

    def onLogin(self):
        username = self.widget.UsernameEntry.text()
        password = self.widget.PasswordEntry.text()

        success = self.controller.client.log_in(username,password)

        if (not success):
            self.widget.LoginStatusLabel.setText(f"Login failed, check username & password.")
        else:
            self.widget.LoginStatusLabel.setText(f"Login success!")
            self.controller.qgis.save_credentials(username,password)
            self.controller.switch_to_page(self.controller.home)


    def open(self,**kwargs):
        self.widget.LoginStatusLabel.setText("")

        user,password = self.controller.qgis.load_credentials()
        self.widget.PasswordEntry.setText(password)
        self.widget.UsernameEntry.setText(user)

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.widget.LoginButton.clicked.connect(self.onLogin)