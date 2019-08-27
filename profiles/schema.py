import graphene
from django.conf import settings
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from munigeo.models import AdministrativeDivision
from thesaurus.models import Concept

from .models import Profile


class ConceptType(DjangoObjectType):
    class Meta:
        model = Concept
        fields = ("code",)

    vocabulary = graphene.String()
    label = graphene.String()

    def resolve_vocabulary(self, info, **kwargs):
        return self.vocabulary.prefix


class AdministrativeDivisionType(DjangoObjectType):
    class Meta:
        model = AdministrativeDivision
        fields = ("children", "origin_id", "ocd_id", "municipality")

    type = graphene.String()
    name = graphene.String()

    def resolve_children(self, info, **kwargs):
        return self.children.filter(type__type="sub_district")

    def resolve_type(self, info, **kwargs):
        return self.type.type


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = (
            "nickname",
            "image",
            "email",
            "phone",
            "language",
            "contact_method",
            "concepts_of_interest",
            "divisions_of_interest",
        )

    concepts_of_interest = graphene.List(ConceptType)
    divisions_of_interest = graphene.List(AdministrativeDivisionType)

    def resolve_concepts_of_interest(self, info, **kwargs):
        return self.concepts_of_interest.all()

    def resolve_divisions_of_interest(self, info, **kwargs):
        return self.divisions_of_interest.all()


Language = graphene.Enum("Language", [(l[1].upper(), l[0]) for l in settings.LANGUAGES])
ContactMethod = graphene.Enum(
    "ContactMethod", [(cm[1].upper(), cm[0]) for cm in settings.CONTACT_METHODS]
)


class ProfileInput(graphene.InputObjectType):
    nickname = graphene.String()
    image = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    language = Language()
    contact_method = ContactMethod()
    concepts_of_interest = graphene.List(graphene.String)
    divisions_of_interest = graphene.List(graphene.String)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        profile = ProfileInput(required=True)

    profile = graphene.Field(ProfileType)

    @login_required
    def mutate(self, info, **kwargs):
        profile_data = kwargs.pop("profile")
        concepts_of_interest = profile_data.pop("concepts_of_interest", [])
        divisions_of_interest = profile_data.pop("divisions_of_interest", [])
        profile, created = Profile.objects.get_or_create(user=info.context.user)
        profile.nickname = profile_data.nickname
        profile.image = profile_data.image
        profile.email = profile_data.email
        profile.phone = profile_data.phone
        profile.language = profile_data.language
        profile.contact_method = profile_data.contact_method
        profile.save()

        cois = []
        for coi_data in concepts_of_interest:
            (prefix, code) = coi_data.split(":")
            c = Concept.objects.get(vocabulary__prefix=prefix, code=code)
            cois.append(c)
        profile.concepts_of_interest.set(cois)
        ads = []
        for ocd_id in divisions_of_interest:
            ad = AdministrativeDivision.objects.get(ocd_id=ocd_id)
            ads.append(ad)
        profile.divisions_of_interest.set(ads)

        return UpdateProfile(profile=profile)


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType)
    concepts_of_interest = graphene.List(ConceptType)
    divisions_of_interest = graphene.List(AdministrativeDivisionType)

    @login_required
    def resolve_profile(self, info, **kwargs):
        return Profile.objects.get(user=info.context.user)

    def resolve_concepts_of_interest(self, info, **kwargs):
        return Concept.objects.all()

    def resolve_divisions_of_interest(self, info, **kwargs):
        return AdministrativeDivision.objects.filter(division_of_interest__isnull=False)


class Mutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()
