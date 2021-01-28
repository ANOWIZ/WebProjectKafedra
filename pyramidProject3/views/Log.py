from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import transaction

from sqlalchemy.exc import DBAPIError

from .. import models

def check_login(request) -> bool:
    try:
        if(request.session['log_in']):
            return True
        else:
            return False
    except Exception as err:
        print("Error", str(err))
        return False

@view_config(route_name='login')
def log_work(request):
    if (request.params['request'] == 'enter'):
        return login(request)
    elif (request.params['request'] == 'registrate'):
        return SignIn(request)
    else:
        return Response("Произошла ошибка")

def SignIn(request):

    try:
        query = request.dbsession.query(models.User).filter(
            models.User.name == request.params['name'], models.User.password == request.params['password']).first()

        if(query is None):
            user = models.User(
                name=request.params['name'],
                password=request.params['password']
            )
            request.dbsession.add(user)
            transaction.commit()

            return Response("Вы успешно зарегистрировались")
        else:
            transaction.commit()

            return Response("Вы уже зарегистрированы")

    except Exception as err:
        print("Error", str(err))
        return Response("Произошла ошибка")


def login(request):

    try:
        query = request.dbsession.query(models.User).filter(
            models.User.name == request.params['name'], models.User.password == request.params['password']).first()

        if(query is None):
            transaction.commit()
            return Response("Вы еще не зарегистрированы")
        else:
            transaction.commit()
            request.session['log_in'] = True
            request.session['user_id'] = query.name
            return Response("Вы успешно зашли!")

    except Exception as err:
        print("Error", str(err))
        return Response("Произошла ошибка")


@view_config(route_name='logout')
def logout(request):
    request.session['log_in'] = False
    return HTTPFound(location='/')

@view_config(route_name='commit')
def make_commit(request):
    if (request.session['log_in'] == True):
        commit = models.Comments(request.session['user_id'],request.params['commit'])
        request.dbsession.add(commit)
        transaction.commit()
        return HTTPFound('/')
    else:
        return Response("Произошла ошибка")

