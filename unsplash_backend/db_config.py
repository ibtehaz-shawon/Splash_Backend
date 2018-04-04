databaseUrl = ''


def db_url_parsing(url):
    global databaseUrl
    databaseUrl = url
    databaseUrl = databaseUrl[11:]  # getting rid of the postgres part

    engine = 'django.db.backends.postgresql'
    user = assist_function(databaseUrl, ':')
    password = assist_function(databaseUrl, '@')
    hostname = assist_function(databaseUrl, ":")
    port = assist_function(databaseUrl, "/")
    database_name = databaseUrl
    database = {
        'ENGINE': engine,
        'HOST': hostname,
        'USER': user,
        'NAME': database_name,
        'PASSWORD': password,
        'PORT': port
    }
    return database


#  assist function to take care of the part


def assist_function(url, checker):
    counter = 0
    variable = ''
    for eachChar in url:
        counter += 1
        if eachChar != checker:
            variable += eachChar
        else:
            break
    global databaseUrl
    databaseUrl = url[counter:]
    return variable
