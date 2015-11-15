# -*- coding: utf-8 -*-
#coding: UTF-8
import sae
import app
application = sae.create_wsgi_app(app.application)