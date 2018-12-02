class Selector:

    def __init__(self, profile, available_objects):
        self.profile = profile
        self.available_objects = available_objects

    def compute_score(self, object):
        return 5

    def get_interesting(self, max_number=None):
        # Stocking interesting objects in an ordered list 'objects' where the
        # items of this list are tuples (object_id, score)
        objects = [
            (object.id, self.compute_score(object))
            for object in self.available_objects
            if self.compute_score(object) >= 1
        ]
        objects.sort(key=lambda object_tuple: object_tuple[1])
        ordered_objects_ids = [object[0] for object in objects][:max_number] if max_number != None \
            else [object[0] for object in objects]
        return ordered_objects_ids


class OfferSelector(Selector):

    def __init__(self, profile, available_offers):
        super().__init__(profile, available_offers)
        # definition of matching criteria
        self.desired_location = profile.desired_location
        if profile.desired_min_salary != None:
            self.desired_min_salary = profile.desired_min_salary
        else:
            self.desired_min_salary = 0
        if profile.desired_max_salary != None:
            self.desired_max_salary = profile.desired_max_salary
        else:
            self.desired_max_salary = 1000000
        self.desired_contract = profile.desired_contract
        self.skills = profile.skills
        self.languages = profile.languages

    def compute_score(self, offer):
        # TODO : to improve the location matching, we could compute the distance from the GPS coordinates
        # We select an offer if it's in the same city
        try:
            offer_location = offer.location
            score_location = 1 \
                if offer_location.city_name == self.desired_location.city_name \
                else 0.1
        except AttributeError:
            score_location = 0.1

        # We select an offer if it respects the min & max salaries desired
        try:
            offer_min_salary = offer.min_salary
            score_min_salary = 1 \
                if (offer_min_salary >= self.desired_min_salary or offer.min_salary is None) \
                else 0.1
        except AttributeError:
            score_min_salary = 0.1
        except TypeError:
            score_min_salary = 0.1

        try:
            offer_max_salary = offer.max_salary
            score_max_salary = 1 \
                if (offer_max_salary <= self.desired_max_salary or offer.max_salary is None) \
                else 0.1
        except AttributeError:
            score_max_salary = 0.1
        except TypeError:
            score_max_salary = 0.1

        # We select an offer if it respects the kind of contract desired
        try:
            offer_contract = offer.contract_type
            score_contract = 1 \
                if self.desired_contract == offer_contract \
                else 0.1
        except AttributeError:
            score_contract = 0.1

        # Languages are a +, count the number of languages satisfied
        score_language = 0.1
        for lang in self.languages.all():
            try:
                offer_languages = offer.languages
                if lang in offer_languages.all():
                    score_language += 1
            except AttributeError:
                pass

        # Count the number of skills satisfied.
        # To increase the number of skills that match the profile, we get skills
        # with similar names (because skills in database are ugly !)
        score_skills = 0.1
        for skill in self.skills.all():
            try:
                offer_skills = offer.skills
                if offer_skills.filter(name__search=skill.name) or offer_skills.filter(name__icontains=skill.name):
                    score_skills += 1
            except AttributeError:
                pass

        # Calculating the score, skills are weighted with 5, languages with 1
        score = score_location * score_min_salary * score_max_salary * score_contract * (score_skills * 5 + score_language)
        print(
            """=========SCORES========\nLOCATION: {}\nMIN_SALARY: {}\nMAX_SALARY: {}\nCONTRACT: {}\nLANGUAGE: {}\nSKILLS: {}\nTOTAL: {}\n"""
            .format(
                score_location,
                score_min_salary,
                score_max_salary,
                score_contract,
                score_language,
                score_skills,
                score
            )
        )
        return score


class FormationSelector(Selector):

    def __init__(self, profile, available_formations):
        super().__init__(profile, available_formations)
        # definition of matching criteria
        self.desired_location = profile.desired_location
        self.skills = profile.skills
        self.languages = profile.languages
        self.interests = profile.interests
        self.degrees = profile.degrees

    def compute_score(self, formation):
        try:
            formation_location = formation.location
            score_location = 1 \
                if formation_location.city_name == self.desired_location.city_name \
                else 0.1
        except AttributeError:
            score_location = 0.1

        score_language = 0.1
        for lang in self.languages.all():
            try:
                formation_languages = formation.language
                if lang in formation_languages.all():
                    score_language += 1
            except AttributeError:
                pass

        # Count the number of skills satisfied.
        # To increase the number of skills that match the profile, we get skills
        # with similar names (because skills in database are ugly !)
        score_skills = 0.1
        for skill in self.skills.all():
            try:
                formation_skills = formation.required_skills
                if formation_skills.filter(name__search=skill.name) or formation_skills.filter(name__icontains=skill.name):
                    score_skills += 1
            except AttributeError:
                pass

        score_degrees = 0.1
        for degree in self.degrees.all():
            try:
                formation_degrees = formation.required_degrees
                if formation_degrees.filter(name__search=degree.name) or formation_degree.filter(name__icontains=degree.name):
                    score_degrees += 1
            except AttributeError:
                pass

        # Calculating the score, skills are weighted with 5, languages with 1
        score = score_location * (score_skills * 5 + score_degrees + score_language)
        print(
            """=========SCORES========\nLOCATION: {}\nLANGUAGE: {}\nSKILLS: {}\nDEGREES: {}\nTOTAL: {}\n"""
            .format(
                score_location,
                score_language,
                score_skills,
                score_degrees,
                score
            )
        )
        return score
