from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#app-header", timeout=4)
    assert dash_duo.find_element("#app-header").text == "Soul Foods Pink Morsel Sales Visualiser"


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=4)
    assert dash_duo.find_element("#sales-line-chart") is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=4)
    assert dash_duo.find_element("#region-filter") is not None