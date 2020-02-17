import tornado.ioloop
import tornado.web

import relayBox as rb
import database


class LastData(tornado.web.RequestHandler):
    
    def get(self):

        self.write(database.getLastData())


class Plugs(tornado.web.RequestHandler):

    def get(self):

        self.write("plug_id: a b i e --- state: 0 1")
    
    
    def post(self):

        plug_id = self.get_argument('plug_id')
        state = self.get_argument('state')

        self.write( "plug_id: " + str(plug_id) + "/nstate: " + str(state) )


        if plug_id == rb.PLUG_A_ID:

            if state == rb.STATE_ON:

                rb.enablePlugA()
                print( "Turn on plug A" )

            elif state == rb.STATE_OFF:

                rb.disablePlugA()
                print( "Turn off plug A" )
        
        elif plug_id == rb.PLUG_B_ID:

            if state == rb.STATE_ON:

                rb.enablePlugB()
                print( "Turn on plug B" )

            elif state == rb.STATE_OFF:

                rb.disablePlugB()
                print( "Turn off plug B" )

        elif plug_id == rb.INVERTER_ID:

            if state == rb.STATE_ON:

                rb.enableInverter()
                print( "Turn on INVERTER" )

            elif state == rb.STATE_OFF:

                rb.disableInverter()
                print( "Turn off plug inverter" )


        elif plug_id == rb.EXTERNAL_SOURCE_ID:

            if state == rb.STATE_ON:

                rb.enableExternalPower()
                print( "Turn on external power supply" )

            elif state == rb.STATE_OFF:

                rb.disableExternalPower()
                print( "Turn on solar panel" )

        

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