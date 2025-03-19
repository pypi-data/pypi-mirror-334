from genova import myfunctions

def test_haversine():
    assert myfunctions.haversine(
        4.895168, 52.370216, 13.404954, 52.520008
    ) == 576.6625818456291