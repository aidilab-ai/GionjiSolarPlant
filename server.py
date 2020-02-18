import tornado.ioloop
import tornado.web

import relayBox as rb
import database


class LastData(tornado.web.RequestHandler):
    
    def get(self):

        self.write(database.getLastData())


class Plugs(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):

        super(Plugs, self).__init__(application, request, **kwargs)
        
        self.handlers = {
            rb.PLUG_A_ID: {
                rb.STATE_ON: (rb.enablePlugA, 'Turn on plug A'),
                rb.STATE_OFF: (rb.disablePlugA, 'Turn off plug A')
            },
            rb.PLUG_B_ID: {
                rb.STATE_ON: (rb.enablePlugB, 'Turn on plug B'),
                rb.STATE_OFF: (rb.disablePlugB, 'Turn off plug B')
            },
            rb.INVERTER_ID: {
                rb.STATE_ON: (rb.enableInverter, 'Turn on inverter'),
                rb.STATE_OFF: (rb.disableInverter, 'Turn off inverter')
            },
            rb.EXTERNAL_SOURCE_ID: {
                rb.STATE_ON: (rb.enableExternalPower, 'Turn on external power'),
                rb.STATE_OFF: (rb.disableExternalPower, 'Turn on solar panel')
            }                                    
        }


    def get(self):

        self.write("plug_id: a b i e --- state: 0 1")
    
    
    def post(self):

        plug_id = self.get_argument('plug_id')
        state = self.get_argument('state')

        self.write( "plug_id: " + str(plug_id) + "/nstate: " + str(state) )
        (handler_function, message) = self.handlers[plug_id][state]
        
        handler_function()
        print(message)


class User(tornado.web.RequestHandler):

    def get(self):

        # form = """
        # <form method="post">
        #     <input type="text" name="username"/>
        #     <input type="text" name="designation"/>
        #     <input type="submit"/>
        # </form>
        # """

        form = """
        <form method="post">
            <input type="text" name="start"/>
            <input type="text" name="end"/>
            <input type="submit"/>
        </form>
        """

        self.write(form)


    def post(self):

        start = self.get_argument('start')
        end = self.get_argument('end')

        conn = database.create_connection(database.DATABASE_PATH)
        data = database.select_data(conn, start, end)        

        self.write(data)

        # self.write("Wow {username}, you're a {designation}".format(
        #     username=self.get_argument("username"), 
        #     designation=self.get_argument("designation")
        # ))


application = tornado.web.Application([
    (r"/last/", LastData),
    (r"/user/", User),
    (r"/relaybox/", Plugs),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()