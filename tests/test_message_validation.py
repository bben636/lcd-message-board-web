import pytest

from app.message_validation import parse_text_update

def test_accept_valid_message():
    # prepare a valid message
    data = {"seq": 1, "text": "Pozdrav"}
    
    # call the function being tested
    result = parse_text_update(data)
    
    assert result == (1, "Pozdrav")
    
def test_accept_empty_text():
    ## empty text clears out the display -> accepted
    result = parse_text_update({"seq": 2, "text": ""})
    
    assert result == (2, "")
    

@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        "Pozdrav",
        {},
        {"seq": 1},
        {"text": "Pozdrav"},
        {"seq": 0, "text": "Pozdrav"},
        {"seq": -1, "text": "Pozdrav"},
        {"seq": "1", "text": "Pozdrav"},
        {"seq": 1.5, "text": "Pozdrav"},
        {"seq": True, "text": "Pozdrav"},
        {"seq": 1, "text": 123},
        {"seq": 1, "text": None},
    ],
)
def test_rejects_invalid_message(data):
    #invalid msg raises a value error
    with pytest.raises(ValueError):
        parse_text_update(data)