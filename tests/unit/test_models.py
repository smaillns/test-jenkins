from installation_requests.models import InstallationRequest, RequestStatusEnum


def test_can_create_installation_request(db_session):
    # @todo
    # TESTER LES CHAMPS REQUIRED
    # SI ON A DES ENUM, TESTER QUE SEUL LES CHAMPS DONT ON A BESOIN SONT ACCEPTABLE. NON Faisable
    # pour l/'instant car on fait un string
    installation_request = InstallationRequest(
        user_id=1,
        budget=100,
        status="NEW",
        equipment_type="SOLAR",
        equipment_brand="",
        equipment_model="",
        comment="",
    )
    db_session.add(installation_request)
    db_session.commit()

    assert installation_request.id > 0
    assert installation_request.status == RequestStatusEnum.NEW
    assert installation_request.equipment_type == "SOLAR"
    assert installation_request.budget == 100
