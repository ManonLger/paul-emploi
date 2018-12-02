from django.core.management.base import BaseCommand
from requests import post
from time import sleep

from api.models.offer import Offer, Degree, Skill, Language, Contract, \
    Location, Company

# despite the API documentation saying that we are allowed 1 req / sec, it
# often fails throwing a "429 too many requests" error. So we increase the
# timeout
POLE_EMPLOI_API_TIMEOUT = 3
POLE_EMPLOI_TOKEN_URL = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire'
POLE_EMPLOI_SEARCH_URL = 'https://api.emploi-store.fr/partenaire/offresdemploi/v1/rechercheroffres'
POLE_EMPLOI_CLIENT_ID = 'PAR_paulemploiletinderdescand_564ca946d246c8de2309f7967d0fd1576d8f1fe8af69f0e82f0c45e54156e82f'
POLE_EMPLOI_CLIENT_SECRET = '7dd3b6f9d6ac3e33b331e71ae3a675189cbe8fec4d572a15cdad467a7e043f86'
POLE_EMPLOI_SCOPE = 'application_PAR_paulemploiletinderdescand_564ca946d246c8de2309f7967d0fd1576d8f1fe8af69f0e82f0c45e54156e82f api_offresdemploiv1 o2dsoffre'

POLE_EMPLOI_SEARCH_KEYWORD = 'informatique'
RESULTS_PER_PAGE = 150


class Command(BaseCommand):
    help = """Run this command to scrap the data from the Pole Emploi API and
    storing the result in the database"""

    def __init__(self):
        super().__init__()
        self.token = None
        self.tot_pages = None

    def handle(self, *kwargs, **options):
        self.token = self.get_token()
        sleep(POLE_EMPLOI_API_TIMEOUT)
        self.tot_pages = self.get_pages_count()
        sleep(POLE_EMPLOI_API_TIMEOUT)
        self.populate_db()

    def get_token(self):
        auth_url = POLE_EMPLOI_TOKEN_URL
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': POLE_EMPLOI_CLIENT_ID,
            'client_secret': POLE_EMPLOI_CLIENT_SECRET,
            'scope': POLE_EMPLOI_SCOPE
        }
        auth_header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        auth_req = post(auth_url, data=auth_data, headers=auth_header)
        return auth_req.json()['access_token']

    def get_pages_count(self):
        url = POLE_EMPLOI_SEARCH_URL
        header = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        data = {
            'technicalParameters': {
                'page': 1,
                'per_page': RESULTS_PER_PAGE,
                'sort': 1
            },
            'criterias': {
                'keywords': POLE_EMPLOI_SEARCH_KEYWORD
            }
        }
        first_offer = post(url, json=data, headers=header)
        tot_results = first_offer.json()['technicalParameters']['totalNumber']
        tot_pages = int(tot_results / RESULTS_PER_PAGE)
        print("Nombre total d'offres : ", tot_results)
        return tot_pages

    def populate_db(self):
        for page_number in range(1, self.tot_pages):

            retry = True
            # we make sure we got the page event if we had an error during the
            # request
            while retry:
                print("Requesting page", page_number, "/", self.tot_pages)

                url = POLE_EMPLOI_SEARCH_URL
                header = {
                    'Authorization': 'Bearer {}'.format(self.token),
                    'Content-Type': 'application/json'
                }
                data = {
                    'technicalParameters': {
                        'page': page_number,
                        'per_page': RESULTS_PER_PAGE,
                        'sort': 1
                    },
                    'criterias': {
                        'keywords': POLE_EMPLOI_SEARCH_KEYWORD
                    }
                }
                offers_received = post(url, json=data, headers=header)
                print("Response code", offers_received.status_code)
                retry = True if offers_received.status_code == 429 else False
                if offers_received.status_code == 400:
                    # Nothing left to add, quitting the for loop
                    print("Bad Request")
                    return

                try:
                    offers = offers_received.json().get('results')
                except(ValueError):
                    print(ValueError)
                    offers = []

                for offer in offers:
                    # create an offer object
                    sql_off = Offer(
                        title=offer.get('title'),
                        min_salary=offer.get('minSalary'),
                        max_salary=offer.get('maxSalary'),
                        description=offer.get('description'),
                        weekly_work_time=offer.get('weeklyWorkTime'),
                        experience_name=offer.get('experienceName')
                    )
                    sql_off.save()

                    for item in offer.get('skills'):
                        item_name = item.get('skillName')
                        item_obj, exists = Skill.objects.get_or_create(
                            name=item_name
                        )
                        sql_off.skills.add(item_obj)

                    for item in offer.get('degrees'):
                        item_name = item.get('degreeName')
                        item_obj, exists = Degree.objects.get_or_create(
                            name=item_name
                        )
                        sql_off.degrees.add(item_obj)

                    for item in offer.get('languages'):
                        item_name = item.get('languageName')
                        item_obj, exists = Language.objects.get_or_create(
                            name=item_name
                        )
                        sql_off.languages.add(item_obj)

                    if offer.get('contractTypeName') is not None:
                        item_name = offer.get('contractTypeName')
                        item_obj, exists = Contract.objects.get_or_create(
                            name=item_name
                        )
                        sql_off.contract_type = item_obj
                        sql_off.save()

                    if offer.get('companyName') is not None:
                        item_name = offer.get('companyName')
                        item_url = offer.get('companyUrl')
                        item_description = offer.get('companyDescription')
                        item_obj, exists = Company.objects.get_or_create(
                            name=item_name,
                            url=item_url,
                            description=item_description
                        )
                        sql_off.company = item_obj
                        sql_off.save()

                    if offer.get('cityName') is not None:
                        item_name = offer.get('cityName') + ', ' \
                                    + str(offer.get('regionName')) + ', ' \
                                    + str(offer.get('countryName'))
                        item_lat = offer.get('gpsLatitude')
                        item_long = offer.get('gpsLongitude')
                        item_obj, exists = Location.objects.get_or_create(
                            city_name=item_name,
                            gps_latitude=item_lat,
                            gps_longitude=item_long
                        )
                        sql_off.location = item_obj
                        sql_off.save()

                sleep(POLE_EMPLOI_API_TIMEOUT)
