# coding=utf-8

import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.web
import os.path

from orm import UserManagerORM
from tornado.options import options, define

define("port", default=8000, help="run in the given port", type=int)
user_orm = UserManagerORM()

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        title = "用户管理"
        users = user_orm.GetAllUser()
        self.render('templates/UserManager.html', title=title, users=users)

class AddUserHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        user_info = {
            'user_name': self.get_argument('user_name'),
            'user_age': self.get_argument('user_age'),
            'user_sex': self.get_argument('user_sex'),
            'user_score': self.get_argument('user_score'),
            'user_subject': self.get_argument('user_subject')
        }
        user_orm.CreateNewUser(user_info)
        self.redirect('http://localhost:%d'% options.port)

class EditUserHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        user_info = user_orm.GetUserByName(self.get_argument("user_name"))
        self.render("templates/EditUserInfo.html", user_info=user_info)

class UpdateUserInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        user_orm.UpdateUserInfoByName({
                        'user_name':self.get_argument( 'user_name' ),
                        'user_age':self.get_argument( 'user_age' ),
                        'user_sex':self.get_argument( 'user_sex' ),
                        'user_score':self.get_argument( 'user_score' ),
                        'user_subject':self.get_argument( 'user_subject' ),
                        })
        self.redirect("http://localhost:%d" %options.port)

class DeleteUserHandler(tornado.web.RequestHandler):
    def get(self):
        user_orm.DeleteUserByName(self.get_argument("user_name"))
        self.render("http://localhost:%d" % options.port)


class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/', MainHandler),
            (r'/add_user', AddUserHandler),
            (r'/edit_user', EditUserHandler),
            (r'/delete_user', DeleteUserHandler),
            (r'/update_user',UpdateUserInfoHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers,**settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()












