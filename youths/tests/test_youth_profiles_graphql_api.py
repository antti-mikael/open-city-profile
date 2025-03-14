import uuid
from string import Template

from youths.tests.factories import ProfileFactory, YouthProfileFactory


def test_anon_user_query_should_fail(rf, youth_profile, anon_user_gql_client):
    request = rf.post("/graphql")
    request.user = anon_user_gql_client.user

    t = Template(
        """
        {
            youthProfile(profileId: "${profileId}") {
                schoolClass
            }
        }
        """
    )
    query = t.substitute(profileId=uuid.uuid4())
    expected_data = {"youthProfile": None}
    executed = anon_user_gql_client.execute(query, context=request)
    assert dict(executed["data"]) == expected_data


def test_normal_user_query_by_id_should_fail(rf, youth_profile, user_gql_client):
    request = rf.post("/graphql")
    request.user = user_gql_client.user

    t = Template(
        """
        {
            youthProfile(profileId: "${profileId}") {
                schoolClass
            }
        }
        """
    )
    query = t.substitute(profileId=uuid.uuid4())
    expected_data = {"youthProfile": None}
    executed = user_gql_client.execute(query, context=request)
    assert dict(executed["data"]) == expected_data


def test_normal_user_can_query_own_youth_profile(rf, user_gql_client):
    request = rf.post("/graphql")
    request.user = user_gql_client.user
    profile = ProfileFactory(user=user_gql_client.user)
    youth_profile = YouthProfileFactory(profile=profile)

    query = """
        {
            youthProfile {
                schoolClass
            }
        }
    """
    expected_data = {"youthProfile": {"schoolClass": youth_profile.school_class}}
    executed = user_gql_client.execute(query, context=request)
    assert dict(executed["data"]) == expected_data


def test_superuser_can_query_by_id(rf, youth_profile, superuser_gql_client):
    request = rf.post("/graphql")
    request.user = superuser_gql_client.user

    t = Template(
        """
        {
            youthProfile(profileId: "${profileId}") {
                schoolClass
            }
        }
        """
    )
    query = t.substitute(profileId=youth_profile.profile.pk)
    expected_data = {"youthProfile": {"schoolClass": youth_profile.school_class}}
    executed = superuser_gql_client.execute(query, context=request)
    assert dict(executed["data"]) == expected_data


def test_normal_user_can_create_youth_profile_mutation(rf, user_gql_client):
    request = rf.post("/graphql")
    request.user = user_gql_client.user
    profile = ProfileFactory(user=user_gql_client.user)

    t = Template(
        """
        mutation{
            createYouthProfile(
                profileId: "${profileId}"
                youthProfileData: {
                    schoolClass: "${schoolClass}"
                    schoolName: "${schoolName}"
                    languageAtHome: ${language}
                    approverEmail: "${approverEmail}"
                }
            )
            {
                youthProfile {
                    schoolClass
                    schoolName
                    approverEmail
                }
            }
        }
        """
    )
    creation_data = {
        "profileId": profile.pk,
        "schoolClass": "2A",
        "schoolName": "Alakoulu",
        "approverEmail": "hyvaksyja@ex.com",
        "language": "FINNISH",
    }
    query = t.substitute(**creation_data)
    expected_data = {
        "youthProfile": {
            "schoolClass": creation_data["schoolClass"],
            "schoolName": creation_data["schoolName"],
            "approverEmail": creation_data["approverEmail"],
        }
    }
    executed = user_gql_client.execute(query, context=request)
    assert dict(executed["data"]["createYouthProfile"]) == expected_data


def test_normal_user_can_update_youth_profile_mutation(rf, user_gql_client):
    request = rf.post("/graphql")
    request.user = user_gql_client.user

    profile = ProfileFactory(user=user_gql_client.user)
    youth_profile = YouthProfileFactory(profile=profile)

    t = Template(
        """
        mutation{
            updateYouthProfile(
                youthProfileData: {
                    schoolClass: "${schoolClass}"
                }
            )
            {
                youthProfile {
                    schoolClass
                    schoolName
                    approverEmail
                }
            }
        }
        """
    )
    creation_data = {"schoolClass": "2A"}
    query = t.substitute(**creation_data)
    expected_data = {
        "youthProfile": {
            "schoolClass": creation_data["schoolClass"],
            "schoolName": youth_profile.school_name,
            "approverEmail": youth_profile.approver_email,
        }
    }
    executed = user_gql_client.execute(query, context=request)
    assert dict(executed["data"]["updateYouthProfile"]) == expected_data


