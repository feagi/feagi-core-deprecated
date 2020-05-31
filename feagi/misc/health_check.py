# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
from misc import db_handler
from configuration import settings

print(settings.Bcolors.YELLOW + "Module loaded: health_check" + settings.Bcolors.ENDC)

def mongo_healthcheck():
    mongo = db_handler.MongoManagement()

    try:
        mongo.client.server_info()
        print(settings.Bcolors.OKGREEN + "Success: Connection to << MongoDb >> has been established." + settings.Bcolors.ENDC)
    except:
        print(settings.Bcolors.RED + "ERROR: Cannot connect to << MongoDb >> Database" + settings.Bcolors.ENDC)


def influx_healthcheck():
    influx = db_handler.InfluxManagement()

    try:
        influx.client.ping()
        print(settings.Bcolors.OKGREEN + "Success: Connection to << InfluxDb >> has been established." + settings.Bcolors.ENDC)
    except:
        print(settings.Bcolors.RED + "ERROR: Cannot connect to << InfluxDb >> Database" + settings.Bcolors.ENDC)


if __name__ == '__main__':
    mongo_healthcheck()
    # influx_healthcheck()
