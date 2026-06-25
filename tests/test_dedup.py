from app.models.asset import Asset


def test_asset_dedup_logic():

    asset1 = Asset(
        type="domain",
        value="example.com"
    )

    asset2 = Asset(
        type="domain",
        value="example.com"
    )

    assert asset1.type == asset2.type
    assert asset1.value == asset2.value