def test_superuser_can_create_youth_profile_mutation(rf, superuser_gql_client, user):
    request = rf.post("/graphql")
    request.user = superuser_gql_client.user
    profile = ProfileFactory(user=user)

    t = Template(
        """
        mutation{
            createYouthProfile(
                profileId: "${profileId}"
                youthProfileData: {
                    schoolClass: "${schoolClass}"
                    schoolName: "${schoolName}"
                    languageAtHome: ${language}
                    approverEmail: "${approverEmail}"
                }
            )
            {
                youthProfile {
                    schoolClass
                    schoolName
                    approverEmail
                }
            }
        }
        """
    )
    creation_data = {
        "profileId": profile.pk,
        "schoolClass": "2A",
        "schoolName": "Alakoulu",
        "approverEmail": "hyvaksyja@ex.com",
        "language": "FINNISH",
    }
    query = t.substitute(**creation_data)
    expected_data = {
        "youthProfile": {
            "schoolClass": creation_data["schoolClass"],
            "schoolName": creation_data["schoolName"],
            "approverEmail": creation_data["approverEmail"],
        }
    }
    executed = superuser_gql_client.execute(query, context=request)
    assert dict(executed["data"]["createYouthProfile"]) == expected_data


def test_superuser_can_update_youth_profile_mutation(
    rf, youth_profile, superuser_gql_client
):
    request = rf.post("/graphql")
    request.user = superuser_gql_client.user

    t = Template(
        """
        mutation{
            updateYouthProfile(
                profileId: "${profileId}"
                youthProfileData: {
                    schoolClass: "${schoolClass}"
                }
            )
            {
                youthProfile {
                    schoolClass
                    schoolName
                    approverEmail
                }
            }
        }
        """
    )
    creation_data = {"schoolClass": "2A", "profileId": youth_profile.profile.pk}
    query = t.substitute(**creation_data)
    expected_data = {
        "youthProfile": {
            "schoolClass": creation_data["schoolClass"],
            "schoolName": youth_profile.school_name,
            "approverEmail": youth_profile.approver_email,
        }
    }
    executed = superuser_gql_client.execute(query, context=request)
    assert dict(executed["data"]["updateYouthProfile"]) == expected_data


def test_anon_user_query_with_token(rf, youth_profile, anon_user_gql_client):
    request = rf.post("/graphql")
    request.user = anon_user_gql_client.user

    t = Template(
        """
        {
            youthProfileByApprovalToken(token: "${approvalToken}") {
                schoolClass
            }
        }
        """
    )
    query = t.substitute(approvalToken=youth_profile.approval_token)
    expected_data = {
        "youthProfileByApprovalToken": {"schoolClass": youth_profile.school_class}
    }
    executed = anon_user_gql_client.execute(query, context=request)
    assert dict(executed["data"]) == expected_data


def test_anon_user_can_approve_with_token(rf, youth_profile, anon_user_gql_client):
    request = rf.post("/graphql")
    request.user = anon_user_gql_client.user

    t = Template(
        """
        mutation{
            approveYouthProfile(
                approvalToken: "${token}",
                approvalData: {
                    photoUsageApproved: true
                    approverFirstName: "${approver_first_name}"
                    approverLastName: "${approver_last_name}"
                    approverPhone: "${approver_phone}"
                    approverEmail: "${approver_email}"
                }
            )
            {
                youthProfile {
                    photoUsageApproved
                    approverFirstName
                    approverLastName
                    approverPhone
                    approverEmail
                }
            }
        }
        """
    )
    approval_data = {
        "token": youth_profile.approval_token,
        "approver_first_name": "Teppo",
        "approver_last_name": "Testi",
        "approver_phone": "0401234567",
        "approver_email": "teppo@testi.com",
    }
    query = t.substitute(**approval_data)
    expected_data = {
        "youthProfile": {
            "photoUsageApproved": True,
            "approverFirstName": approval_data["approver_first_name"],
            "approverLastName": approval_data["approver_last_name"],
            "approverPhone": approval_data["approver_phone"],
            "approverEmail": approval_data["approver_email"],
        }
    }
    executed = anon_user_gql_client.execute(query, context=request)
    assert dict(executed["data"]["approveYouthProfile"]) == expected_data
