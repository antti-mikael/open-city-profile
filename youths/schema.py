import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from profiles.models import Profile

from .consts import GENDERS, LANGUAGES
from .models import YouthProfile


class YouthProfileType(DjangoObjectType):
    class Meta:
        model = YouthProfile
        exclude = ["id"]


PreferredLanguage = graphene.Enum(
    "PreferredLanguage", [(l[0].upper(), l[0]) for l in LANGUAGES]
)
Gender = graphene.Enum("Gender", [(g[0].upper(), g[0]) for g in GENDERS])


class YouthProfileInput(graphene.InputObjectType):
    ssn = graphene.String(required=True)
    school_name = graphene.String(required=True)
    school_class = graphene.String(required=True)
    expiration = graphene.DateTime(required=True)
    preferred_language = PreferredLanguage()
    volunteer_info = graphene.String()
    gender = Gender(required=True)
    diabetes = graphene.Boolean()
    epilepsy = graphene.Boolean()
    heart_disease = graphene.Boolean()
    extra_illnesses_info = graphene.String()
    serious_allergies = graphene.Boolean()
    allergies = graphene.String()
    notes = graphene.String()
    # approved_by = ?
    approved_time = graphene.DateTime()
    photo_usage_approved = graphene.Boolean()


class UpdateYouthProfile(graphene.Mutation):
    class Arguments:
        youth_profile = YouthProfileInput(required=True)

    youth_profile = graphene.Field(YouthProfileType)

    @login_required
    def mutate(self, info, **kwargs):
        youth_profile_data = kwargs.pop("youth_profile")
        profile = Profile.objects.get(user=info.context.user)
        youth_profile, created = YouthProfile.objects.get_or_create(profile=profile)
        youth_profile.ssn = youth_profile_data.ssn
        youth_profile.school_name = youth_profile_data.school_name
        youth_profile.school_class = youth_profile_data.school_class
        youth_profile.expiration = youth_profile_data.expiration
        youth_profile.preferred_language = youth_profile_data.preferred_language
        youth_profile.volunteer_info = youth_profile_data.volunteer_info or ""
        youth_profile.gender = youth_profile_data.gender
        youth_profile.diabetes = youth_profile_data.diabetes or False
        youth_profile.epilepsy = youth_profile_data.epilepsy or False
        youth_profile.heart_disease = youth_profile_data.heart_disease or False
        youth_profile.extra_illnesses_info = (
            youth_profile_data.extra_illnesses_info or ""
        )
        youth_profile.serious_allergies = youth_profile_data.serious_allergies or False
        youth_profile.allergies = youth_profile_data.allergies or ""
        youth_profile.notes = youth_profile_data.notes or ""
        # approved_by = ?
        youth_profile.approved_time = youth_profile_data.approved_time
        youth_profile.photo_usage_approved = (
            youth_profile_data.photo_usage_approved or False
        )
        youth_profile.save()

        return UpdateYouthProfile(youth_profile=youth_profile)


class Query(graphene.ObjectType):
    youth_profile = graphene.Field(YouthProfileType)

    @login_required
    def resolve_youth_profile(self, info, **kwargs):
        profile = Profile.objects.get(user=info.context.user)
        return YouthProfile.objects.get(profile=profile)


class Mutation(graphene.ObjectType):
    update_youth_profile = UpdateYouthProfile.Field()
